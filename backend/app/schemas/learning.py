from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class LessonOut(BaseModel):
    id: int
    title: str
    category: str
    level: str
    description: Optional[str] = None
    content_json: Optional[Dict[str, Any]] = None
    order_num: int

    class Config:
        from_attributes = True

class SentencePatternOut(BaseModel):
    id: int
    pattern: str
    structure_formula: str
    purpose: str
    explanation: str
    level: str
    examples_json: List[Dict[str, str]]
    speaking_prompt: str

    class Config:
        from_attributes = True

class VocabularyOut(BaseModel):
    id: int
    word: str
    part_of_speech: str
    telugu_meaning: str
    english_definition: str
    level: str
    example_sentence: str
    usage_notes: Optional[str] = None

    class Config:
        from_attributes = True

class DailyChallengeOut(BaseModel):
    id: int
    title: str
    topic: str
    description: str
    telugu_context: str
    speaking_prompt: str
    points: int
