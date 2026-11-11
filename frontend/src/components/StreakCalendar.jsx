import React from 'react';
import { Flame, Trophy, Calendar, CheckCircle2 } from 'lucide-react';
import { getLocalDateString } from '../utils/dateUtils';

/**
 * Displays Current Streak, Longest Streak, and a 28-day local activity calendar
 * showing completed learning days across Words & Expressions and Speaking Practice.
 */
export function StreakCalendar({ streakData }) {
  const currentStreak = streakData?.current_streak ?? 0;
  const longestStreak = streakData?.longest_streak ?? 0;
  const completedDaysCount = streakData?.completed_days_count ?? 0;
  const calendarDays = streakData?.calendar_days || [];

  const activityByDate = {};
  calendarDays.forEach((entry) => {
    activityByDate[entry.date] = entry;
  });

  // Build last 28 calendar days ending at user's local today
  const today = new Date();
  const daysList = [];
  for (let i = 27; i >= 0; i--) {
    const d = new Date(today.getFullYear(), today.getMonth(), today.getDate() - i);
    const dateKey = getLocalDateString(d);
    const record = activityByDate[dateKey];
    daysList.push({
      dateKey,
      dayNumber: d.getDate(),
      weekday: d.toLocaleDateString('en-US', { weekday: 'short' }),
      isToday: i === 0,
      isActive: Boolean(record && record.total_sessions > 0),
      wordsSessions: record?.words_sessions || 0,
      speakingSessions: record?.speaking_sessions || 0,
    });
  }

  return (
    <div className="streak-calendar-card">
      <div className="streak-summary-header">
        <div className="streak-headline">
          <Calendar size={20} className="text-blue" />
          <div>
            <h3>Daily Learning Streak & Activity</h3>
            <p className="streak-sub">Complete any full daily target session to earn a streak day</p>
          </div>
        </div>

        <div className="streak-counters-row">
          <div className="streak-stat-box current">
            <Flame size={20} className="flame-icon" />
            <div>
              <span className="s-val" data-testid="current-streak-value">{currentStreak} Days</span>
              <span className="s-lbl">Current Streak</span>
            </div>
          </div>

          <div className="streak-stat-box longest">
            <Trophy size={20} className="star-icon" />
            <div>
              <span className="s-val" data-testid="longest-streak-value">{longestStreak} Days</span>
              <span className="s-lbl">Longest Streak</span>
            </div>
          </div>

          <div className="streak-stat-box total-days">
            <CheckCircle2 size={20} className="text-green" />
            <div>
              <span className="s-val">{completedDaysCount} Days</span>
              <span className="s-lbl">Active Days</span>
            </div>
          </div>
        </div>
      </div>

      {/* 28-Day Visual Calendar Grid */}
      <div className="activity-calendar-grid">
        {daysList.map((day) => (
          <div
            key={day.dateKey}
            className={`calendar-day-cell ${day.isActive ? 'active-day' : ''} ${day.isToday ? 'today-cell' : ''}`}
            title={
              day.isActive
                ? `${day.dateKey}: Completed (${day.wordsSessions} Words, ${day.speakingSessions} Speaking)`
                : `${day.dateKey}: Not completed`
            }
          >
            <span className="cal-weekday">{day.weekday}</span>
            <span className="cal-num">{day.dayNumber}</span>
            {day.isActive && <span className="cal-dot" />}
          </div>
        ))}
      </div>

      <div className="calendar-legend">
        <span className="legend-item"><span className="legend-box inactive" /> Missed / Incomplete</span>
        <span className="legend-item"><span className="legend-box active" /> Completed Learning Day</span>
        <span className="legend-item"><span className="legend-box today" /> Today</span>
      </div>
    </div>
  );
}
