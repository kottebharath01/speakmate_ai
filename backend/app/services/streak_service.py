from datetime import date, datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.entities import DailyActivity, LearningProfile


def parse_local_date(local_date_str: Optional[str]) -> date:
    """Safely parse YYYY-MM-DD local date string, defaulting to UTC/server today."""
    if local_date_str:
        try:
            return datetime.strptime(local_date_str.strip()[:10], "%Y-%m-%d").date()
        except ValueError:
            pass
    return date.today()


class StreakService:
    """
    Beginner-friendly service managing daily learning streaks and activity calendar.
    Follows strict rules:
    - Only completing a full learning session marks a calendar day as active.
    - Completing both modules on the same day counts as ONE streak day.
    - Missing one complete calendar day resets current_streak to 0 (next completed day starts at Day 1).
    - longest_streak is always preserved across resets.
    """

    @staticmethod
    def calculate_streaks(db: Session, user_id: int, reference_date_str: Optional[str] = None) -> Dict[str, Any]:
        ref_date = parse_local_date(reference_date_str)

        # Fetch all active learning dates for this user where at least 1 session was completed
        activities = (
            db.query(DailyActivity)
            .filter(
                DailyActivity.user_id == user_id,
                (DailyActivity.words_sessions_completed + DailyActivity.speaking_sessions_completed) > 0,
            )
            .order_by(DailyActivity.activity_date.asc())
            .all()
        )

        active_date_objs = []
        active_date_map: Dict[str, DailyActivity] = {}
        for act in activities:
            try:
                d = datetime.strptime(act.activity_date, "%Y-%m-%d").date()
                # Ignore future dates beyond ref_date when evaluating against a simulated/reference date
                if d <= ref_date:
                    active_date_objs.append(d)
                    active_date_map[act.activity_date] = act
            except ValueError:
                continue

        active_set = set(active_date_objs)

        # 1. Calculate current_streak relative to ref_date
        current_streak = 0
        if ref_date in active_set:
            cursor = ref_date
            while cursor in active_set:
                current_streak += 1
                cursor -= timedelta(days=1)
        elif (ref_date - timedelta(days=1)) in active_set:
            # Today isn't finished yet, but yesterday was completed so streak is still alive
            cursor = ref_date - timedelta(days=1)
            while cursor in active_set:
                current_streak += 1
                cursor -= timedelta(days=1)
        else:
            # Missed at least one complete calendar day -> reset to 0
            current_streak = 0

        # 2. Calculate historical longest run from all active dates
        historical_max = 0
        if active_date_objs:
            sorted_dates = sorted(active_set)
            run = 1
            historical_max = 1
            for i in range(1, len(sorted_dates)):
                if sorted_dates[i] == sorted_dates[i - 1] + timedelta(days=1):
                    run += 1
                    if run > historical_max:
                        historical_max = run
                else:
                    run = 1

        profile = db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()
        stored_longest = profile.longest_streak if (profile and profile.longest_streak) else 0
        longest_streak = max(stored_longest, historical_max, current_streak)

        if profile:
            profile.streak_count = current_streak
            profile.longest_streak = longest_streak
            db.commit()

        today_act = active_date_map.get(ref_date.isoformat())
        calendar_days = [
            {
                "date": d_str,
                "words_sessions": act.words_sessions_completed,
                "speaking_sessions": act.speaking_sessions_completed,
                "total_sessions": act.words_sessions_completed + act.speaking_sessions_completed,
            }
            for d_str, act in sorted(active_date_map.items())
        ]

        return {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "completed_days_count": len(active_set),
            "reference_date": ref_date.isoformat(),
            "today_completed": ref_date in active_set,
            "words_completed_today": today_act.words_sessions_completed if today_act else 0,
            "speaking_completed_today": today_act.speaking_sessions_completed if today_act else 0,
            "active_dates": sorted(list(active_date_map.keys())),
            "calendar_days": calendar_days,
        }

    @staticmethod
    def record_session_completion(
        db: Session,
        user_id: int,
        module_name: str,
        local_date_str: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Records a completed full session for 'words' or 'speaking' on local_date_str.
        Updates DailyActivity and recalculates user's streak safely.
        """
        activity_date = parse_local_date(local_date_str)
        date_str = activity_date.isoformat()

        activity = (
            db.query(DailyActivity)
            .filter(DailyActivity.user_id == user_id, DailyActivity.activity_date == date_str)
            .first()
        )
        if not activity:
            activity = DailyActivity(
                user_id=user_id,
                activity_date=date_str,
                words_sessions_completed=0,
                speaking_sessions_completed=0,
            )
            db.add(activity)

        if module_name == "words":
            activity.words_sessions_completed += 1
        elif module_name == "speaking":
            activity.speaking_sessions_completed += 1

        profile = db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()
        if profile:
            profile.last_practice_date = datetime.utcnow()

        db.commit()
        return StreakService.calculate_streaks(db, user_id, date_str)


streak_service = StreakService()
