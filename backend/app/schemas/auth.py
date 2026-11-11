from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ProfileOut(BaseModel):
    id: int
    user_id: int
    current_level: str
    daily_goal_minutes: int
    streak_count: int
    longest_streak: int = 0
    target_focus: str
    total_points: int

    class Config:
        from_attributes = True

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    current_level: Optional[str] = None
    daily_goal_minutes: Optional[int] = None
    target_focus: Optional[str] = None
