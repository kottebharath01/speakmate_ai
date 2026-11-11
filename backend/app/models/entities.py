import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime,
    ForeignKey, Float, Enum, JSON, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.database.session import Base

class DifficultyLevel(str, enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("LearningProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    mistakes = relationship("Mistake", back_populates="user", cascade="all, delete-orphan")
    progress_records = relationship("Progress", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="user", cascade="all, delete-orphan")
    learning_sessions = relationship("LearningSession", back_populates="user", cascade="all, delete-orphan")
    practice_attempts = relationship("PracticeAttempt", back_populates="user", cascade="all, delete-orphan")

class LearningProfile(Base):
    __tablename__ = "learning_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    current_level = Column(String(50), default="BEGINNER")
    daily_goal_minutes = Column(Integer, default=15)
    streak_count = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_practice_date = Column(DateTime, nullable=True)
    target_focus = Column(String(100), default="Spoken English & Real Situations")
    total_points = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, index=True)  # grammar, vocabulary, conversation
    level = Column(String(50), default="BEGINNER", index=True)
    description = Column(Text, nullable=True)
    content_json = Column(JSON, nullable=True)  # detailed lesson sections, definition, examples, rules
    order_num = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    exercises = relationship("Exercise", back_populates="lesson", cascade="all, delete-orphan")

class Situation(Base):
    __tablename__ = "situations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, index=True)  # Shopping, Travel, Dining, Workplace, Interview
    level = Column(String(50), default="BEGINNER", index=True)
    telugu_explanation = Column(Text, nullable=False)  # Simple Telugu explanation in Telugu script
    telugu_transliteration = Column(Text, nullable=True)  # Romanized Telugu for quick phonetic read
    english_prompt = Column(Text, nullable=False)  # "How would you explain..."
    context_tags = Column(String(255), nullable=True)
    is_system = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    exercises = relationship("Exercise", back_populates="situation")
    practice_attempts = relationship("PracticeAttempt", back_populates="situation")

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    situation_id = Column(Integer, ForeignKey("situations.id"), nullable=True)
    question = Column(Text, nullable=False)
    exercise_type = Column(String(50), default="speaking")  # speaking, multiple_choice, sentence_formation
    options_json = Column(JSON, nullable=True)
    expected_answer = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    lesson = relationship("Lesson", back_populates="exercises")
    situation = relationship("Situation", back_populates="exercises")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String(100), nullable=False)
    status = Column(String(50), default="active")  # active, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan")

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender = Column(String(20), nullable=False)  # "user" or "ai"
    message_text = Column(Text, nullable=False)
    feedback_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

class Mistake(Base):
    __tablename__ = "mistakes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    situation_id = Column(Integer, ForeignKey("situations.id"), nullable=True)
    original_sentence = Column(Text, nullable=False)
    corrected_sentence = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)  # grammar, tense, subject_verb, article, preposition, vocabulary, sentence_structure
    explanation = Column(Text, nullable=False)
    repetition_count = Column(Integer, default=1)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="mistakes")

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(String(20), nullable=False, index=True)  # YYYY-MM-DD
    minutes_practiced = Column(Float, default=0.0)
    situations_completed = Column(Integer, default=0)
    accuracy_score = Column(Float, default=0.0)
    grammar_score = Column(Float, default=0.0)
    vocabulary_score = Column(Float, default=0.0)
    fluency_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress_records")

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_type = Column(String(50), nullable=False)  # level_test, grammar_test, interview_eval
    score = Column(Float, nullable=False)
    feedback = Column(Text, nullable=True)
    assessed_level = Column(String(50), default="BEGINNER")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="assessments")

class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_type = Column(String(50), nullable=False)  # situation_practice, conversation, grammar, pattern, interview
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, default=0)
    items_completed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="learning_sessions")

class SentencePattern(Base):
    __tablename__ = "sentence_patterns"

    id = Column(Integer, primary_key=True, index=True)
    pattern = Column(String(100), nullable=False, unique=True)
    structure_formula = Column(String(200), nullable=False)
    purpose = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    level = Column(String(50), default="BEGINNER")
    examples_json = Column(JSON, nullable=False)  # list of examples with explanations
    speaking_prompt = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Vocabulary(Base):
    __tablename__ = "vocabulary"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), nullable=False, unique=True, index=True)
    part_of_speech = Column(String(50), nullable=False)
    telugu_meaning = Column(String(200), nullable=False)  # Telugu meaning
    english_definition = Column(Text, nullable=False)
    level = Column(String(50), default="BEGINNER", index=True)
    example_sentence = Column(Text, nullable=False)
    usage_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PracticeAttempt(Base):
    __tablename__ = "practice_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    situation_id = Column(Integer, ForeignKey("situations.id"), nullable=True)
    session_id = Column(Integer, ForeignKey("speaking_sessions.id"), nullable=True, index=True)
    original_answer = Column(Text, nullable=False)
    recognized_transcript = Column(Text, nullable=True)
    corrected_sentence = Column(Text, nullable=False)
    mistakes_json = Column(JSON, nullable=True)
    explanation = Column(Text, nullable=True)
    natural_expression = Column(Text, nullable=True)
    examples_json = Column(JSON, nullable=True)
    score = Column(Float, default=100.0)
    repeated_correctly = Column(Boolean, default=False)
    repetition_required = Column(Boolean, default=False)
    repetition_success_count = Column(Integer, default=0)
    repetition_history_json = Column(JSON, nullable=True)
    item_completed = Column(Boolean, default=False)
    attempt_type = Column(String(50), default="situation")  # situation, pattern, conversation, interview
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="practice_attempts")
    situation = relationship("Situation", back_populates="practice_attempts")


class SpeakingSession(Base):
    """Independent guided session for Module B: Speaking Practice."""
    __tablename__ = "speaking_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category = Column(String(100), nullable=False, default="All")
    daily_target = Column(Integer, nullable=False, default=5)
    completed_count = Column(Integer, default=0)
    situation_ids_json = Column(JSON, nullable=False)
    current_index = Column(Integer, default=0)
    status = Column(String(50), default="active")  # active, completed
    is_revision = Column(Boolean, default=False)
    local_date = Column(String(20), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class UserSituationCompletion(Base):
    """Prevents presenting already-completed speaking situations as new situations."""
    __tablename__ = "user_situation_completions"
    __table_args__ = (UniqueConstraint("user_id", "situation_id", name="uq_user_situation"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    situation_id = Column(Integer, ForeignKey("situations.id"), nullable=False, index=True)
    completed_at = Column(DateTime, default=datetime.utcnow)


class DailyActivity(Base):
    """Tracks completed meaningful sessions per calendar date in user's local timezone."""
    __tablename__ = "daily_activities"
    __table_args__ = (UniqueConstraint("user_id", "activity_date", name="uq_user_activity_date"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    activity_date = Column(String(20), nullable=False, index=True)  # YYYY-MM-DD
    words_sessions_completed = Column(Integer, default=0)
    speaking_sessions_completed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
