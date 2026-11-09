from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    message: str
    topic: Optional[str] = "General English Conversation"
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    reply: str
    gentle_tip: Optional[str] = None
    suggested_reply_ideas: List[str] = []

class SentenceCorrectionRequest(BaseModel):
    sentence: str

class SentenceCorrectionResponse(BaseModel):
    original: str
    is_grammatically_sound: bool
    corrected: str
    explanation: str

class InterviewStartRequest(BaseModel):
    topic: str  # HR, Self-Introduction, Python, SQL, Project
    level: Optional[str] = "INTERMEDIATE"

class InterviewAnswerRequest(BaseModel):
    topic: str
    question: str
    answer: str

class InterviewAnswerResponse(BaseModel):
    score: float
    strengths: List[str]
    areas_for_improvement: List[str]
    improved_model_answer: str
    interviewer_feedback: str
    next_question: str
