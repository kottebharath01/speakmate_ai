from typing import List, Optional
from datetime import datetime, date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import (
    User, Mistake, Progress, LearningProfile, Assessment,
    PracticeAttempt, SpeakingSession, UserSituationCompletion
)
from app.models.words_expressions import WordSession, UserWordCompletion
from app.schemas.progress import MistakeOut, ProgressOut, DashboardStatsOut
from app.services.streak_service import streak_service, parse_local_date
from app.api.deps import get_current_user

router = APIRouter(tags=["Progress & Analytics"])


@router.get("/streak")
def get_streak_details(
    local_date: Optional[str] = Query(None, description="YYYY-MM-DD in learner local timezone"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return streak_service.calculate_streaks(db, current_user.id, local_date)

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
    local_date: Optional[str] = Query(None, description="YYYY-MM-DD in learner local timezone"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = current_user.profile or db.query(LearningProfile).filter(LearningProfile.user_id == current_user.id).first()
    streak_info = streak_service.calculate_streaks(db, current_user.id, local_date)

    current_level = profile.current_level if profile else "BEGINNER"
    streak_count = streak_info["current_streak"]
    longest_streak = streak_info["longest_streak"]
    daily_goal_minutes = profile.daily_goal_minutes if profile else 15
    total_points = profile.total_points if profile else 0

    ref_date = parse_local_date(local_date)
    today_str = ref_date.isoformat()
    today_progress = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.date == today_str
    ).first()
    minutes_practiced_today = today_progress.minutes_practiced if today_progress else 0.0

    # Independent counts per module
    total_situations_completed = db.query(UserSituationCompletion).filter(
        UserSituationCompletion.user_id == current_user.id
    ).count()
    words_completed_count = db.query(UserWordCompletion).filter(
        UserWordCompletion.user_id == current_user.id
    ).count()
    words_sessions_completed = db.query(WordSession).filter(
        WordSession.user_id == current_user.id,
        WordSession.status == "completed"
    ).count()
    speaking_sessions_completed = db.query(SpeakingSession).filter(
        SpeakingSession.user_id == current_user.id,
        SpeakingSession.status == "completed"
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
        day_date = ref_date - timedelta(days=i)
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
        longest_streak=longest_streak,
        daily_goal_minutes=daily_goal_minutes,
        minutes_practiced_today=round(minutes_practiced_today, 1),
        total_situations_completed=total_situations_completed,
        total_mistakes_tracked=total_mistakes_tracked,
        total_mistakes_resolved=total_mistakes_resolved,
        total_points=total_points,
        words_completed_count=words_completed_count,
        speaking_sessions_completed=speaking_sessions_completed,
        words_sessions_completed=words_sessions_completed,
        recent_mistakes=recent_mistakes,
        weekly_accuracy_trend=weekly_accuracy_trend
    )
