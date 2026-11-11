from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class MistakeOut(BaseModel):
    id: int
    user_id: int
    situation_id: Optional[int]
    original_sentence: str
    corrected_sentence: str
    category: str
    explanation: str
    repetition_count: int
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ProgressOut(BaseModel):
    date: str
    minutes_practiced: float
    situations_completed: int
    accuracy_score: float
    grammar_score: float
    vocabulary_score: float
    fluency_score: float

    class Config:
        from_attributes = True

class DashboardStatsOut(BaseModel):
    current_level: str
    streak_count: int
    longest_streak: int = 0
    daily_goal_minutes: int
    minutes_practiced_today: float
    total_situations_completed: int
    total_mistakes_tracked: int
    total_mistakes_resolved: int
    total_points: int
    words_completed_count: int = 0
    speaking_sessions_completed: int = 0
    words_sessions_completed: int = 0
    recent_mistakes: List[MistakeOut]
    weekly_accuracy_trend: List[Dict[str, Any]]
