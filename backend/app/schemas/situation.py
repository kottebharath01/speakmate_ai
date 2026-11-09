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
