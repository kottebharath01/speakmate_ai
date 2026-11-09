from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import User, Situation
from app.schemas.situation import (
    SituationOut, SituationSubmitRequest, SituationAnalysisResponse,
    RepeatEvaluationRequest, RepeatEvaluationResponse
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
