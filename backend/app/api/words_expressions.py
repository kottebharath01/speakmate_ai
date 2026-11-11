from typing import List, Optional, Dict, Any
from datetime import datetime, date
import random
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.database.session import get_db
from app.models.entities import User
from app.models.words_expressions import (
    WordItem, WordBookmark, WordProgress, WordExercise,
    WordSession, WordSessionAttempt, UserWordCompletion
)
from app.schemas.words_expressions import (
    WordItemOut, WordItemListResponse, CategoryCount,
    DailyFeaturedResponse, WordProgressStatsResponse,
    CheckSentenceRequest, CheckSentenceResponse,
    WordExerciseOut, ExerciseAnswerRequest, ExerciseAnswerResponse,
    ModeCategoryStat, ModeSummaryItem, ModesSummaryResponse,
    StartWordSessionRequest, WordSessionStateResponse, WordPromptItem,
    WordAttemptStateOut, SubmitWordAnswerRequest, SubmitWordAnswerResponse,
    RepeatWordAnswerRequest, RepeatWordAnswerResponse, WordSessionHistoryEntry
)
from app.services.ai_service import ai_service
from app.services.word_tutor_service import word_tutor_service
from app.services.streak_service import streak_service, parse_local_date
from app.utils.text_utils import normalize_text
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
        completed_rec = db.query(UserWordCompletion).filter(
            UserWordCompletion.user_id == user_id,
            UserWordCompletion.item_id == item.id
        ).first()
        if progress:
            is_learned = progress.is_learned or (completed_rec is not None)
            practice_count = progress.practice_count
        elif completed_rec is not None:
            is_learned = True
            practice_count = 1

    return WordItemOut(
        id=item.id,
        content_uid=item.content_uid,
        section=item.section,
        mode=item.mode,
        category=item.category,
        level=item.level,
        telugu_text=item.telugu_text,
        english_text=item.english_text,
        valid_alternatives_json=item.valid_alternatives_json,
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


# =========================================================================
# AI TUTOR-LED WORDS & EXPRESSIONS GUIDED SESSION ENDPOINTS
# =========================================================================

MODE_META = {
    "words": {
        "label": "Words",
        "description": "Individual everyday English words with Telugu meanings, multiple synonyms & real usage.",
    },
    "expressions": {
        "label": "Expressions",
        "description": "Daily conversational phrases, office expressions, complete sentences & interview idioms.",
    },
    "situation_expressions": {
        "label": "Situation Expressions",
        "description": "Topic-based spoken expressions across Daily Life, Office, Travel, Shopping, Restaurant & Interviews.",
    },
}


def _to_prompt_item(item: Optional[WordItem]) -> Optional[WordPromptItem]:
    if not item:
        return None
    return WordPromptItem(
        id=item.id,
        content_uid=item.content_uid,
        mode=item.mode or "words",
        category=item.category,
        level=item.level,
        telugu_text=item.telugu_text,
        telugu_transliteration=item.telugu_transliteration,
        pronunciation=item.pronunciation,
        part_of_speech=item.part_of_speech,
        prompt_question="How do you say this in English?",
    )


def _get_eligible_items_for_user(
    db: Session,
    user_id: int,
    mode: str,
    category: str = "All",
    is_revision: bool = False,
) -> List[WordItem]:
    """
    Selects eligible learning items for a mode & category.
    - New learning (is_revision=False): strictly excludes any already-completed item ID
      OR equivalent normalized_english expression across categories for this user.
    - Revision (is_revision=True): selects previously completed items cleanly separated from new learning.
    """
    completions = db.query(UserWordCompletion).filter(UserWordCompletion.user_id == user_id).all()
    completed_ids = {c.item_id for c in completions}
    completed_norms = {c.normalized_english for c in completions if c.normalized_english}

    query = db.query(WordItem).filter(WordItem.mode == mode)
    if category and category != "All":
        query = query.filter(WordItem.category == category)

    candidates = query.order_by(WordItem.id.asc()).all()
    eligible: List[WordItem] = []
    seen_norms = set()

    for item in candidates:
        norm = item.normalized_english or normalize_text(item.english_text)
        if is_revision:
            if item.id in completed_ids and norm not in seen_norms:
                eligible.append(item)
                seen_norms.add(norm)
        else:
            # Duplicate prevention across both exact ID and normalized equivalent text
            if item.id in completed_ids or (norm and norm in completed_norms) or (norm and norm in seen_norms):
                continue
            eligible.append(item)
            if norm:
                seen_norms.add(norm)

    return eligible


def _build_session_state(db: Session, session: WordSession) -> WordSessionStateResponse:
    current_item_obj = None
    if session.status == "active" and session.current_index < len(session.item_ids_json):
        item_id = session.item_ids_json[session.current_index]
        current_item_obj = db.query(WordItem).filter(WordItem.id == item_id).first()

    # Check if current item has an incomplete attempt awaiting repetition 1/2 or 2/2
    pending_attempt = None
    if current_item_obj:
        pending_attempt = (
            db.query(WordSessionAttempt)
            .filter(
                WordSessionAttempt.session_id == session.id,
                WordSessionAttempt.item_id == current_item_obj.id,
                WordSessionAttempt.item_completed == False,
            )
            .order_by(WordSessionAttempt.id.desc())
            .first()
        )

    return WordSessionStateResponse(
        id=session.id,
        mode=session.mode,
        category=session.category,
        daily_target=session.daily_target,
        completed_count=session.completed_count,
        current_index=session.current_index,
        status=session.status,
        is_revision=session.is_revision,
        local_date=session.local_date,
        current_item=_to_prompt_item(current_item_obj),
        pending_attempt=WordAttemptStateOut.model_validate(pending_attempt) if pending_attempt else None,
        started_at=session.started_at,
        completed_at=session.completed_at,
    )


def _record_item_completion_and_advance(
    db: Session,
    user: User,
    session: WordSession,
    item: WordItem,
) -> Dict[str, Any]:
    """Marks item completed (respecting revision separation) and checks session completion."""
    if not session.is_revision:
        norm = item.normalized_english or normalize_text(item.english_text)
        existing_comp = (
            db.query(UserWordCompletion)
            .filter(UserWordCompletion.user_id == user.id, UserWordCompletion.item_id == item.id)
            .first()
        )
        if not existing_comp:
            db.add(
                UserWordCompletion(
                    user_id=user.id,
                    item_id=item.id,
                    normalized_english=norm,
                    mode=item.mode or session.mode,
                )
            )
        # Also mirror learned marker in WordProgress
        wp = (
            db.query(WordProgress)
            .filter(WordProgress.user_id == user.id, WordProgress.item_id == item.id)
            .first()
        )
        if not wp:
            db.add(WordProgress(user_id=user.id, item_id=item.id, is_learned=True, practice_count=1))
        else:
            wp.is_learned = True
            wp.practice_count += 1
            wp.last_practiced_at = datetime.utcnow()

    session.completed_count += 1
    session.current_index += 1

    if user.profile:
        user.profile.total_points += 10

    session_completed = session.completed_count >= session.daily_target
    streak_info = None
    next_item_obj = None

    if session_completed:
        session.status = "completed"
        session.completed_at = datetime.utcnow()
        db.commit()
        streak_info = streak_service.record_session_completion(
            db, user.id, "words", session.local_date
        )
    else:
        if session.current_index < len(session.item_ids_json):
            next_id = session.item_ids_json[session.current_index]
            next_item_obj = db.query(WordItem).filter(WordItem.id == next_id).first()
        db.commit()

    return {
        "session_completed": session_completed,
        "next_item": _to_prompt_item(next_item_obj),
        "streak_info": streak_info,
    }


@router.get("/modes/summary", response_model=ModesSummaryResponse)
def get_modes_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    completions = db.query(UserWordCompletion).filter(UserWordCompletion.user_id == current_user.id).all()
    completed_ids = {c.item_id for c in completions}
    completed_norms = {c.normalized_english for c in completions if c.normalized_english}

    mode_summaries = []
    for mode_key, meta in MODE_META.items():
        all_mode_items = db.query(WordItem).filter(WordItem.mode == mode_key).order_by(WordItem.id.asc()).all()
        cat_totals: dict = {}
        cat_eligible: dict = {}

        seen_mode_norms = set()
        for item in all_mode_items:
            cat_totals[item.category] = cat_totals.get(item.category, 0) + 1
            norm = item.normalized_english or normalize_text(item.english_text)
            is_done = item.id in completed_ids or (norm in completed_norms) or (norm in seen_mode_norms)
            if not is_done:
                cat_eligible[item.category] = cat_eligible.get(item.category, 0) + 1
                if norm:
                    seen_mode_norms.add(norm)

        cat_stats = [
            ModeCategoryStat(
                name=cat,
                total_count=cat_totals[cat],
                remaining_new_count=cat_eligible.get(cat, 0),
            )
            for cat in sorted(cat_totals.keys())
        ]

        mode_summaries.append(
            ModeSummaryItem(
                mode=mode_key,
                label=meta["label"],
                description=meta["description"],
                total_items=len(all_mode_items),
                remaining_new_items=sum(c.remaining_new_count for c in cat_stats),
                categories=cat_stats,
            )
        )

    return ModesSummaryResponse(
        modes=mode_summaries,
        total_learned_by_user=len(completed_ids),
    )


@router.post("/sessions/start", response_model=WordSessionStateResponse)
def start_word_session(
    req: StartWordSessionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if req.mode not in MODE_META:
        raise HTTPException(status_code=400, detail="Invalid mode. Choose 'words', 'expressions', or 'situation_expressions'.")
    if req.daily_target < 1 or req.daily_target > 50:
        raise HTTPException(status_code=400, detail="Daily target must be between 1 and 50 items.")

    category = req.category or "All"
    eligible = _get_eligible_items_for_user(
        db=db,
        user_id=current_user.id,
        mode=req.mode,
        category=category,
        is_revision=req.is_revision,
    )

    if len(eligible) < req.daily_target:
        label = "completed items available to revise" if req.is_revision else "eligible new items remaining"
        raise HTTPException(
            status_code=400,
            detail=f"Only {len(eligible)} {label} for mode '{MODE_META[req.mode]['label']}' ({category}). "
                   f"Please lower your target to {len(eligible)} or fewer, choose another category, or switch to Revision mode."
        )

    selected_items = eligible[:req.daily_target]
    local_date_str = parse_local_date(req.local_date).isoformat()

    session = WordSession(
        user_id=current_user.id,
        mode=req.mode,
        category=category,
        daily_target=req.daily_target,
        completed_count=0,
        item_ids_json=[item.id for item in selected_items],
        current_index=0,
        status="active",
        is_revision=req.is_revision,
        local_date=local_date_str,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return _build_session_state(db, session)


@router.get("/sessions/active", response_model=Optional[WordSessionStateResponse])
def get_active_word_session(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = (
        db.query(WordSession)
        .filter(WordSession.user_id == current_user.id, WordSession.status == "active")
        .order_by(WordSession.id.desc())
        .first()
    )
    if not session:
        return None
    return _build_session_state(db, session)


@router.get("/sessions/history", response_model=List[WordSessionHistoryEntry])
def get_word_sessions_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sessions = (
        db.query(WordSession)
        .filter(WordSession.user_id == current_user.id)
        .order_by(WordSession.started_at.desc())
        .limit(30)
        .all()
    )
    history = []
    for s in sessions:
        attempts = (
            db.query(WordSessionAttempt)
            .filter(WordSessionAttempt.session_id == s.id, WordSessionAttempt.user_id == current_user.id)
            .order_by(WordSessionAttempt.created_at.asc())
            .all()
        )
        history.append(
            WordSessionHistoryEntry(
                id=s.id,
                mode=s.mode,
                category=s.category,
                daily_target=s.daily_target,
                completed_count=s.completed_count,
                status=s.status,
                is_revision=s.is_revision,
                local_date=s.local_date,
                started_at=s.started_at,
                completed_at=s.completed_at,
                attempts=[WordAttemptStateOut.model_validate(a) for a in attempts],
            )
        )
    return history


@router.get("/sessions/{session_id}", response_model=WordSessionStateResponse)
def get_word_session_by_id(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = (
        db.query(WordSession)
        .filter(WordSession.id == session_id, WordSession.user_id == current_user.id)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Learning session not found")
    return _build_session_state(db, session)


@router.post("/sessions/{session_id}/abandon")
def abandon_word_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = (
        db.query(WordSession)
        .filter(WordSession.id == session_id, WordSession.user_id == current_user.id)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Learning session not found")
    if session.status == "active":
        session.status = "abandoned"
        db.commit()
    return {"status": session.status, "session_id": session.id}


@router.post("/sessions/{session_id}/answer", response_model=SubmitWordAnswerResponse)
def submit_word_session_answer(
    session_id: int,
    req: SubmitWordAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = (
        db.query(WordSession)
        .filter(WordSession.id == session_id, WordSession.user_id == current_user.id)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Learning session not found")
    if session.status != "active":
        raise HTTPException(status_code=400, detail="This session is already completed.")
    if session.current_index >= len(session.item_ids_json):
        raise HTTPException(status_code=400, detail="All items in this session have been completed.")

    expected_item_id = session.item_ids_json[session.current_index]
    if req.item_id != expected_item_id:
        raise HTTPException(status_code=400, detail="Item mismatch with current session step.")

    item = db.query(WordItem).filter(WordItem.id == expected_item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if not req.answer or not req.answer.strip():
        raise HTTPException(status_code=400, detail="Please speak or type your English answer.")

    # Guard against bypassing incomplete correction repetitions
    existing_pending = (
        db.query(WordSessionAttempt)
        .filter(
            WordSessionAttempt.session_id == session.id,
            WordSessionAttempt.item_id == expected_item_id,
            WordSessionAttempt.item_completed == False,
        )
        .first()
    )
    if existing_pending:
        raise HTTPException(
            status_code=400,
            detail="Please complete the 2 required repetitions for the current item before submitting a new answer.",
        )

    # Evaluate answer semantically with valid alternatives support
    eval_result = word_tutor_service.evaluate_answer(item, req.answer)
    is_correct = eval_result["is_correct"]

    attempt = WordSessionAttempt(
        session_id=session.id,
        user_id=current_user.id,
        item_id=item.id,
        telugu_text=item.telugu_text,
        original_answer=req.answer.strip(),
        is_correct=is_correct,
        accepted_answer=eval_result["accepted_answer"],
        valid_alternatives_json=eval_result["valid_alternatives"],
        evaluation_feedback=eval_result["feedback"],
        correction_details=eval_result["correction_details"],
        example_sentence=eval_result["example_sentence"],
        repetition_required=not is_correct,
        repetition_success_count=0,
        repetition_history_json=[],
        item_completed=is_correct,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    if is_correct:
        adv = _record_item_completion_and_advance(db, current_user, session, item)
        return SubmitWordAnswerResponse(
            attempt_id=attempt.id,
            is_correct=True,
            accepted_answer=eval_result["accepted_answer"],
            valid_alternatives=eval_result["valid_alternatives"],
            evaluation_feedback=eval_result["feedback"],
            correction_details=None,
            example_sentence=eval_result["example_sentence"],
            repetition_required=False,
            repetitions_completed=0,
            repetitions_required=0,
            item_completed=True,
            session_completed=adv["session_completed"],
            completed_count=session.completed_count,
            daily_target=session.daily_target,
            next_item=adv["next_item"],
            streak_info=adv["streak_info"],
        )

    # Incorrect answer -> require exact 2 repetitions (1/2, 2/2)
    return SubmitWordAnswerResponse(
        attempt_id=attempt.id,
        is_correct=False,
        accepted_answer=eval_result["accepted_answer"],
        valid_alternatives=eval_result["valid_alternatives"],
        evaluation_feedback=eval_result["feedback"],
        correction_details=eval_result["correction_details"],
        example_sentence=eval_result["example_sentence"],
        repetition_required=True,
        repetitions_completed=0,
        repetitions_required=2,
        item_completed=False,
        session_completed=False,
        completed_count=session.completed_count,
        daily_target=session.daily_target,
        next_item=None,
        streak_info=None,
    )


@router.post("/sessions/{session_id}/repeat", response_model=RepeatWordAnswerResponse)
def submit_word_session_repeat(
    session_id: int,
    req: RepeatWordAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = (
        db.query(WordSession)
        .filter(WordSession.id == session_id, WordSession.user_id == current_user.id)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Learning session not found")
    if session.status != "active":
        raise HTTPException(status_code=400, detail="Session already completed.")

    attempt = (
        db.query(WordSessionAttempt)
        .filter(
            WordSessionAttempt.id == req.attempt_id,
            WordSessionAttempt.session_id == session.id,
            WordSessionAttempt.user_id == current_user.id,
        )
        .first()
    )
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt record not found")
    if attempt.item_completed:
        raise HTTPException(status_code=400, detail="This item is already completed.")

    rep_eval = word_tutor_service.evaluate_repetition(
        target_answer=attempt.accepted_answer,
        valid_alternatives=attempt.valid_alternatives_json or [],
        repeated_text=req.repeated_answer,
    )

    history = list(attempt.repetition_history_json or [])
    history.append({
        "attempt_text": req.repeated_answer.strip(),
        "is_successful": rep_eval["is_successful"],
        "accuracy": rep_eval["accuracy_score"],
    })
    attempt.repetition_history_json = history

    if not rep_eval["is_successful"]:
        db.commit()
        return RepeatWordAnswerResponse(
            attempt_id=attempt.id,
            is_successful=False,
            accuracy_score=rep_eval["accuracy_score"],
            feedback=rep_eval["feedback"],
            accepted_answer=attempt.accepted_answer,
            repetitions_completed=attempt.repetition_success_count,
            repetitions_required=2,
            item_completed=False,
            session_completed=False,
            completed_count=session.completed_count,
            daily_target=session.daily_target,
            next_item=None,
            streak_info=None,
        )

    # Successful repetition -> increment 1 -> 2
    attempt.repetition_success_count += 1

    if attempt.repetition_success_count < 2:
        db.commit()
        return RepeatWordAnswerResponse(
            attempt_id=attempt.id,
            is_successful=True,
            accuracy_score=rep_eval["accuracy_score"],
            feedback="Great! First repetition (1/2) complete. Now repeat it one more time (2/2) to lock it in.",
            accepted_answer=attempt.accepted_answer,
            repetitions_completed=attempt.repetition_success_count,
            repetitions_required=2,
            item_completed=False,
            session_completed=False,
            completed_count=session.completed_count,
            daily_target=session.daily_target,
            next_item=None,
            streak_info=None,
        )

    # Exact 2/2 repetitions complete -> mark item complete & advance automatically!
    attempt.item_completed = True
    item = db.query(WordItem).filter(WordItem.id == attempt.item_id).first()
    adv = _record_item_completion_and_advance(db, current_user, session, item)

    return RepeatWordAnswerResponse(
        attempt_id=attempt.id,
        is_successful=True,
        accuracy_score=rep_eval["accuracy_score"],
        feedback="Excellent! Both repetitions (2/2) completed cleanly!",
        accepted_answer=attempt.accepted_answer,
        repetitions_completed=2,
        repetitions_required=2,
        item_completed=True,
        session_completed=adv["session_completed"],
        completed_count=session.completed_count,
        daily_target=session.daily_target,
        next_item=adv["next_item"],
        streak_info=adv["streak_info"],
    )
