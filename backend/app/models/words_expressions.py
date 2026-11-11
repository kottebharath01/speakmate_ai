import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime,
    ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from app.database.session import Base

class WordItem(Base):
    """
    Core content entity for the Words & Expressions module.
    Covers:
    - Section 1: Individual Words
    - Section 2: Daily Use Phrases and Expressions
    - Section 3: Complete Telugu-to-English Sentences
    - Section 4: Situation-Based Expressions
    """
    __tablename__ = "word_items"

    id = Column(Integer, primary_key=True, index=True)
    section = Column(String(50), nullable=False, index=True)  # "words", "phrases", "sentences", "situations"
    category = Column(String(100), nullable=False, index=True)
    level = Column(String(50), default="BEGINNER", index=True)  # BEGINNER, INTERMEDIATE, ADVANCED

    # Core bilingual data
    telugu_text = Column(Text, nullable=False, index=True)  # Word / phrase / sentence in Telugu script
    english_text = Column(Text, nullable=False, index=True)  # Primary natural English translation
    telugu_transliteration = Column(Text, nullable=True)  # Phonetic transliteration for pronunciation ease
    english_definition = Column(Text, nullable=True)  # Simple definition in plain English
    pronunciation = Column(String(100), nullable=True)  # Phonetic pronunciation guide
    part_of_speech = Column(String(50), nullable=True)  # Noun, Verb, Adjective, Phrase, Sentence, etc.

    # Contextual instructional depth
    when_to_use = Column(Text, nullable=True)  # Practical guidance on when & where to use it
    sentence_structure = Column(Text, nullable=True)  # Grammar pattern & tense explanation
    word_by_word_json = Column(JSON, nullable=True)  # [{telugu: "నేను", english: "I"}, ...]
    contextual_alternatives_json = Column(JSON, nullable=True)  # [{english: "Never mind", context: "Casual dismissal"}, ...]
    examples_json = Column(JSON, nullable=True)  # [{english: "...", telugu: "..."}]
    common_mistakes_json = Column(JSON, nullable=True)  # [{incorrect: "...", correct: "...", reason: "..."}]
    synonyms_json = Column(JSON, nullable=True)  # ["Synonym 1", "Synonym 2"]
    dialogue_json = Column(JSON, nullable=True)  # Practical A/B conversation for situations

    is_difficult = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    bookmarks = relationship("WordBookmark", back_populates="item", cascade="all, delete-orphan")
    progress_records = relationship("WordProgress", back_populates="item", cascade="all, delete-orphan")
    exercises = relationship("WordExercise", back_populates="item", cascade="all, delete-orphan")

class WordBookmark(Base):
    """Tracks bookmarked / favorite items per user."""
    __tablename__ = "word_bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("word_items.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    item = relationship("WordItem", back_populates="bookmarks")

class WordProgress(Base):
    """Tracks learned status and practice attempts per user."""
    __tablename__ = "word_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("word_items.id"), nullable=False, index=True)
    is_learned = Column(Boolean, default=False)
    is_favorite = Column(Boolean, default=False)
    practice_count = Column(Integer, default=0)
    last_practiced_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)

    item = relationship("WordItem", back_populates="progress_records")

class WordExercise(Base):
    """Quiz and exercise questions generated for words & expressions."""
    __tablename__ = "word_exercises"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("word_items.id"), nullable=True)
    section = Column(String(50), nullable=False)
    exercise_type = Column(String(50), nullable=False)  # translation, mcq, fill_blank, sentence_formation, usage_choice
    question = Column(Text, nullable=False)
    telugu_prompt = Column(Text, nullable=True)
    options_json = Column(JSON, nullable=True)
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    item = relationship("WordItem", back_populates="exercises")
