from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import User
from app.schemas.ai import (
    InterviewStartRequest, InterviewAnswerRequest, InterviewAnswerResponse
)
from app.services.ai_service import ai_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/interviews", tags=["Interview Preparation"])

INTERVIEW_TOPICS = {
    "Self-Introduction": [
        "Tell me about yourself, your educational background, and why you are interested in software engineering.",
        "Walk me through your key strengths and one area you are currently improving."
    ],
    "Python Developer": [
        "How do you explain the difference between lists and tuples in Python, and when would you use each?",
        "Explain how memory management and garbage collection work in Python.",
        "What are Python generators and decorators, and how have you used them in your projects?"
    ],
    "SQL & Database": [
        "Can you explain the difference between INNER JOIN, LEFT JOIN, and FULL OUTER JOIN with a quick example?",
        "How would you optimize a slow-running SQL query in production?"
    ],
    "Project Explanation": [
        "Walk me through the most impactful project you've built. What was the architecture and your specific role?",
        "Tell me about a difficult bug or production issue you solved in your project."
    ],
    "HR & Behavioral": [
        "Why should we hire you for this position over other candidates?",
        "Describe a situation where you had a disagreement with a team member and how you resolved it."
    ]
}

@router.post("/start")
def start_interview(req: InterviewStartRequest):
    topic = req.topic if req.topic in INTERVIEW_TOPICS else "Self-Introduction"
    questions = INTERVIEW_TOPICS[topic]
    return {
        "topic": topic,
        "first_question": questions[0],
        "total_questions": len(questions),
        "guidance": "Speak clearly. Maintain eye contact with the tutor. Structure your response with examples."
    }

@router.post("/answer", response_model=InterviewAnswerResponse)
async def answer_interview(
    req: InterviewAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_level = current_user.profile.current_level if current_user.profile else "INTERMEDIATE"
    eval_result = await ai_service.interview_practice(
        topic=req.topic,
        question=req.question,
        answer=req.answer,
        level=user_level
    )

    if current_user.profile:
        current_user.profile.total_points += 20
        db.commit()

    return InterviewAnswerResponse(
        score=eval_result.get("score", 80.0),
        strengths=eval_result.get("strengths", ["Clear explanation"]),
        areas_for_improvement=eval_result.get("areas_for_improvement", ["Use more concise sentences"]),
        improved_model_answer=eval_result.get("improved_model_answer", req.answer),
        interviewer_feedback=eval_result.get("interviewer_feedback", "Good communication effort."),
        next_question=eval_result.get("next_question", "Thank you! That completes this mock session.")
    )
