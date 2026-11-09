from datetime import datetime, date
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.entities import (
    Situation, PracticeAttempt, Mistake, Progress, LearningProfile, User
)
from app.services.ai_service import ai_service
from app.services.adaptive_service import adaptive_engine
from app.schemas.situation import (
    SituationAnalysisResponse, RepeatEvaluationResponse
)

class SituationService:
    @staticmethod
    def get_situations(db: Session, level: Optional[str] = None, category: Optional[str] = None) -> List[Situation]:
        query = db.query(Situation)
        if level:
            query = query.filter(Situation.level == level.upper())
        if category:
            query = query.filter(Situation.category == category)
        return query.order_by(Situation.id.asc()).all()

    @staticmethod
    def get_situation_by_id(db: Session, situation_id: int) -> Optional[Situation]:
        return db.query(Situation).filter(Situation.id == situation_id).first()

    @staticmethod
    async def generate_and_save_situation(db: Session, category: str, level: str) -> Situation:
        generated = await ai_service.generate_situation(category, level)
        situation = Situation(
            title=generated.get("title", f"{category} Practice"),
            category=generated.get("category", category),
            level=generated.get("level", level).upper(),
            telugu_explanation=generated.get("telugu_explanation", ""),
            telugu_transliteration=generated.get("telugu_transliteration", ""),
            english_prompt=generated.get("english_prompt", ""),
            context_tags=generated.get("context_tags", ""),
            is_system=False
        )
        db.add(situation)
        db.commit()
        db.refresh(situation)
        return situation

    @staticmethod
    async def submit_answer(
        db: Session,
        user: User,
        situation_id: int,
        original_answer: str,
        recognized_transcript: Optional[str] = None
    ) -> SituationAnalysisResponse:
        situation = db.query(Situation).filter(Situation.id == situation_id).first()
        situation_prompt = situation.english_prompt if situation else "General speaking scenario"
        level = user.profile.current_level if user.profile else "BEGINNER"

        # Check recurring mistakes history for this user
        past_mistakes_objs = db.query(Mistake).filter(Mistake.user_id == user.id, Mistake.is_resolved == False).limit(5).all()
        past_mistakes_str = ", ".join([f"{m.category}: {m.original_sentence}" for m in past_mistakes_objs]) if past_mistakes_objs else ""

        # Analyze answer using AI
        analysis = await ai_service.analyze_answer(
            answer=original_answer,
            prompt=situation_prompt,
            level=level,
            past_mistakes=past_mistakes_str
        )

        # Save Practice Attempt
        attempt = PracticeAttempt(
            user_id=user.id,
            situation_id=situation_id,
            original_answer=original_answer,
            recognized_transcript=recognized_transcript or original_answer,
            corrected_sentence=analysis.get("corrected_sentence", original_answer),
            mistakes_json=analysis.get("mistakes", []),
            explanation=analysis.get("simple_explanation", ""),
            natural_expression=analysis.get("natural_expression", ""),
            examples_json=analysis.get("additional_examples", []),
            score=analysis.get("score", 85.0),
            repeated_correctly=False,
            attempt_type="situation"
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)

        # Record mistakes in Mistake Journal
        for m in analysis.get("mistakes", []):
            existing_mistake = db.query(Mistake).filter(
                Mistake.user_id == user.id,
                Mistake.category == m.get("category"),
                Mistake.original_sentence == m.get("incorrect_part")
            ).first()

            if existing_mistake:
                existing_mistake.repetition_count += 1
                existing_mistake.is_resolved = False
                existing_mistake.updated_at = datetime.utcnow()
            else:
                new_mistake = Mistake(
                    user_id=user.id,
                    situation_id=situation_id,
                    original_sentence=m.get("incorrect_part", original_answer),
                    corrected_sentence=m.get("correction", analysis.get("corrected_sentence", "")),
                    category=m.get("category", "grammar"),
                    explanation=m.get("explanation", ""),
                    repetition_count=1,
                    is_resolved=False
                )
                db.add(new_mistake)
        db.commit()

        # Update Daily Progress & Profile Points
        today_str = date.today().isoformat()
        daily_progress = db.query(Progress).filter(
            Progress.user_id == user.id,
            Progress.date == today_str
        ).first()

        if not daily_progress:
            daily_progress = Progress(
                user_id=user.id,
                date=today_str,
                minutes_practiced=2.5,
                situations_completed=1,
                accuracy_score=analysis.get("score", 85.0),
                grammar_score=90.0 if analysis.get("is_correct") else 70.0,
                vocabulary_score=85.0,
                fluency_score=80.0
            )
            db.add(daily_progress)
        else:
            daily_progress.situations_completed += 1
            daily_progress.minutes_practiced += 2.5
            daily_progress.accuracy_score = (daily_progress.accuracy_score + analysis.get("score", 85.0)) / 2.0

        if user.profile:
            user.profile.total_points += 15 if analysis.get("is_correct") else 10
            user.profile.last_practice_date = datetime.utcnow()

        db.commit()

        # Check adaptive level progression
        adaptive_engine.evaluate_level_progression(db, user.id)

        return SituationAnalysisResponse(
            original_answer=analysis.get("original_answer", original_answer),
            is_correct=analysis.get("is_correct", False),
            score=analysis.get("score", 85.0),
            mistakes=analysis.get("mistakes", []),
            corrected_sentence=analysis.get("corrected_sentence", original_answer),
            simple_explanation=analysis.get("simple_explanation", ""),
            natural_expression=analysis.get("natural_expression", ""),
            additional_examples=analysis.get("additional_examples", []),
            encouragement=analysis.get("encouragement", ""),
            attempt_id=attempt.id
        )

    @staticmethod
    async def evaluate_repeated_sentence(
        db: Session,
        user: User,
        attempt_id: int,
        target_sentence: str,
        repeated_sentence: str,
        previous_mistake: Optional[str] = None
    ) -> RepeatEvaluationResponse:
        attempt = db.query(PracticeAttempt).filter(
            PracticeAttempt.id == attempt_id,
            PracticeAttempt.user_id == user.id
        ).first()

        result = await ai_service.evaluate_repeat(
            target_sentence=target_sentence,
            repeated_sentence=repeated_sentence,
            previous_mistake=previous_mistake
        )

        if attempt and result.get("is_successful"):
            attempt.repeated_correctly = True
            if user.profile:
                user.profile.total_points += 10  # Bonus points for successful repeat practice
            db.commit()

            # Mark associated mistake as resolved if exists
            if attempt.situation_id:
                mistakes = db.query(Mistake).filter(
                    Mistake.user_id == user.id,
                    Mistake.situation_id == attempt.situation_id
                ).all()
                for m in mistakes:
                    m.is_resolved = True
                db.commit()

        return RepeatEvaluationResponse(
            is_successful=result.get("is_successful", False),
            accuracy_score=result.get("accuracy_score", 0.0),
            feedback=result.get("feedback", ""),
            remaining_mistake=result.get("remaining_mistake"),
            next_action=result.get("next_action", "try_again"),
            encouragement=result.get("encouragement", "")
        )

situation_service = SituationService()
