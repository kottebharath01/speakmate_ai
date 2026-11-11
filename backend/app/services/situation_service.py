from datetime import datetime, date
from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.entities import (
    Situation, PracticeAttempt, Mistake, Progress, LearningProfile, User,
    SpeakingSession, UserSituationCompletion
)
from app.services.ai_service import ai_service
from app.services.adaptive_service import adaptive_engine
from app.services.streak_service import streak_service, parse_local_date
from app.schemas.situation import (
    SituationAnalysisResponse, RepeatEvaluationResponse,
    SpeakingCategoryStat, SpeakingSessionStateResponse, SpeakingAttemptOut,
    SubmitSpeakingAnswerResponse, RepeatSpeakingAnswerResponse, SpeakingSessionHistoryEntry
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

    # =========================================================================
    # GUIDED AI SPEAKING PRACTICE SESSIONS (Independent Module B)
    # =========================================================================

    @staticmethod
    def get_category_stats(db: Session, user_id: int) -> List[SpeakingCategoryStat]:
        completed_ids = {
            row[0]
            for row in db.query(UserSituationCompletion.situation_id)
            .filter(UserSituationCompletion.user_id == user_id)
            .all()
        }
        all_sits = db.query(Situation).order_by(Situation.id.asc()).all()
        totals: dict = {}
        remaining: dict = {}
        for s in all_sits:
            totals[s.category] = totals.get(s.category, 0) + 1
            if s.id not in completed_ids:
                remaining[s.category] = remaining.get(s.category, 0) + 1

        return [
            SpeakingCategoryStat(
                name=cat,
                total_count=totals[cat],
                remaining_new_count=remaining.get(cat, 0),
            )
            for cat in sorted(totals.keys())
        ]

    @staticmethod
    def _build_session_state(db: Session, session: SpeakingSession) -> SpeakingSessionStateResponse:
        curr_sit = None
        if session.status == "active" and session.current_index < len(session.situation_ids_json):
            sit_id = session.situation_ids_json[session.current_index]
            curr_sit = db.query(Situation).filter(Situation.id == sit_id).first()

        pending_attempt = None
        if curr_sit:
            att = (
                db.query(PracticeAttempt)
                .filter(
                    PracticeAttempt.session_id == session.id,
                    PracticeAttempt.situation_id == curr_sit.id,
                    PracticeAttempt.item_completed == False,
                )
                .order_by(PracticeAttempt.id.desc())
                .first()
            )
            if att:
                pending_attempt = SpeakingAttemptOut(
                    id=att.id,
                    situation_id=att.situation_id,
                    situation_title=curr_sit.title,
                    situation_question=curr_sit.english_prompt,
                    original_answer=att.original_answer,
                    corrected_sentence=att.corrected_sentence,
                    mistakes_json=att.mistakes_json,
                    explanation=att.explanation,
                    natural_expression=att.natural_expression,
                    examples_json=att.examples_json,
                    score=att.score,
                    repetition_required=att.repetition_required,
                    repetition_success_count=att.repetition_success_count,
                    item_completed=att.item_completed,
                    created_at=att.created_at,
                )

        return SpeakingSessionStateResponse(
            id=session.id,
            category=session.category,
            daily_target=session.daily_target,
            completed_count=session.completed_count,
            current_index=session.current_index,
            status=session.status,
            is_revision=session.is_revision,
            local_date=session.local_date,
            current_situation=curr_sit,
            pending_attempt=pending_attempt,
            started_at=session.started_at,
            completed_at=session.completed_at,
        )

    @staticmethod
    def start_session(
        db: Session,
        user: User,
        category: str = "All",
        daily_target: int = 5,
        is_revision: bool = False,
        local_date: Optional[str] = None,
    ) -> SpeakingSessionStateResponse:
        if daily_target < 1 or daily_target > 25:
            raise HTTPException(status_code=400, detail="Daily target must be between 1 and 25 situations.")

        completed_ids = {
            row[0]
            for row in db.query(UserSituationCompletion.situation_id)
            .filter(UserSituationCompletion.user_id == user.id)
            .all()
        }

        query = db.query(Situation)
        if category and category != "All":
            query = query.filter(Situation.category == category)

        # Prefer user's adaptive level first, while including all levels in selected category so target isn't artificially starved
        candidates = query.order_by(Situation.id.asc()).all()
        user_level = user.profile.current_level if user.profile else "BEGINNER"
        candidates_sorted = sorted(candidates, key=lambda s: (0 if s.level == user_level else 1, s.id))

        eligible = []
        seen_questions = set()
        for sit in candidates_sorted:
            q_key = (sit.english_prompt or "").strip().lower()
            if is_revision:
                if sit.id in completed_ids and q_key not in seen_questions:
                    eligible.append(sit)
                    seen_questions.add(q_key)
            else:
                if sit.id not in completed_ids and q_key not in seen_questions:
                    eligible.append(sit)
                    seen_questions.add(q_key)

        if len(eligible) < daily_target:
            label = "completed situations available to revise" if is_revision else "eligible new situations remaining"
            raise HTTPException(
                status_code=400,
                detail=f"Only {len(eligible)} {label} in '{category}'. Please lower your target to {len(eligible)} or choose 'All Categories'."
            )

        selected = eligible[:daily_target]
        local_date_str = parse_local_date(local_date).isoformat()

        session = SpeakingSession(
            user_id=user.id,
            category=category or "All",
            daily_target=daily_target,
            completed_count=0,
            situation_ids_json=[s.id for s in selected],
            current_index=0,
            status="active",
            is_revision=is_revision,
            local_date=local_date_str,
        )
        db.add(session)
        db.commit()
        db.refresh(session)

        return SituationService._build_session_state(db, session)

    @staticmethod
    def get_active_session(db: Session, user: User) -> Optional[SpeakingSessionStateResponse]:
        session = (
            db.query(SpeakingSession)
            .filter(SpeakingSession.user_id == user.id, SpeakingSession.status == "active")
            .order_by(SpeakingSession.id.desc())
            .first()
        )
        if not session:
            return None
        return SituationService._build_session_state(db, session)

    @staticmethod
    def get_session_by_id(db: Session, user: User, session_id: int) -> SpeakingSessionStateResponse:
        session = (
            db.query(SpeakingSession)
            .filter(SpeakingSession.id == session_id, SpeakingSession.user_id == user.id)
            .first()
        )
        if not session:
            raise HTTPException(status_code=404, detail="Speaking practice session not found")
        return SituationService._build_session_state(db, session)

    @staticmethod
    def get_session_history(db: Session, user: User) -> List[SpeakingSessionHistoryEntry]:
        sessions = (
            db.query(SpeakingSession)
            .filter(SpeakingSession.user_id == user.id)
            .order_by(SpeakingSession.started_at.desc())
            .limit(30)
            .all()
        )
        results = []
        for s in sessions:
            attempts = (
                db.query(PracticeAttempt)
                .filter(PracticeAttempt.session_id == s.id, PracticeAttempt.user_id == user.id)
                .order_by(PracticeAttempt.created_at.asc())
                .all()
            )
            attempt_outs = []
            for a in attempts:
                sit = a.situation
                attempt_outs.append(
                    SpeakingAttemptOut(
                        id=a.id,
                        situation_id=a.situation_id,
                        situation_title=sit.title if sit else None,
                        situation_question=sit.english_prompt if sit else None,
                        original_answer=a.original_answer,
                        corrected_sentence=a.corrected_sentence,
                        mistakes_json=a.mistakes_json,
                        explanation=a.explanation,
                        natural_expression=a.natural_expression,
                        examples_json=a.examples_json,
                        score=a.score,
                        repetition_required=a.repetition_required,
                        repetition_success_count=a.repetition_success_count,
                        item_completed=a.item_completed,
                        created_at=a.created_at,
                    )
                )
            results.append(
                SpeakingSessionHistoryEntry(
                    id=s.id,
                    category=s.category,
                    daily_target=s.daily_target,
                    completed_count=s.completed_count,
                    status=s.status,
                    is_revision=s.is_revision,
                    local_date=s.local_date,
                    started_at=s.started_at,
                    completed_at=s.completed_at,
                    attempts=attempt_outs,
                )
            )
        return results

    @staticmethod
    def _complete_speaking_item_and_advance(
        db: Session,
        user: User,
        session: SpeakingSession,
        situation_id: int,
    ) -> Dict[str, Any]:
        if not session.is_revision:
            existing = (
                db.query(UserSituationCompletion)
                .filter(
                    UserSituationCompletion.user_id == user.id,
                    UserSituationCompletion.situation_id == situation_id,
                )
                .first()
            )
            if not existing:
                db.add(UserSituationCompletion(user_id=user.id, situation_id=situation_id))

        session.completed_count += 1
        session.current_index += 1

        if user.profile:
            user.profile.total_points += 15

        session_completed = session.completed_count >= session.daily_target
        next_sit = None
        streak_info = None

        if session_completed:
            session.status = "completed"
            session.completed_at = datetime.utcnow()
            db.commit()
            streak_info = streak_service.record_session_completion(
                db, user.id, "speaking", session.local_date
            )
        else:
            if session.current_index < len(session.situation_ids_json):
                next_id = session.situation_ids_json[session.current_index]
                next_sit = db.query(Situation).filter(Situation.id == next_id).first()
            db.commit()

        return {
            "session_completed": session_completed,
            "next_situation": next_sit,
            "streak_info": streak_info,
        }

    @staticmethod
    async def submit_session_answer(
        db: Session,
        user: User,
        session_id: int,
        situation_id: int,
        original_answer: str,
        recognized_transcript: Optional[str] = None,
    ) -> SubmitSpeakingAnswerResponse:
        session = (
            db.query(SpeakingSession)
            .filter(SpeakingSession.id == session_id, SpeakingSession.user_id == user.id)
            .first()
        )
        if not session:
            raise HTTPException(status_code=404, detail="Speaking session not found")
        if session.status != "active":
            raise HTTPException(status_code=400, detail="Speaking session is already completed")
        if session.current_index >= len(session.situation_ids_json):
            raise HTTPException(status_code=400, detail="All situations in this session are completed")

        expected_sit_id = session.situation_ids_json[session.current_index]
        if situation_id != expected_sit_id:
            raise HTTPException(status_code=400, detail="Situation mismatch with current session step.")

        existing_pending = (
            db.query(PracticeAttempt)
            .filter(
                PracticeAttempt.session_id == session.id,
                PracticeAttempt.situation_id == expected_sit_id,
                PracticeAttempt.item_completed == False,
            )
            .first()
        )
        if existing_pending:
            raise HTTPException(
                status_code=400,
                detail="Please complete the 2 required repetitions for the current situation first.",
            )

        situation = db.query(Situation).filter(Situation.id == expected_sit_id).first()
        situation_prompt = situation.english_prompt if situation else "Speaking scenario"
        level = user.profile.current_level if user.profile else "BEGINNER"

        past_mistakes_objs = db.query(Mistake).filter(Mistake.user_id == user.id, Mistake.is_resolved == False).limit(5).all()
        past_mistakes_str = ", ".join([f"{m.category}: {m.original_sentence}" for m in past_mistakes_objs]) if past_mistakes_objs else ""

        analysis = await ai_service.analyze_answer(
            answer=original_answer,
            prompt=situation_prompt,
            level=level,
            past_mistakes=past_mistakes_str,
        )
        is_correct = bool(analysis.get("is_correct", False))

        attempt = PracticeAttempt(
            user_id=user.id,
            situation_id=situation_id,
            session_id=session.id,
            original_answer=original_answer.strip(),
            recognized_transcript=recognized_transcript or original_answer.strip(),
            corrected_sentence=analysis.get("corrected_sentence", original_answer.strip()),
            mistakes_json=analysis.get("mistakes", []),
            explanation=analysis.get("simple_explanation", ""),
            natural_expression=analysis.get("natural_expression", ""),
            examples_json=analysis.get("additional_examples", []),
            score=analysis.get("score", 85.0),
            repeated_correctly=is_correct,
            repetition_required=not is_correct,
            repetition_success_count=0,
            repetition_history_json=[],
            item_completed=is_correct,
            attempt_type="situation",
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)

        # Save mistakes to Mistake Journal
        for m in analysis.get("mistakes", []):
            existing_mistake = db.query(Mistake).filter(
                Mistake.user_id == user.id,
                Mistake.category == m.get("category"),
                Mistake.original_sentence == m.get("incorrect_part"),
            ).first()
            if existing_mistake:
                existing_mistake.repetition_count += 1
                existing_mistake.is_resolved = False
                existing_mistake.updated_at = datetime.utcnow()
            else:
                db.add(
                    Mistake(
                        user_id=user.id,
                        situation_id=situation_id,
                        original_sentence=m.get("incorrect_part", original_answer),
                        corrected_sentence=m.get("correction", analysis.get("corrected_sentence", "")),
                        category=m.get("category", "grammar"),
                        explanation=m.get("explanation", ""),
                        repetition_count=1,
                        is_resolved=False,
                    )
                )

        # Update Daily Progress chart metric (strictly for Speaking Practice)
        today_str = session.local_date
        daily_progress = db.query(Progress).filter(
            Progress.user_id == user.id, Progress.date == today_str
        ).first()
        if not daily_progress:
            db.add(
                Progress(
                    user_id=user.id,
                    date=today_str,
                    minutes_practiced=2.5,
                    situations_completed=1 if is_correct else 0,
                    accuracy_score=analysis.get("score", 85.0),
                    grammar_score=95.0 if is_correct else 70.0,
                    vocabulary_score=85.0,
                    fluency_score=80.0,
                )
            )
        else:
            if is_correct:
                daily_progress.situations_completed += 1
            daily_progress.minutes_practiced += 2.5
            daily_progress.accuracy_score = (daily_progress.accuracy_score + analysis.get("score", 85.0)) / 2.0

        db.commit()
        adaptive_engine.evaluate_level_progression(db, user.id)

        if is_correct:
            adv = SituationService._complete_speaking_item_and_advance(db, user, session, situation_id)
            return SubmitSpeakingAnswerResponse(
                original_answer=analysis.get("original_answer", original_answer),
                is_correct=True,
                score=analysis.get("score", 95.0),
                mistakes=[],
                corrected_sentence=analysis.get("corrected_sentence", original_answer),
                simple_explanation=analysis.get("simple_explanation", ""),
                natural_expression=analysis.get("natural_expression", ""),
                additional_examples=analysis.get("additional_examples", []),
                encouragement=analysis.get("encouragement", "Excellent English!"),
                attempt_id=attempt.id,
                repetition_required=False,
                repetitions_completed=0,
                repetitions_required=0,
                item_completed=True,
                session_completed=adv["session_completed"],
                completed_count=session.completed_count,
                daily_target=session.daily_target,
                next_situation=adv["next_situation"],
                streak_info=adv["streak_info"],
            )

        # Mistakes found -> require exact 2 repetitions (1/2, 2/2)
        return SubmitSpeakingAnswerResponse(
            original_answer=analysis.get("original_answer", original_answer),
            is_correct=False,
            score=analysis.get("score", 70.0),
            mistakes=analysis.get("mistakes", []),
            corrected_sentence=analysis.get("corrected_sentence", original_answer),
            simple_explanation=analysis.get("simple_explanation", ""),
            natural_expression=analysis.get("natural_expression", ""),
            additional_examples=analysis.get("additional_examples", []),
            encouragement=analysis.get("encouragement", ""),
            attempt_id=attempt.id,
            repetition_required=True,
            repetitions_completed=0,
            repetitions_required=2,
            item_completed=False,
            session_completed=False,
            completed_count=session.completed_count,
            daily_target=session.daily_target,
            next_situation=None,
            streak_info=None,
        )

    @staticmethod
    async def evaluate_session_repeat(
        db: Session,
        user: User,
        session_id: int,
        attempt_id: int,
        repeated_sentence: str,
    ) -> RepeatSpeakingAnswerResponse:
        session = (
            db.query(SpeakingSession)
            .filter(SpeakingSession.id == session_id, SpeakingSession.user_id == user.id)
            .first()
        )
        if not session:
            raise HTTPException(status_code=404, detail="Speaking session not found")
        if session.status != "active":
            raise HTTPException(status_code=400, detail="Session already completed")

        attempt = (
            db.query(PracticeAttempt)
            .filter(
                PracticeAttempt.id == attempt_id,
                PracticeAttempt.session_id == session.id,
                PracticeAttempt.user_id == user.id,
            )
            .first()
        )
        if not attempt:
            raise HTTPException(status_code=404, detail="Attempt record not found")
        if attempt.item_completed:
            raise HTTPException(status_code=400, detail="This situation is already completed.")

        prev_mistake = attempt.mistakes_json[0].get("explanation") if attempt.mistakes_json else None
        result = await ai_service.evaluate_repeat(
            target_sentence=attempt.corrected_sentence,
            repeated_sentence=repeated_sentence,
            previous_mistake=prev_mistake,
        )

        # Also accept matching natural_expression gracefully
        if not result.get("is_successful") and attempt.natural_expression:
            nat_res = await ai_service.evaluate_repeat(
                target_sentence=attempt.natural_expression,
                repeated_sentence=repeated_sentence,
                previous_mistake=prev_mistake,
            )
            if nat_res.get("is_successful"):
                result = nat_res

        is_ok = bool(result.get("is_successful", False))
        history = list(attempt.repetition_history_json or [])
        history.append({
            "attempt_text": repeated_sentence.strip(),
            "is_successful": is_ok,
            "accuracy": result.get("accuracy_score", 0.0),
        })
        attempt.repetition_history_json = history

        if not is_ok:
            db.commit()
            return RepeatSpeakingAnswerResponse(
                attempt_id=attempt.id,
                is_successful=False,
                accuracy_score=result.get("accuracy_score", 0.0),
                feedback=result.get("feedback", f"Please repeat: {attempt.corrected_sentence}"),
                remaining_mistake=result.get("remaining_mistake"),
                next_action="try_again",
                encouragement="Take your time and repeat the corrected response clearly.",
                repetitions_completed=attempt.repetition_success_count,
                repetitions_required=2,
                item_completed=False,
                session_completed=False,
                completed_count=session.completed_count,
                daily_target=session.daily_target,
                next_situation=None,
                streak_info=None,
            )

        attempt.repetition_success_count += 1

        if attempt.repetition_success_count < 2:
            db.commit()
            return RepeatSpeakingAnswerResponse(
                attempt_id=attempt.id,
                is_successful=True,
                accuracy_score=result.get("accuracy_score", 95.0),
                feedback="First repetition (1/2) succeeded! Please repeat the corrected sentence one more time (2/2).",
                remaining_mistake=None,
                next_action="repeat_second_time",
                encouragement="Great job! One more repetition to go!",
                repetitions_completed=attempt.repetition_success_count,
                repetitions_required=2,
                item_completed=False,
                session_completed=False,
                completed_count=session.completed_count,
                daily_target=session.daily_target,
                next_situation=None,
                streak_info=None,
            )

        # Both 2/2 repetitions succeeded -> complete item and resolve mistakes!
        attempt.repeated_correctly = True
        attempt.item_completed = True

        daily_progress = db.query(Progress).filter(
            Progress.user_id == user.id, Progress.date == session.local_date
        ).first()
        if daily_progress:
            daily_progress.situations_completed += 1

        if attempt.situation_id:
            mistakes = db.query(Mistake).filter(
                Mistake.user_id == user.id, Mistake.situation_id == attempt.situation_id
            ).all()
            for m in mistakes:
                m.is_resolved = True

        adv = SituationService._complete_speaking_item_and_advance(db, user, session, attempt.situation_id)

        return RepeatSpeakingAnswerResponse(
            attempt_id=attempt.id,
            is_successful=True,
            accuracy_score=result.get("accuracy_score", 98.0),
            feedback="Excellent! Both repetitions (2/2) completed accurately!",
            remaining_mistake=None,
            next_action="next_situation",
            encouragement="You've mastered this situation!",
            repetitions_completed=2,
            repetitions_required=2,
            item_completed=True,
            session_completed=adv["session_completed"],
            completed_count=session.completed_count,
            daily_target=session.daily_target,
            next_situation=adv["next_situation"],
            streak_info=adv["streak_info"],
        )


situation_service = SituationService()
