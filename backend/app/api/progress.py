from typing import List, Optional
from datetime import datetime, date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import User, Mistake, Progress, LearningProfile, Assessment, PracticeAttempt
from app.schemas.progress import MistakeOut, ProgressOut, DashboardStatsOut
from app.api.deps import get_current_user

router = APIRouter(tags=["Progress & Analytics"])

@router.get("/progress", response_model=List[ProgressOut])
def get_progress_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    records = db.query(Progress).filter(
        Progress.user_id == current_user.id
    ).order_by(Progress.date.asc()).limit(30).all()
    return records

@router.get("/mistakes", response_model=List[MistakeOut])
def get_mistakes(
    is_resolved: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Mistake).filter(Mistake.user_id == current_user.id)
    if is_resolved is not None:
        query = query.filter(Mistake.is_resolved == is_resolved)
    return query.order_by(Mistake.updated_at.desc()).all()

@router.get("/assessments")
def get_assessments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Assessment).filter(Assessment.user_id == current_user.id).order_by(Assessment.created_at.desc()).all()

@router.get("/dashboard-stats", response_model=DashboardStatsOut)
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = current_user.profile or db.query(LearningProfile).filter(LearningProfile.user_id == current_user.id).first()
    
    current_level = profile.current_level if profile else "BEGINNER"
    streak_count = profile.streak_count if profile else 1
    daily_goal_minutes = profile.daily_goal_minutes if profile else 20
    total_points = profile.total_points if profile else 50

    today_str = date.today().isoformat()
    today_progress = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.date == today_str
    ).first()
    minutes_practiced_today = today_progress.minutes_practiced if today_progress else 0.0

    total_situations_completed = db.query(PracticeAttempt).filter(
        PracticeAttempt.user_id == current_user.id
    ).count()

    total_mistakes_tracked = db.query(Mistake).filter(
        Mistake.user_id == current_user.id
    ).count()

    total_mistakes_resolved = db.query(Mistake).filter(
        Mistake.user_id == current_user.id,
        Mistake.is_resolved == True
    ).count()

    recent_mistakes = db.query(Mistake).filter(
        Mistake.user_id == current_user.id
    ).order_by(Mistake.updated_at.desc()).limit(5).all()

    # Weekly accuracy trend for charts
    weekly_accuracy_trend = []
    for i in range(6, -1, -1):
        day_date = date.today() - timedelta(days=i)
        day_str = day_date.isoformat()
        day_label = day_date.strftime("%a")
        prog = db.query(Progress).filter(
            Progress.user_id == current_user.id,
            Progress.date == day_str
        ).first()
        score = prog.accuracy_score if prog else 0.0
        situations = prog.situations_completed if prog else 0
        weekly_accuracy_trend.append({
            "day": day_label,
            "date": day_str,
            "accuracy": round(score, 1),
            "situations": situations
        })

    return DashboardStatsOut(
        current_level=current_level,
        streak_count=streak_count,
        daily_goal_minutes=daily_goal_minutes,
        minutes_practiced_today=round(minutes_practiced_today, 1),
        total_situations_completed=total_situations_completed,
        total_mistakes_tracked=total_mistakes_tracked,
        total_mistakes_resolved=total_mistakes_resolved,
        total_points=total_points,
        recent_mistakes=recent_mistakes,
        weekly_accuracy_trend=weekly_accuracy_trend
    )
