from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class WordItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content_uid: Optional[str] = None
    section: str
    mode: Optional[str] = None
    category: str
    level: str
    telugu_text: str
    english_text: str
    valid_alternatives_json: Optional[List[str]] = None
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


# =========================================================================
# AI TUTOR-LED WORDS & EXPRESSIONS SESSIONS (3 Modes + 2 Repetitions)
# =========================================================================

class ModeCategoryStat(BaseModel):
    name: str
    total_count: int
    remaining_new_count: int


class ModeSummaryItem(BaseModel):
    mode: str
    label: str
    description: str
    total_items: int
    remaining_new_items: int
    categories: List[ModeCategoryStat]


class ModesSummaryResponse(BaseModel):
    modes: List[ModeSummaryItem]
    total_learned_by_user: int


class StartWordSessionRequest(BaseModel):
    mode: str  # "words", "expressions", "situation_expressions"
    category: Optional[str] = "All"
    daily_target: int = 10
    is_revision: bool = False
    local_date: Optional[str] = None


class WordPromptItem(BaseModel):
    id: int
    content_uid: Optional[str] = None
    mode: str
    category: str
    level: str
    telugu_text: str
    telugu_transliteration: Optional[str] = None
    pronunciation: Optional[str] = None
    part_of_speech: Optional[str] = None
    prompt_question: str = "How do you say this in English?"


class WordAttemptStateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_id: int
    telugu_text: str
    original_answer: str
    is_correct: bool
    accepted_answer: str
    valid_alternatives_json: Optional[List[str]] = None
    evaluation_feedback: str
    correction_details: Optional[str] = None
    example_sentence: Optional[str] = None
    repetition_required: bool
    repetition_success_count: int
    item_completed: bool
    created_at: datetime


class WordSessionStateResponse(BaseModel):
    id: int
    mode: str
    category: str
    daily_target: int
    completed_count: int
    current_index: int
    status: str  # active, completed
    is_revision: bool
    local_date: str
    current_item: Optional[WordPromptItem] = None
    pending_attempt: Optional[WordAttemptStateOut] = None
    started_at: datetime
    completed_at: Optional[datetime] = None


class SubmitWordAnswerRequest(BaseModel):
    item_id: int
    answer: str


class SubmitWordAnswerResponse(BaseModel):
    attempt_id: int
    is_correct: bool
    accepted_answer: str
    valid_alternatives: List[str]
    evaluation_feedback: str
    correction_details: Optional[str] = None
    example_sentence: Optional[str] = None
    repetition_required: bool
    repetitions_completed: int
    repetitions_required: int
    item_completed: bool
    session_completed: bool
    completed_count: int
    daily_target: int
    next_item: Optional[WordPromptItem] = None
    streak_info: Optional[Dict[str, Any]] = None


class RepeatWordAnswerRequest(BaseModel):
    attempt_id: int
    repeated_answer: str


class RepeatWordAnswerResponse(BaseModel):
    attempt_id: int
    is_successful: bool
    accuracy_score: float
    feedback: str
    accepted_answer: str
    repetitions_completed: int
    repetitions_required: int
    item_completed: bool
    session_completed: bool
    completed_count: int
    daily_target: int
    next_item: Optional[WordPromptItem] = None
    streak_info: Optional[Dict[str, Any]] = None


class WordSessionHistoryEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    mode: str
    category: str
    daily_target: int
    completed_count: int
    status: str
    is_revision: bool
    local_date: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    attempts: List[WordAttemptStateOut] = []

