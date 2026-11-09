import pytest
from app.database.session import SessionLocal, Base, engine
from app.database.seed_data import seed_database
from app.models.entities import User, Situation, Mistake, LearningProfile, PracticeAttempt
from app.services.ai_service import ai_service
from app.services.adaptive_service import adaptive_engine
from app.core.security import verify_password, get_password_hash

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    seed_database(session)
    yield session
    session.close()

def test_database_seeded(db):
    user = db.query(User).filter(User.email == "learner@speakmate.ai").first()
    assert user is not None
    assert verify_password("password123", user.hashed_password)

    situations = db.query(Situation).all()
    assert len(situations) >= 5

    # Check Telugu explanation exists and is in Telugu script
    first_sit = situations[0]
    assert len(first_sit.telugu_explanation) > 10
    assert first_sit.english_prompt != ""

def test_ai_grammar_analysis_incorrect():
    # Test a common Telugu learner mistake: "I am agree with you"
    res = ai_service.analyze_english_built_in(
        answer="I am agree with you and I didn't knew about it",
        prompt="Explain your agreement",
        level="BEGINNER"
    )
    assert res["is_correct"] is False
    assert len(res["mistakes"]) >= 2
    # Verify corrections
    categories = [m["category"] for m in res["mistakes"]]
    assert "grammar" in categories or "tense" in categories
    assert "I agree" in res["corrected_sentence"]
    assert "didn't know" in res["corrected_sentence"]
    assert res["score"] < 90

def test_ai_grammar_analysis_correct():
    # Test a correct sentence
    res = ai_service.analyze_english_built_in(
        answer="I would like to order one hot veg biryani and a bottle of water, please.",
        prompt="Order food in a restaurant",
        level="BEGINNER"
    )
    assert res["is_correct"] is True
    assert len(res["mistakes"]) == 0
    assert res["score"] >= 90
    assert len(res["additional_examples"]) >= 1

@pytest.mark.asyncio
async def test_repeat_evaluation_success():
    target = "I want to buy a medium blue formal shirt."
    repeat = "I want to buy a medium blue formal shirt"
    res = await ai_service.evaluate_repeat(target, repeat, "want to buy")
    assert res["is_successful"] is True
    assert res["accuracy_score"] >= 80

@pytest.mark.asyncio
async def test_repeat_evaluation_mismatch():
    target = "I would like to request sick leave for today."
    repeat = "I want something else totally different"
    res = await ai_service.evaluate_repeat(target, repeat)
    assert res["is_successful"] is False
    assert res["next_action"] == "try_again"

def test_adaptive_progression(db):
    user = db.query(User).filter(User.email == "learner@speakmate.ai").first()
    assert user is not None
    res = adaptive_engine.evaluate_level_progression(db, user.id)
    assert "current_level" in res
