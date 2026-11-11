from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import User, Situation
from app.schemas.situation import (
    SituationOut, SituationSubmitRequest, SituationAnalysisResponse,
    RepeatEvaluationRequest, RepeatEvaluationResponse,
    SpeakingCategoryStat, StartSpeakingSessionRequest,
    SpeakingSessionStateResponse, SubmitSpeakingAnswerRequest,
    SubmitSpeakingAnswerResponse, RepeatSpeakingAnswerRequest,
    RepeatSpeakingAnswerResponse, SpeakingSessionHistoryEntry
)
from app.services.situation_service import situation_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/situations", tags=["Situations"])

@router.get("", response_model=List[SituationOut])
def list_situations(
    level: Optional[str] = Query(None, description="BEGINNER, INTERMEDIATE, or ADVANCED"),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return situation_service.get_situations(db, level=level, category=category)


# =========================================================================
# GUIDED SPEAKING PRACTICE SESSION ENDPOINTS
# (Declared BEFORE /{situation_id} to prevent integer path collision)
# =========================================================================

@router.get("/categories/stats", response_model=List[SpeakingCategoryStat])
def get_speaking_category_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return situation_service.get_category_stats(db, current_user.id)

@router.post("/sessions/start", response_model=SpeakingSessionStateResponse)
def start_speaking_session(
    req: StartSpeakingSessionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return situation_service.start_session(
        db=db,
        user=current_user,
        category=req.category or "All",
        daily_target=req.daily_target,
        is_revision=req.is_revision,
        local_date=req.local_date,
    )

@router.get("/sessions/active", response_model=Optional[SpeakingSessionStateResponse])
def get_active_speaking_session(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return situation_service.get_active_session(db, current_user)

@router.get("/sessions/history", response_model=List[SpeakingSessionHistoryEntry])
def get_speaking_session_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return situation_service.get_session_history(db, current_user)

@router.get("/sessions/{session_id}", response_model=SpeakingSessionStateResponse)
def get_speaking_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return situation_service.get_session_by_id(db, current_user, session_id)

@router.post("/sessions/{session_id}/abandon")
def abandon_speaking_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.models.entities import SpeakingSession
    session = (
        db.query(SpeakingSession)
        .filter(SpeakingSession.id == session_id, SpeakingSession.user_id == current_user.id)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Speaking session not found")
    if session.status == "active":
        session.status = "abandoned"
        db.commit()
    return {"status": session.status, "session_id": session.id}

@router.post("/sessions/{session_id}/submit", response_model=SubmitSpeakingAnswerResponse)
async def submit_speaking_session_answer(
    session_id: int,
    submission: SubmitSpeakingAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not submission.original_answer or not submission.original_answer.strip():
        raise HTTPException(status_code=400, detail="Answer cannot be empty.")

    return await situation_service.submit_session_answer(
        db=db,
        user=current_user,
        session_id=session_id,
        situation_id=submission.situation_id,
        original_answer=submission.original_answer,
        recognized_transcript=submission.recognized_transcript,
    )

@router.post("/sessions/{session_id}/repeat", response_model=RepeatSpeakingAnswerResponse)
async def evaluate_speaking_session_repeat(
    session_id: int,
    req: RepeatSpeakingAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await situation_service.evaluate_session_repeat(
        db=db,
        user=current_user,
        session_id=session_id,
        attempt_id=req.attempt_id,
        repeated_sentence=req.repeated_sentence,
    )


@router.get("/{situation_id}", response_model=SituationOut)
def get_situation(situation_id: int, db: Session = Depends(get_db)):
    situation = situation_service.get_situation_by_id(db, situation_id)
    if not situation:
        raise HTTPException(status_code=404, detail="Situation not found")
    return situation

@router.post("/generate", response_model=SituationOut)
async def generate_situation(
    category: str = Query("Daily Life"),
    level: str = Query("BEGINNER"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_level = current_user.profile.current_level if current_user.profile else level
    return await situation_service.generate_and_save_situation(db, category, user_level)

@router.post("/submit", response_model=SituationAnalysisResponse)
async def submit_situation_answer(
    submission: SituationSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not submission.original_answer.strip():
        raise HTTPException(status_code=400, detail="Answer cannot be empty.")
    
    return await situation_service.submit_answer(
        db=db,
        user=current_user,
        situation_id=submission.situation_id,
        original_answer=submission.original_answer,
        recognized_transcript=submission.recognized_transcript
    )

@router.post("/repeat-evaluation", response_model=RepeatEvaluationResponse)
async def repeat_evaluation(
    eval_req: RepeatEvaluationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await situation_service.evaluate_repeated_sentence(
        db=db,
        user=current_user,
        attempt_id=eval_req.attempt_id,
        target_sentence=eval_req.target_sentence,
        repeated_sentence=eval_req.repeated_sentence,
        previous_mistake=eval_req.previous_mistake
    )
