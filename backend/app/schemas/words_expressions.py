from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class WordItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    section: str
    category: str
    level: str
    telugu_text: str
    english_text: str
    telugu_transliteration: Optional[str] = None
    english_definition: Optional[str] = None
    pronunciation: Optional[str] = None
    part_of_speech: Optional[str] = None
    when_to_use: Optional[str] = None
    sentence_structure: Optional[str] = None
    word_by_word_json: Optional[List[Dict[str, Any]]] = None
    contextual_alternatives_json: Optional[List[Dict[str, Any]]] = None
    examples_json: Optional[List[Dict[str, str]]] = None
    common_mistakes_json: Optional[List[Dict[str, str]]] = None
    synonyms_json: Optional[List[str]] = None
    dialogue_json: Optional[List[Dict[str, str]]] = None
    is_difficult: bool = False
    is_bookmarked: bool = False
    is_learned: bool = False
    practice_count: int = 0
    created_at: datetime

class WordItemListResponse(BaseModel):
    items: List[WordItemOut]
    total: int
    page: int
    page_size: int
    total_pages: int

class CategoryCount(BaseModel):
    name: str
    count: int

class DailyFeaturedResponse(BaseModel):
    word_of_the_day: Optional[WordItemOut] = None
    expression_of_the_day: Optional[WordItemOut] = None
    sentence_of_the_day: Optional[WordItemOut] = None

class WordProgressStatsResponse(BaseModel):
    total_items: int
    learned_count: int
    bookmarked_count: int
    percent_mastered: float
    sections_breakdown: Dict[str, Dict[str, int]]
    recent_learned: List[WordItemOut]

class CheckSentenceRequest(BaseModel):
    item_id: int
    target_text: str
    user_sentence: str

class CheckSentenceResponse(BaseModel):
    is_correct: bool
    score: float
    corrected_sentence: str
    feedback: str
    encouragement: str

class WordExerciseOut(BaseModel):
    id: int
    section: str
    exercise_type: str
    question: str
    telugu_prompt: Optional[str] = None
    options: List[str]
    explanation: Optional[str] = None

class ExerciseAnswerRequest(BaseModel):
    exercise_id: int
    selected_answer: str

class ExerciseAnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str
    encouragement: str
