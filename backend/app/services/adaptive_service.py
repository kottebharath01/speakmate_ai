from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.entities import LearningProfile, PracticeAttempt, Mistake, User

LEVEL_PROGRESSION = ["BEGINNER", "INTERMEDIATE", "ADVANCED"]

class AdaptiveDifficultyEngine:
    """
    Intelligent adaptive difficulty engine.
    - Evaluates rolling performance across last 5 attempts.
    - Promotes to next level when recent average >= 85% and at least 3 consecutive high-scoring attempts.
    - Demotes only if last 4 consecutive attempts score < 50%, to avoid discouraging the learner after an isolated mistake.
    - Detects recurring mistakes by category to recommend targeted practice.
    """

    @staticmethod
    def evaluate_level_progression(db: Session, user_id: int) -> Dict[str, Any]:
        profile = db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()
        if not profile:
            return {"current_level": "BEGINNER", "level_changed": False, "reason": "No profile found"}

        current_level = profile.current_level or "BEGINNER"
        recent_attempts = (
            db.query(PracticeAttempt)
            .filter(PracticeAttempt.user_id == user_id)
            .order_by(PracticeAttempt.created_at.desc())
            .limit(5)
            .all()
        )

        if len(recent_attempts) < 3:
            return {
                "current_level": current_level,
                "level_changed": False,
                "reason": f"Need at least 3 practice attempts to evaluate progression (currently {len(recent_attempts)})."
            }

        scores = [a.score for a in recent_attempts]
        avg_score = sum(scores) / len(scores)
        
        # Check promotion condition: current average >= 82 and last 3 attempts >= 80
        curr_idx = LEVEL_PROGRESSION.index(current_level) if current_level in LEVEL_PROGRESSION else 0
        
        if avg_score >= 82 and all(s >= 80 for s in scores[:3]):
            if curr_idx < len(LEVEL_PROGRESSION) - 1:
                new_level = LEVEL_PROGRESSION[curr_idx + 1]
                profile.current_level = new_level
                db.commit()
                return {
                    "current_level": new_level,
                    "previous_level": current_level,
                    "level_changed": True,
                    "reason": f"Congratulations! Your consistent high performance (average score {round(avg_score, 1)}%) has unlocked {new_level} level!"
                }

        # Demotion condition: only if last 4 attempts are consistently < 50%
        if len(scores) >= 4 and all(s < 50 for s in scores[:4]):
            if curr_idx > 0:
                new_level = LEVEL_PROGRESSION[curr_idx - 1]
                profile.current_level = new_level
                db.commit()
                return {
                    "current_level": new_level,
                    "previous_level": current_level,
                    "level_changed": True,
                    "reason": f"Let's reinforce the fundamentals. Difficulty temporarily adjusted to {new_level}."
                }

        return {
            "current_level": current_level,
            "level_changed": False,
            "average_score": round(avg_score, 1),
            "reason": f"Performance is steady at {current_level} level with {round(avg_score, 1)}% average score."
        }

    @staticmethod
    def get_recurring_mistakes_analysis(db: Session, user_id: int) -> Dict[str, Any]:
        """Identify mistake categories that need targeted revision."""
        mistakes = db.query(Mistake).filter(Mistake.user_id == user_id).all()
        
        category_counts: Dict[str, int] = {}
        for m in mistakes:
            category_counts[m.category] = category_counts.get(m.category, 0) + m.repetition_count

        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        recommended_lessons = []
        
        for cat, count in sorted_categories:
            if cat in ("tense", "grammar"):
                recommended_lessons.append("Tenses Mastery: Simple Present vs Present Continuous")
            elif cat in ("article"):
                recommended_lessons.append("Articles: A, An, and The Made Crystal Clear")
            elif cat in ("subject_verb"):
                recommended_lessons.append("Subject-Verb Agreement")
            elif cat in ("preposition"):
                recommended_lessons.append("Prepositions of Time and Place")

        return {
            "total_mistakes": len(mistakes),
            "category_breakdown": category_counts,
            "top_weakness": sorted_categories[0][0] if sorted_categories else None,
            "recommended_lessons": list(dict.fromkeys(recommended_lessons))[:3]
        }

adaptive_engine = AdaptiveDifficultyEngine()
