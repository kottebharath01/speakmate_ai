from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import User, LearningProfile
from app.schemas.auth import ProfileOut, ProfileUpdate
from app.services.streak_service import streak_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("", response_model=ProfileOut)
def get_profile(
    local_date: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(LearningProfile).filter(LearningProfile.user_id == current_user.id).first()
    if not profile:
        profile = LearningProfile(
            user_id=current_user.id,
            current_level="BEGINNER",
            daily_goal_minutes=15,
            streak_count=0,
            longest_streak=0,
            target_focus="Spoken English & Real Situations",
            total_points=0
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    streak_service.calculate_streaks(db, current_user.id, local_date)
    db.refresh(profile)
    return profile

@router.put("", response_model=ProfileOut)
def update_profile(
    profile_in: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(LearningProfile).filter(LearningProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    if profile_in.current_level:
        profile.current_level = profile_in.current_level.upper()
    if profile_in.daily_goal_minutes:
        profile.daily_goal_minutes = profile_in.daily_goal_minutes
    if profile_in.target_focus:
        profile.target_focus = profile_in.target_focus

    if profile_in.full_name:
        current_user.full_name = profile_in.full_name

    db.commit()
    db.refresh(profile)
    return profile
