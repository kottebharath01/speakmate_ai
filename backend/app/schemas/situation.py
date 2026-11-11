from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class MistakeDetail(BaseModel):
    category: str
    incorrect_part: str
    correction: str
    explanation: str

class SituationCreate(BaseModel):
    title: str
    category: str
    level: str = "BEGINNER"
    telugu_explanation: str
    telugu_transliteration: Optional[str] = None
    english_prompt: str
    context_tags: Optional[str] = None

class SituationOut(BaseModel):
    id: int
    title: str
    category: str
    level: str
    telugu_explanation: str
    telugu_transliteration: Optional[str] = None
    english_prompt: str
    context_tags: Optional[str] = None
    is_system: bool
    created_at: datetime

    class Config:
        from_attributes = True

class SituationSubmitRequest(BaseModel):
    situation_id: int
    original_answer: str
    recognized_transcript: Optional[str] = None

class SituationAnalysisResponse(BaseModel):
    original_answer: str
    is_correct: bool
    score: float
    mistakes: List[MistakeDetail] = []
    corrected_sentence: str
    simple_explanation: str
    natural_expression: str
    additional_examples: List[str] = []
    encouragement: str
    attempt_id: Optional[int] = None

class RepeatEvaluationRequest(BaseModel):
    attempt_id: int
    target_sentence: str
    repeated_sentence: str
    previous_mistake: Optional[str] = None

class RepeatEvaluationResponse(BaseModel):
    is_successful: bool
    accuracy_score: float
    feedback: str
    remaining_mistake: Optional[str] = None
    next_action: str
    encouragement: str


# =========================================================================
# AI TUTOR-LED SPEAKING PRACTICE SESSIONS (Target + 2 Repetitions)
# =========================================================================

class SpeakingCategoryStat(BaseModel):
    name: str
    total_count: int
    remaining_new_count: int


class StartSpeakingSessionRequest(BaseModel):
    category: Optional[str] = "All"
    daily_target: int = 5
    is_revision: bool = False
    local_date: Optional[str] = None


class SpeakingAttemptOut(BaseModel):
    id: int
    situation_id: Optional[int] = None
    situation_title: Optional[str] = None
    situation_question: Optional[str] = None
    original_answer: str
    corrected_sentence: str
    mistakes_json: Optional[List[Dict[str, Any]]] = None
    explanation: Optional[str] = None
    natural_expression: Optional[str] = None
    examples_json: Optional[List[str]] = None
    score: float
    repetition_required: bool = False
    repetition_success_count: int = 0
    item_completed: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class SpeakingSessionStateResponse(BaseModel):
    id: int
    category: str
    daily_target: int
    completed_count: int
    current_index: int
    status: str  # active, completed
    is_revision: bool
    local_date: str
    current_situation: Optional[SituationOut] = None
    pending_attempt: Optional[SpeakingAttemptOut] = None
    started_at: datetime
    completed_at: Optional[datetime] = None


class SubmitSpeakingAnswerRequest(BaseModel):
    situation_id: int
    original_answer: str
    recognized_transcript: Optional[str] = None


class SubmitSpeakingAnswerResponse(SituationAnalysisResponse):
    repetition_required: bool
    repetitions_completed: int
    repetitions_required: int
    item_completed: bool
    session_completed: bool
    completed_count: int
    daily_target: int
    next_situation: Optional[SituationOut] = None
    streak_info: Optional[Dict[str, Any]] = None


class RepeatSpeakingAnswerRequest(BaseModel):
    attempt_id: int
    repeated_sentence: str


class RepeatSpeakingAnswerResponse(RepeatEvaluationResponse):
    attempt_id: int
    repetitions_completed: int
    repetitions_required: int
    item_completed: bool
    session_completed: bool
    completed_count: int
    daily_target: int
    next_situation: Optional[SituationOut] = None
    streak_info: Optional[Dict[str, Any]] = None


class SpeakingSessionHistoryEntry(BaseModel):
    id: int
    category: str
    daily_target: int
    completed_count: int
    status: str
    is_revision: bool
    local_date: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    attempts: List[SpeakingAttemptOut] = []

