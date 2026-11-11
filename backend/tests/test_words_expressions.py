import pytest
from app.database.session import SessionLocal, Base, engine
from app.database.seed_data import seed_database
from app.database.seed_words_expressions import seed_words_expressions
from app.models.entities import User
from app.models.words_expressions import WordItem, WordBookmark, WordProgress, WordExercise
from app.api.words_expressions import (
    get_items, get_daily_featured, toggle_bookmark, toggle_learned,
    get_user_progress, check_exercise_answer
)
from app.schemas.words_expressions import ExerciseAnswerRequest

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    seed_database(session)
    seed_words_expressions(session)
    yield session
    session.close()

def test_words_expressions_seeded(db):
    total = db.query(WordItem).count()
    assert total >= 15, "Expected at least 15 comprehensive items seeded"

    # Check that all 4 sections are represented
    words = db.query(WordItem).filter(WordItem.section == "words").all()
    phrases = db.query(WordItem).filter(WordItem.section == "phrases").all()
    sentences = db.query(WordItem).filter(WordItem.section == "sentences").all()
    situations = db.query(WordItem).filter(WordItem.section == "situations").all()

    assert len(words) > 0, "Individual words section should have entries"
    assert len(phrases) > 0, "Daily use phrases section should have entries"
    assert len(sentences) > 0, "Complete sentences section should have entries"
    assert len(situations) > 0, "Situation expressions section should have entries"

    # Verify Telugu script presence
    convenient = db.query(WordItem).filter(WordItem.english_text == "Convenient").first()
    assert convenient is not None
    assert "సౌకర్యవంతమైన" in convenient.telugu_text
    assert len(convenient.examples_json) >= 2

def test_daily_featured_items(db):
    user = db.query(User).filter(User.email == "learner@speakmate.ai").first()
    featured = get_daily_featured(current_user=user, db=db)
    assert featured.word_of_the_day is not None
    assert featured.expression_of_the_day is not None
    assert featured.sentence_of_the_day is not None

def test_bookmark_and_learned_toggle(db):
    user = db.query(User).filter(User.email == "learner@speakmate.ai").first()
    item = db.query(WordItem).first()

    # Reset any existing test state for this user & item
    db.query(WordBookmark).filter(WordBookmark.user_id == user.id, WordBookmark.item_id == item.id).delete()
    db.query(WordProgress).filter(WordProgress.user_id == user.id, WordProgress.item_id == item.id).delete()
    db.commit()

    # Toggle Bookmark ON
    res_bm = toggle_bookmark(item_id=item.id, current_user=user, db=db)
    assert res_bm["is_bookmarked"] is True

    # Check progress stats reflects bookmark
    stats = get_user_progress(current_user=user, db=db)
    assert stats.bookmarked_count >= 1

    # Toggle Learned ON
    res_learn = toggle_learned(item_id=item.id, current_user=user, db=db)
    assert res_learn["is_learned"] is True

    stats_after = get_user_progress(current_user=user, db=db)
    assert stats_after.learned_count >= 1

def test_quiz_exercise_evaluation(db):
    user = db.query(User).filter(User.email == "learner@speakmate.ai").first()
    ex = db.query(WordExercise).first()
    assert ex is not None

    # Test correct answer
    req_correct = ExerciseAnswerRequest(exercise_id=ex.id, selected_answer=ex.correct_answer)
    res_correct = check_exercise_answer(req=req_correct, current_user=user, db=db)
    assert res_correct.is_correct is True

    # Test wrong answer
    req_wrong = ExerciseAnswerRequest(exercise_id=ex.id, selected_answer="CompletelyWrongXYZ")
    res_wrong = check_exercise_answer(req=req_wrong, current_user=user, db=db)
    assert res_wrong.is_correct is False
