import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.session import Base, get_db, ensure_schema_columns
from app.database.seed_data import seed_database
from app.database.seed_words_expressions import seed_words_expressions
from app.main import app


@pytest.fixture(scope="module")
def test_client_and_db():
    """Creates a completely isolated temporary SQLite DB so real user data is never touched."""
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    test_url = f"sqlite:///{db_path}"

    test_engine = create_engine(test_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    Base.metadata.create_all(bind=test_engine)
    ensure_schema_columns(test_engine)

    with TestingSessionLocal() as db:
        seed_database(db)
        seed_words_expressions(db)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    yield client, TestingSessionLocal

    app.dependency_overrides.clear()
    test_engine.dispose()
    if os.path.exists(db_path):
        os.remove(db_path)


def register_and_login(client: TestClient, email: str, username: str, password: str = "Pass123!") -> dict:
    reg = client.post(
        "/api/auth/register",
        json={"email": email, "username": username, "password": password, "full_name": username.title()},
    )
    assert reg.status_code == 200, reg.text
    tok = client.post("/api/auth/login", json={"email": email, "password": password})
    assert tok.status_code == 200, tok.text
    token = tok.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_authentication_and_user_isolation(test_client_and_db):
    client, _ = test_client_and_db

    # Negative test: Unauthenticated access must fail with 401
    unauth = client.get("/api/words-expressions/modes/summary")
    assert unauth.status_code == 401

    unauth_sp = client.get("/api/situations/sessions/history")
    assert unauth_sp.status_code == 401

    # Register two distinct users and verify session isolation
    headers_a = register_and_login(client, "alice@test.ai", "alice")
    headers_b = register_and_login(client, "bob@test.ai", "bob")

    # Fresh users must start with 0 streak & 0 points (not fake progress)
    prof_a = client.get("/api/profile", params={"local_date": "2026-11-01"}, headers=headers_a).json()
    assert prof_a["streak_count"] == 0
    assert prof_a["longest_streak"] == 0
    assert prof_a["total_points"] == 0

    # User A starts a Words session
    start_a = client.post(
        "/api/words-expressions/sessions/start",
        json={"mode": "words", "category": "All", "daily_target": 2, "local_date": "2026-11-01"},
        headers=headers_a,
    )
    assert start_a.status_code == 200
    session_a_id = start_a.json()["id"]

    # User B must NOT be able to access or abandon User A's session
    get_b = client.get(f"/api/words-expressions/sessions/{session_a_id}", headers=headers_b)
    assert get_b.status_code == 404

    abandon_b = client.post(f"/api/words-expressions/sessions/{session_a_id}/abandon", headers=headers_b)
    assert abandon_b.status_code == 404

    # Cleanup A's session
    client.post(f"/api/words-expressions/sessions/{session_a_id}/abandon", headers=headers_a)


def test_words_expressions_end_to_end_target_10_and_2_repetitions(test_client_and_db):
    client, db_factory = test_client_and_db
    headers = register_and_login(client, "words_e2e@test.ai", "wordse2e")

    # 1. Check modes summary returns all 3 official modes
    summary = client.get("/api/words-expressions/modes/summary", headers=headers).json()
    mode_keys = {m["mode"] for m in summary["modes"]}
    assert mode_keys == {"words", "expressions", "situation_expressions"}

    # Negative test: requesting target larger than available items is rejected cleanly (never padded)
    too_large = client.post(
        "/api/words-expressions/sessions/start",
        json={"mode": "words", "category": "All", "daily_target": 500, "local_date": "2026-11-02"},
        headers=headers,
    )
    assert too_large.status_code == 400

    # 2. Start exact target = 10 Words session
    start_res = client.post(
        "/api/words-expressions/sessions/start",
        json={"mode": "words", "category": "All", "daily_target": 10, "local_date": "2026-11-02"},
        headers=headers,
    )
    assert start_res.status_code == 200
    sess = start_res.json()
    session_id = sess["id"]
    assert sess["daily_target"] == 10
    assert sess["completed_count"] == 0
    assert sess["current_item"]["prompt_question"] == "How do you say this in English?"

    seen_item_ids = []

    # 3. Item 1: Test accepting valid ALTERNATIVE answer (e.g., "put off" for "వాయిదా వేయడం" / Postpone)
    item1 = sess["current_item"]
    seen_item_ids.append(item1["id"])
    with db_factory() as db:
        from app.models.words_expressions import WordItem
        db_item1 = db.query(WordItem).filter(WordItem.id == item1["id"]).first()
        alt_answer = (db_item1.valid_alternatives_json or [db_item1.english_text])[0]

    ans1 = client.post(
        f"/api/words-expressions/sessions/{session_id}/answer",
        json={"item_id": item1["id"], "answer": alt_answer},
        headers=headers,
    )
    assert ans1.status_code == 200
    ans1_data = ans1.json()
    assert ans1_data["is_correct"] is True
    assert ans1_data["repetition_required"] is False
    assert ans1_data["item_completed"] is True
    assert ans1_data["completed_count"] == 1
    assert ans1_data["next_item"] is not None

    # Incomplete session must NOT grant streak day yet!
    streak_mid = client.get("/api/streak", params={"local_date": "2026-11-02"}, headers=headers).json()
    assert streak_mid["current_streak"] == 0

    # 4. Item 2: Test INCORRECT answer -> Mistake explanation -> Exact 2 repetitions (1/2, 2/2)
    item2 = ans1_data["next_item"]
    seen_item_ids.append(item2["id"])
    ans2 = client.post(
        f"/api/words-expressions/sessions/{session_id}/answer",
        json={"item_id": item2["id"], "answer": "completely wrong answer xyz"},
        headers=headers,
    )
    assert ans2.status_code == 200
    ans2_data = ans2.json()
    assert ans2_data["is_correct"] is False
    assert ans2_data["repetition_required"] is True
    assert ans2_data["repetitions_required"] == 2
    assert ans2_data["item_completed"] is False
    assert ans2_data["next_item"] is None  # Cannot progress yet!
    attempt2_id = ans2_data["attempt_id"]
    target_eng = ans2_data["accepted_answer"]

    # Negative guard: Trying to answer Item 2 again before 2 repetitions fails
    blocked = client.post(
        f"/api/words-expressions/sessions/{session_id}/answer",
        json={"item_id": item2["id"], "answer": target_eng},
        headers=headers,
    )
    assert blocked.status_code == 400

    # Wrong repetition attempt must NOT increment repetition count
    bad_rep = client.post(
        f"/api/words-expressions/sessions/{session_id}/repeat",
        json={"attempt_id": attempt2_id, "repeated_answer": "wrong repeat words"},
        headers=headers,
    )
    assert bad_rep.status_code == 200
    assert bad_rep.json()["is_successful"] is False
    assert bad_rep.json()["repetitions_completed"] == 0

    # First accurate repetition (1/2)
    rep1 = client.post(
        f"/api/words-expressions/sessions/{session_id}/repeat",
        json={"attempt_id": attempt2_id, "repeated_answer": target_eng},
        headers=headers,
    )
    assert rep1.status_code == 200
    assert rep1.json()["is_successful"] is True
    assert rep1.json()["repetitions_completed"] == 1
    assert rep1.json()["item_completed"] is False  # Must NOT complete on 1/2!
    assert rep1.json()["next_item"] is None

    # Second accurate repetition (2/2) -> completes item & progresses automatically!
    rep2 = client.post(
        f"/api/words-expressions/sessions/{session_id}/repeat",
        json={"attempt_id": attempt2_id, "repeated_answer": target_eng},
        headers=headers,
    )
    assert rep2.status_code == 200
    rep2_data = rep2.json()
    assert rep2_data["is_successful"] is True
    assert rep2_data["repetitions_completed"] == 2
    assert rep2_data["item_completed"] is True
    assert rep2_data["completed_count"] == 2
    assert rep2_data["next_item"] is not None

    # 5. Complete items 3 through 10 accurately
    current_item = rep2_data["next_item"]
    for idx in range(3, 11):
        seen_item_ids.append(current_item["id"])
        with db_factory() as db:
            from app.models.words_expressions import WordItem
            db_item = db.query(WordItem).filter(WordItem.id == current_item["id"]).first()
            correct_str = db_item.english_text

        res = client.post(
            f"/api/words-expressions/sessions/{session_id}/answer",
            json={"item_id": current_item["id"], "answer": correct_str},
            headers=headers,
        )
        assert res.status_code == 200
        d = res.json()
        assert d["completed_count"] == idx
        if idx < 10:
            assert d["session_completed"] is False
            current_item = d["next_item"]
        else:
            assert d["session_completed"] is True
            assert d["next_item"] is None
            assert d["streak_info"]["current_streak"] == 1

    # Verify exact 10 unique items taught
    assert len(set(seen_item_ids)) == 10

    # Verify strict module separation: Speaking Practice counters must still be ZERO!
    dash = client.get("/api/dashboard-stats", params={"local_date": "2026-11-02"}, headers=headers).json()
    assert dash["words_completed_count"] == 10
    assert dash["words_sessions_completed"] == 1
    assert dash["total_situations_completed"] == 0
    assert dash["speaking_sessions_completed"] == 0

    # Verify history persistence
    hist = client.get("/api/words-expressions/sessions/history", headers=headers).json()
    assert len(hist) == 1
    assert hist[0]["status"] == "completed"
    assert hist[0]["completed_count"] == 10
    assert len(hist[0]["attempts"]) == 10

    # Verify strict duplicate prevention on next Words session: NONE of seen_item_ids appear!
    next_start = client.post(
        "/api/words-expressions/sessions/start",
        json={"mode": "words", "category": "All", "daily_target": 5, "local_date": "2026-11-03"},
        headers=headers,
    )
    assert next_start.status_code == 200
    next_item_id = next_start.json()["current_item"]["id"]
    assert next_item_id not in seen_item_ids


def test_speaking_practice_end_to_end_target_5_and_2_repetitions(test_client_and_db):
    client, _ = test_client_and_db
    headers = register_and_login(client, "speaking_e2e@test.ai", "speakinge2e")

    # 1. Start exact target = 5 Speaking Situations session
    start_res = client.post(
        "/api/situations/sessions/start",
        json={"category": "All", "daily_target": 5, "local_date": "2026-11-02"},
        headers=headers,
    )
    assert start_res.status_code == 200
    sess = start_res.json()
    session_id = sess["id"]
    assert sess["daily_target"] == 5
    assert sess["completed_count"] == 0
    sit1 = sess["current_situation"]
    assert len(sit1["telugu_explanation"]) > 5

    # 2. Situation 1: Clean accurate English -> NO forced repetitions!
    s1_res = client.post(
        f"/api/situations/sessions/{session_id}/submit",
        json={"situation_id": sit1["id"], "original_answer": "I would like to buy a medium blue cotton shirt please."},
        headers=headers,
    )
    assert s1_res.status_code == 200
    s1_data = s1_res.json()
    assert s1_data["is_correct"] is True
    assert s1_data["repetition_required"] is False
    assert s1_data["item_completed"] is True
    assert s1_data["completed_count"] == 1
    assert s1_data["next_situation"] is not None

    # 3. Situation 2: Incorrect English -> requires EXACTLY 2 repetitions (1/2, 2/2)
    sit2 = s1_data["next_situation"]
    s2_res = client.post(
        f"/api/situations/sessions/{session_id}/submit",
        json={"situation_id": sit2["id"], "original_answer": "I am agree and I didn't knew what to do."},
        headers=headers,
    )
    assert s2_res.status_code == 200
    s2_data = s2_res.json()
    assert s2_data["is_correct"] is False
    assert len(s2_data["mistakes"]) >= 1
    assert s2_data["repetition_required"] is True
    assert s2_data["repetitions_required"] == 2
    assert s2_data["item_completed"] is False
    attempt2_id = s2_data["attempt_id"]
    corrected = s2_data["corrected_sentence"]

    # First repeat (1/2) -> not yet completed
    rep1 = client.post(
        f"/api/situations/sessions/{session_id}/repeat",
        json={"attempt_id": attempt2_id, "repeated_sentence": corrected},
        headers=headers,
    )
    assert rep1.status_code == 200
    assert rep1.json()["is_successful"] is True
    assert rep1.json()["repetitions_completed"] == 1
    assert rep1.json()["item_completed"] is False

    # Second repeat (2/2) -> completed & auto-advances!
    rep2 = client.post(
        f"/api/situations/sessions/{session_id}/repeat",
        json={"attempt_id": attempt2_id, "repeated_sentence": corrected},
        headers=headers,
    )
    assert rep2.status_code == 200
    assert rep2.json()["is_successful"] is True
    assert rep2.json()["repetitions_completed"] == 2
    assert rep2.json()["item_completed"] is True
    assert rep2.json()["completed_count"] == 2

    # 4. Complete Situations 3, 4, 5 accurately
    curr_sit = rep2.json()["next_situation"]
    completed_ids = {sit1["id"], sit2["id"]}
    for idx in range(3, 6):
        completed_ids.add(curr_sit["id"])
        res = client.post(
            f"/api/situations/sessions/{session_id}/submit",
            json={"situation_id": curr_sit["id"], "original_answer": "Excuse me, could you please help me with this request right now?"},
            headers=headers,
        )
        assert res.status_code == 200
        d = res.json()
        assert d["completed_count"] == idx
        if idx < 5:
            assert d["session_completed"] is False
            curr_sit = d["next_situation"]
        else:
            assert d["session_completed"] is True
            assert d["streak_info"]["current_streak"] == 1

    # Strict module separation: Words & Expressions counts remain 0!
    dash = client.get("/api/dashboard-stats", params={"local_date": "2026-11-02"}, headers=headers).json()
    assert dash["total_situations_completed"] == 5
    assert dash["speaking_sessions_completed"] == 1
    assert dash["words_completed_count"] == 0
    assert dash["words_sessions_completed"] == 0

    # Persistent Speaking History check
    hist = client.get("/api/situations/sessions/history", headers=headers).json()
    assert len(hist) == 1
    assert hist[0]["status"] == "completed"
    assert hist[0]["completed_count"] == 5

    # Duplicate prevention check: next Speaking session never picks same situations
    next_sp = client.post(
        "/api/situations/sessions/start",
        json={"category": "All", "daily_target": 3, "local_date": "2026-11-03"},
        headers=headers,
    )
    assert next_sp.status_code == 200
    assert next_sp.json()["current_situation"]["id"] not in completed_ids


def test_streak_calendar_same_day_dedup_and_missed_day_reset(test_client_and_db):
    """
    Implements Section 17.7 Streak End-to-End Test using controlled dates:
    - Mon (2026-11-02): Complete Words session -> Day 1
    - Mon (2026-11-02): Also complete Speaking session -> Still Day 1 (never double-counted!)
    - Tue (2026-11-03): Complete Words session -> Day 2
    - Wed (2026-11-04): Complete Speaking session -> Day 3
    - Thu (2026-11-05): MISSED completely
    - Fri (2026-11-06 before session): Streak MUST reset to 0 while longest_streak == 3 preserved!
    - Fri (2026-11-06 complete session): Streak restarts at Day 1 while longest_streak stays 3!
    - Sat (2026-11-07 complete session): Streak is Day 2 while longest_streak stays 3!
    """
    client, db_factory = test_client_and_db
    headers = register_and_login(client, "streak_test@test.ai", "streakuser")

    def complete_one_word_session_on(local_date: str):
        s = client.post(
            "/api/words-expressions/sessions/start",
            json={"mode": "words", "category": "All", "daily_target": 1, "local_date": local_date},
            headers=headers,
        ).json()
        item_id = s["current_item"]["id"]
        with db_factory() as db:
            from app.models.words_expressions import WordItem
            eng = db.query(WordItem).filter(WordItem.id == item_id).first().english_text
        res = client.post(
            f"/api/words-expressions/sessions/{s['id']}/answer",
            json={"item_id": item_id, "answer": eng},
            headers=headers,
        ).json()
        assert res["session_completed"] is True
        return res["streak_info"]

    def complete_one_speaking_session_on(local_date: str):
        s = client.post(
            "/api/situations/sessions/start",
            json={"category": "All", "daily_target": 1, "local_date": local_date},
            headers=headers,
        ).json()
        sit_id = s["current_situation"]["id"]
        res = client.post(
            f"/api/situations/sessions/{s['id']}/submit",
            json={"situation_id": sit_id, "original_answer": "I would politely request help from my colleague today."},
            headers=headers,
        ).json()
        assert res["session_completed"] is True
        return res["streak_info"]

    # Day 1: Monday
    mon_words = complete_one_word_session_on("2026-11-02")
    assert mon_words["current_streak"] == 1
    assert mon_words["longest_streak"] == 1

    # Same Day Monday Speaking session -> MUST NOT double count!
    mon_speak = complete_one_speaking_session_on("2026-11-02")
    assert mon_speak["current_streak"] == 1
    assert mon_speak["longest_streak"] == 1
    assert mon_speak["words_completed_today"] == 1
    assert mon_speak["speaking_completed_today"] == 1

    # Day 2: Tuesday
    tue = complete_one_word_session_on("2026-11-03")
    assert tue["current_streak"] == 2
    assert tue["longest_streak"] == 2

    # Day 3: Wednesday
    wed = complete_one_speaking_session_on("2026-11-04")
    assert wed["current_streak"] == 3
    assert wed["longest_streak"] == 3

    # Check on Thursday (2026-11-05) during day -> still 3 (today isn't over yet)
    thu_check = client.get("/api/streak", params={"local_date": "2026-11-05"}, headers=headers).json()
    assert thu_check["current_streak"] == 3

    # Missed Thursday completely! Check on Friday (2026-11-06) BEFORE finishing Friday -> RESET to 0!
    fri_before = client.get("/api/streak", params={"local_date": "2026-11-06"}, headers=headers).json()
    assert fri_before["current_streak"] == 0
    assert fri_before["longest_streak"] == 3  # Previous longest preserved!

    # Complete session on Friday -> starts at Day 1, longest stays 3!
    fri_after = complete_one_word_session_on("2026-11-06")
    assert fri_after["current_streak"] == 1
    assert fri_after["longest_streak"] == 3

    # Complete session on Saturday -> Day 2, longest stays 3!
    sat = complete_one_speaking_session_on("2026-11-07")
    assert sat["current_streak"] == 2
    assert sat["longest_streak"] == 3


def test_revision_does_not_count_as_new_learning(test_client_and_db):
    client, db_factory = test_client_and_db
    headers = register_and_login(client, "rev_test@test.ai", "revuser")

    # Learn 2 words as new learning
    s = client.post(
        "/api/words-expressions/sessions/start",
        json={"mode": "words", "category": "All", "daily_target": 2, "local_date": "2026-11-08"},
        headers=headers,
    ).json()

    for _ in range(2):
        curr = client.get(f"/api/words-expressions/sessions/{s['id']}", headers=headers).json()["current_item"]
        with db_factory() as db:
            from app.models.words_expressions import WordItem
            eng = db.query(WordItem).filter(WordItem.id == curr["id"]).first().english_text
        client.post(
            f"/api/words-expressions/sessions/{s['id']}/answer",
            json={"item_id": curr["id"], "answer": eng},
            headers=headers,
        )

    dash_before = client.get("/api/dashboard-stats", params={"local_date": "2026-11-08"}, headers=headers).json()
    assert dash_before["words_completed_count"] == 2

    # Start Revision session targeting those 2 completed words
    rev = client.post(
        "/api/words-expressions/sessions/start",
        json={"mode": "words", "category": "All", "daily_target": 2, "is_revision": True, "local_date": "2026-11-08"},
        headers=headers,
    )
    assert rev.status_code == 200
    rev_sess = rev.json()
    assert rev_sess["is_revision"] is True

    for _ in range(2):
        curr = client.get(f"/api/words-expressions/sessions/{rev_sess['id']}", headers=headers).json()["current_item"]
        with db_factory() as db:
            from app.models.words_expressions import WordItem
            eng = db.query(WordItem).filter(WordItem.id == curr["id"]).first().english_text
        client.post(
            f"/api/words-expressions/sessions/{rev_sess['id']}/answer",
            json={"item_id": curr["id"], "answer": eng},
            headers=headers,
        )

    # New-learning counter must remain strictly 2!
    dash_after = client.get("/api/dashboard-stats", params={"local_date": "2026-11-08"}, headers=headers).json()
    assert dash_after["words_completed_count"] == 2
