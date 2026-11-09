from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import Lesson, SentencePattern, Vocabulary
from app.schemas.learning import (
    LessonOut, SentencePatternOut, VocabularyOut, DailyChallengeOut
)

router = APIRouter(tags=["Learning Modules"])

@router.get("/lessons", response_model=List[LessonOut])
def get_lessons(
    category: Optional[str] = None,
    level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Lesson)
    if category:
        query = query.filter(Lesson.category == category)
    if level:
        query = query.filter(Lesson.level == level.upper())
    return query.order_by(Lesson.order_num.asc()).all()

@router.get("/lessons/{lesson_id}", response_model=LessonOut)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.get("/patterns", response_model=List[SentencePatternOut])
def get_patterns(
    level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(SentencePattern)
    if level:
        query = query.filter(SentencePattern.level == level.upper())
    return query.order_by(SentencePattern.id.asc()).all()

@router.get("/vocabulary", response_model=List[VocabularyOut])
def get_vocabulary(
    level: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Vocabulary)
    if level:
        query = query.filter(Vocabulary.level == level.upper())
    if search:
        query = query.filter(Vocabulary.word.ilike(f"%{search}%"))
    return query.order_by(Vocabulary.id.asc()).all()

@router.get("/daily-challenges", response_model=List[DailyChallengeOut])
def get_daily_challenges():
    challenges = [
        {
            "id": 1,
            "title": "Morning Routine Description",
            "topic": "Daily Habits",
            "description": "Speak for at least 30 seconds describing your morning routine from waking up until starting work.",
            "telugu_context": "ఉదయం లేచినప్పటి నుండి కాలేజీ లేదా ఆఫీస్ వర్క్ మొదలయ్యే వరకు నీ మార్నింగ్ రొటీన్ గురించి ఇంగ్లీష్‌లో చెప్పాలి.",
            "speaking_prompt": "Describe what you do first in the morning, what you eat for breakfast, and how you prepare for your day.",
            "points": 25
        },
        {
            "id": 2,
            "title": "Explain Your Favourite Project",
            "topic": "Technical & Passion",
            "description": "Explain an exciting application or project you built or want to build.",
            "telugu_context": "నువ్వు డెవలప్ చేసిన లేదా చేయాలనుకుంటున్న ఒక సాఫ్ట్‌వేర్ ప్రాజెక్ట్ గురించి దాని ఫీచర్లతో సహా వివరించు.",
            "speaking_prompt": "Tell the tutor the problem your project solves, the tech stack you used, and what you learned.",
            "points": 35
        },
        {
            "id": 3,
            "title": "Why You Want to be a Python Backend Developer",
            "topic": "Career Goal",
            "description": "Express your ambition and technical enthusiasm for Python backend development.",
            "telugu_context": "నువ్వు పైథాన్ బ్యాకెండ్ డెవలపర్ ఎందుకు అవ్వాలనుకుంటున్నావో క్లియర్‌గా చెప్పు.",
            "speaking_prompt": "Explain why you chose Python, what backend frameworks you like, and your career aspiration.",
            "points": 30
        }
    ]
    return challenges
