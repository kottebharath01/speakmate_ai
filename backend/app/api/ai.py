from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import User, Conversation, ConversationMessage
from app.schemas.ai import (
    ChatRequest, ChatResponse, SentenceCorrectionRequest,
    SentenceCorrectionResponse
)
from app.schemas.situation import (
    RepeatEvaluationRequest, RepeatEvaluationResponse
)
from app.services.ai_service import ai_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/ai", tags=["AI Tutor"])

@router.post("/chat", response_model=ChatResponse)
async def chat_with_tutor(
    chat_in: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Retrieve or create conversation
    conv = None
    if chat_in.conversation_id:
        conv = db.query(Conversation).filter(
            Conversation.id == chat_in.conversation_id,
            Conversation.user_id == current_user.id
        ).first()

    if not conv:
        conv = Conversation(
            user_id=current_user.id,
            topic=chat_in.topic or "English Practice",
            status="active"
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)

    # Save user message
    user_msg = ConversationMessage(
        conversation_id=conv.id,
        sender="user",
        message_text=chat_in.message
    )
    db.add(user_msg)
    db.commit()

    # Get conversation history
    past_msgs = db.query(ConversationMessage).filter(
        ConversationMessage.conversation_id == conv.id
    ).order_by(ConversationMessage.created_at.desc()).limit(6).all()
    
    history_text = "\n".join([f"{m.sender}: {m.message_text}" for m in reversed(past_msgs)])
    user_level = current_user.profile.current_level if current_user.profile else "BEGINNER"

    ai_reply = await ai_service.chat_conversation(
        message=chat_in.message,
        topic=conv.topic,
        level=user_level,
        history=history_text
    )

    # Save AI message
    ai_msg = ConversationMessage(
        conversation_id=conv.id,
        sender="ai",
        message_text=ai_reply.get("reply", ""),
        feedback_json={"gentle_tip": ai_reply.get("gentle_tip")}
    )
    db.add(ai_msg)
    db.commit()

    return ChatResponse(
        conversation_id=conv.id,
        reply=ai_reply.get("reply", ""),
        gentle_tip=ai_reply.get("gentle_tip"),
        suggested_reply_ideas=ai_reply.get("suggested_reply_ideas", [])
    )

@router.post("/correct-sentence", response_model=SentenceCorrectionResponse)
async def correct_sentence(req: SentenceCorrectionRequest):
    analysis = ai_service.analyze_english_built_in(req.sentence, "Direct sentence correction", "BEGINNER")
    return SentenceCorrectionResponse(
        original=req.sentence,
        is_grammatically_sound=analysis.get("is_correct", False),
        corrected=analysis.get("corrected_sentence", req.sentence),
        explanation=analysis.get("simple_explanation", "")
    )

@router.post("/repeat-evaluation", response_model=RepeatEvaluationResponse)
async def direct_repeat_evaluation(req: RepeatEvaluationRequest):
    result = await ai_service.evaluate_repeat(
        target_sentence=req.target_sentence,
        repeated_sentence=req.repeated_sentence,
        previous_mistake=req.previous_mistake
    )
    return RepeatEvaluationResponse(
        is_successful=result.get("is_successful", False),
        accuracy_score=result.get("accuracy_score", 0.0),
        feedback=result.get("feedback", ""),
        remaining_mistake=result.get("remaining_mistake"),
        next_action=result.get("next_action", "try_again"),
        encouragement=result.get("encouragement", "")
    )
