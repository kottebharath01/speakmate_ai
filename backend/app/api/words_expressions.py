from typing import List, Optional
from datetime import datetime, date
import random
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.database.session import get_db
from app.models.entities import User
from app.models.words_expressions import (
    WordItem, WordBookmark, WordProgress, WordExercise
)
from app.schemas.words_expressions import (
    WordItemOut, WordItemListResponse, CategoryCount,
    DailyFeaturedResponse, WordProgressStatsResponse,
    CheckSentenceRequest, CheckSentenceResponse,
    WordExerciseOut, ExerciseAnswerRequest, ExerciseAnswerResponse
)
from app.services.ai_service import ai_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/words-expressions", tags=["Words & Expressions"])

def _hydrate_item_user_state(item: WordItem, user_id: Optional[int], db: Session) -> WordItemOut:
    """Helper to attach user-specific bookmarked & learned status."""
    is_bookmarked = False
    is_learned = False
    practice_count = 0

    if user_id:
        bookmark = db.query(WordBookmark).filter(
            WordBookmark.user_id == user_id,
            WordBookmark.item_id == item.id
        ).first()
        is_bookmarked = bookmark is not None

        progress = db.query(WordProgress).filter(
            WordProgress.user_id == user_id,
            WordProgress.item_id == item.id
        ).first()
        if progress:
            is_learned = progress.is_learned
            practice_count = progress.practice_count

    return WordItemOut(
        id=item.id,
        section=item.section,
        category=item.category,
        level=item.level,
        telugu_text=item.telugu_text,
        english_text=item.english_text,
        telugu_transliteration=item.telugu_transliteration,
        english_definition=item.english_definition,
        pronunciation=item.pronunciation,
        part_of_speech=item.part_of_speech,
        when_to_use=item.when_to_use,
        sentence_structure=item.sentence_structure,
        word_by_word_json=item.word_by_word_json,
        contextual_alternatives_json=item.contextual_alternatives_json,
        examples_json=item.examples_json,
        common_mistakes_json=item.common_mistakes_json,
        synonyms_json=item.synonyms_json,
        dialogue_json=item.dialogue_json,
        is_difficult=item.is_difficult,
        is_bookmarked=is_bookmarked,
        is_learned=is_learned,
        practice_count=practice_count,
        created_at=item.created_at
    )

@router.get("/items", response_model=WordItemListResponse)
def get_items(
    section: Optional[str] = Query(None, description="words, phrases, sentences, situations"),
    category: Optional[str] = None,
    level: Optional[str] = None,
    search: Optional[str] = None,
    bookmarked_only: bool = False,
    learned_only: bool = False,
    difficult_only: bool = False,
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(WordItem)

    if section:
        query = query.filter(WordItem.section == section.lower())
    if category and category != "All":
        query = query.filter(WordItem.category == category)
    if level and level != "ALL":
        query = query.filter(WordItem.level == level.upper())
    if difficult_only:
        query = query.filter(WordItem.is_difficult == True)

    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                WordItem.english_text.ilike(search_term),
                WordItem.telugu_text.ilike(search_term),
                WordItem.telugu_transliteration.ilike(search_term),
                WordItem.english_definition.ilike(search_term)
            )
        )

    # Filter bookmarked / learned for current user
    if bookmarked_only and current_user:
        bookmarked_ids = db.query(WordBookmark.item_id).filter(WordBookmark.user_id == current_user.id).subquery()
        query = query.filter(WordItem.id.in_(bookmarked_ids))

    if learned_only and current_user:
        learned_ids = db.query(WordProgress.item_id).filter(
            WordProgress.user_id == current_user.id,
            WordProgress.is_learned == True
        ).subquery()
        query = query.filter(WordItem.id.in_(learned_ids))

    total = query.count()
    offset = (page - 1) * page_size
    items = query.order_by(WordItem.id.asc()).offset(offset).limit(page_size).all()

    hydrated = [_hydrate_item_user_state(item, current_user.id if current_user else None, db) for item in items]
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return WordItemListResponse(
        items=hydrated,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.get("/items/{item_id}", response_model=WordItemOut)
def get_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(WordItem).filter(WordItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Word/Expression not found")
    return _hydrate_item_user_state(item, current_user.id if current_user else None, db)

@router.get("/categories", response_model=List[CategoryCount])
def get_categories(
    section: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(WordItem.category, func.count(WordItem.id).label("count"))
    if section:
        query = query.filter(WordItem.section == section.lower())
    results = query.group_by(WordItem.category).order_by(WordItem.category.asc()).all()
    return [CategoryCount(name=r[0], count=r[1]) for r in results]

@router.get("/daily-featured", response_model=DailyFeaturedResponse)
def get_daily_featured(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Deterministic daily rotation using day of year
    day_num = date.today().timetuple().tm_yday
    user_id = current_user.id if current_user else None

    # Word of the day
    words = db.query(WordItem).filter(WordItem.section == "words").order_by(WordItem.id.asc()).all()
    word_of_day = words[day_num % len(words)] if words else None

    # Expression of the day
    phrases = db.query(WordItem).filter(WordItem.section == "phrases").order_by(WordItem.id.asc()).all()
    phrase_of_day = phrases[(day_num + 1) % len(phrases)] if phrases else None

    # Sentence of the day
    sentences = db.query(WordItem).filter(WordItem.section == "sentences").order_by(WordItem.id.asc()).all()
    sentence_of_day = sentences[(day_num + 2) % len(sentences)] if sentences else None

    return DailyFeaturedResponse(
        word_of_the_day=_hydrate_item_user_state(word_of_day, user_id, db) if word_of_day else None,
        expression_of_the_day=_hydrate_item_user_state(phrase_of_day, user_id, db) if phrase_of_day else None,
        sentence_of_the_day=_hydrate_item_user_state(sentence_of_day, user_id, db) if sentence_of_day else None
    )

@router.get("/random", response_model=WordItemOut)
def get_random_item(
    section: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(WordItem)
    if section:
        query = query.filter(WordItem.section == section.lower())
    count = query.count()
    if count == 0:
        raise HTTPException(status_code=404, detail="No items available")
    
    random_offset = random.randint(0, count - 1)
    item = query.offset(random_offset).first()
    return _hydrate_item_user_state(item, current_user.id if current_user else None, db)

@router.post("/items/{item_id}/bookmark")
def toggle_bookmark(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(WordItem).filter(WordItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    existing = db.query(WordBookmark).filter(
        WordBookmark.user_id == current_user.id,
        WordBookmark.item_id == item_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"item_id": item_id, "is_bookmarked": False, "message": "Bookmark removed"}
    else:
        new_bm = WordBookmark(user_id=current_user.id, item_id=item_id)
        db.add(new_bm)
        db.commit()
        return {"item_id": item_id, "is_bookmarked": True, "message": "Bookmark added"}

@router.post("/items/{item_id}/mark-learned")
def toggle_learned(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(WordItem).filter(WordItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    progress = db.query(WordProgress).filter(
        WordProgress.user_id == current_user.id,
        WordProgress.item_id == item_id
    ).first()

    if not progress:
        progress = WordProgress(
            user_id=current_user.id,
            item_id=item_id,
            is_learned=True,
            practice_count=1,
            last_practiced_at=datetime.utcnow()
        )
        db.add(progress)
        is_learned = True
    else:
        progress.is_learned = not progress.is_learned
        progress.last_practiced_at = datetime.utcnow()
        is_learned = progress.is_learned

    if is_learned and current_user.profile:
        current_user.profile.total_points += 5

    db.commit()
    return {"item_id": item_id, "is_learned": is_learned, "message": "Learned status updated"}

@router.get("/progress", response_model=WordProgressStatsResponse)
def get_user_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_items = db.query(WordItem).count()
    learned_count = db.query(WordProgress).filter(
        WordProgress.user_id == current_user.id,
        WordProgress.is_learned == True
    ).count()

    bookmarked_count = db.query(WordBookmark).filter(
        WordBookmark.user_id == current_user.id
    ).count()

    percent = round((learned_count / total_items * 100), 1) if total_items > 0 else 0.0

    # Breakdown by section
    sections = ["words", "phrases", "sentences", "situations"]
    breakdown = {}
    for sec in sections:
        sec_total = db.query(WordItem).filter(WordItem.section == sec).count()
        sec_learned = db.query(WordProgress).join(WordItem).filter(
            WordProgress.user_id == current_user.id,
            WordProgress.is_learned == True,
            WordItem.section == sec
        ).count()
        breakdown[sec] = {"total": sec_total, "learned": sec_learned}

    # Recent learned items
    recent_progress = db.query(WordProgress).filter(
        WordProgress.user_id == current_user.id,
        WordProgress.is_learned == True
    ).order_by(WordProgress.last_practiced_at.desc()).limit(5).all()

    recent_items = [
        _hydrate_item_user_state(p.item, current_user.id, db)
        for p in recent_progress if p.item
    ]

    return WordProgressStatsResponse(
        total_items=total_items,
        learned_count=learned_count,
        bookmarked_count=bookmarked_count,
        percent_mastered=percent,
        sections_breakdown=breakdown,
        recent_learned=recent_items
    )

@router.get("/exercises", response_model=List[WordExerciseOut])
def get_exercises(
    section: Optional[str] = None,
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    query = db.query(WordExercise)
    if section:
        query = query.filter(WordExercise.section == section.lower())
    exercises = query.order_by(func.random()).limit(limit).all()

    return [
        WordExerciseOut(
            id=ex.id,
            section=ex.section,
            exercise_type=ex.exercise_type,
            question=ex.question,
            telugu_prompt=ex.telugu_prompt,
            options=ex.options_json or [],
            explanation=ex.explanation
        )
        for ex in exercises
    ]

@router.post("/check-exercise", response_model=ExerciseAnswerResponse)
def check_exercise_answer(
    req: ExerciseAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exercise = db.query(WordExercise).filter(WordExercise.id == req.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    is_correct = req.selected_answer.strip().lower() == exercise.correct_answer.strip().lower()

    if is_correct and current_user.profile:
        current_user.profile.total_points += 10
        db.commit()

    encouragement = (
        "Brilliant! You identified the exact native English usage."
        if is_correct
        else "Keep practicing! Review the explanation to understand the natural pattern."
    )

    return ExerciseAnswerResponse(
        is_correct=is_correct,
        correct_answer=exercise.correct_answer,
        explanation=exercise.explanation or "Good effort!",
        encouragement=encouragement
    )

@router.post("/check-sentence", response_model=CheckSentenceResponse)
async def check_custom_sentence(
    req: CheckSentenceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Learner creates their own sentence using a word or expression.
    AI verifies whether the sentence is grammatically correct and uses the target item properly.
    """
    sentence = req.user_sentence.strip()
    if not sentence:
        raise HTTPException(status_code=400, detail="Sentence cannot be empty")

    analysis = ai_service.analyze_english_built_in(
        answer=sentence,
        prompt=f"Sentence using word/expression '{req.target_text}'",
        level="INTERMEDIATE"
    )

    is_correct = analysis.get("is_correct", False)
    score = analysis.get("score", 85.0)
    corrected = analysis.get("corrected_sentence", sentence)
    explanation = analysis.get("simple_explanation", "")

    # Record practice in WordProgress if item_id is valid
    if req.item_id:
        progress = db.query(WordProgress).filter(
            WordProgress.user_id == current_user.id,
            WordProgress.item_id == req.item_id
        ).first()
        if not progress:
            progress = WordProgress(
                user_id=current_user.id,
                item_id=req.item_id,
                practice_count=1,
                last_practiced_at=datetime.utcnow()
            )
            db.add(progress)
        else:
            progress.practice_count += 1
            progress.last_practiced_at = datetime.utcnow()
        db.commit()

    encouragement = (
        f"Fantastic! You used '{req.target_text}' accurately in a natural English sentence."
        if is_correct
        else f"Good effort! Notice the corrected phrasing to make your sentence sound natural."
    )

    return CheckSentenceResponse(
        is_correct=is_correct,
        score=score,
        corrected_sentence=corrected,
        feedback=explanation,
        encouragement=encouragement
    )
