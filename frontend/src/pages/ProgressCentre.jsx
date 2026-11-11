import React, { useState, useEffect } from 'react';
import { progressAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useTutor } from '../context/TutorContext';
import { DifficultyBadge } from '../components/DifficultyBadge';
import { StreakCalendar } from '../components/StreakCalendar';
import {
  TrendingUp, Clock, CheckCircle2, AlertOctagon, Award, Flame,
  BarChart3, Calendar, Layers, ShieldCheck, Languages
} from 'lucide-react';

export function ProgressCentre() {
  const { profile } = useAuth();
  const { setRobotState } = useTutor();
  const [stats, setStats] = useState(null);
  const [streakData, setStreakData] = useState(null);
  const [progressRecords, setProgressRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setRobotState('SUCCESS', 'Track your fluency growth! Consistent practice leads to natural confidence.');

    const loadProgress = async () => {
      try {
        const [statsRes, streakRes, recordsRes] = await Promise.all([
          progressAPI.getStats(),
          progressAPI.getStreak(),
          progressAPI.getRecords(),
        ]);
        setStats(statsRes.data);
        setStreakData(streakRes.data);
        setProgressRecords(recordsRes.data);
      } catch (err) {
        console.warn('Progress fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    loadProgress();
  }, [setRobotState]);

  const currentLevel = profile?.current_level || stats?.current_level || 'BEGINNER';
  const totalCompleted = stats?.total_situations_completed || 0;
  const wordsCompleted = stats?.words_completed_count || 0;
  const totalMistakes = stats?.total_mistakes_tracked || 0;
  const resolvedMistakes = stats?.total_mistakes_resolved || 0;
  const resolutionRate = totalMistakes > 0 ? Math.round((resolvedMistakes / totalMistakes) * 100) : 100;
  const currentStreak = streakData?.current_streak ?? stats?.streak_count ?? profile?.streak_count ?? 0;

  return (
    <div className="progress-centre-page">
      <div className="page-header-row">
        <div>
          <h2>English Learning Progress Centre</h2>
          <p className="subtitle">
            Independent tracking for Words & Expressions and Speaking Practice sessions.
          </p>
        </div>
      </div>

      {/* KPI Overview Grid */}
      <div className="progress-kpi-grid">
        <div className="kpi-card">
          <div className="kpi-icon bg-blue">
            <Languages size={22} />
          </div>
          <div className="kpi-info">
            <span className="kpi-title">Words & Expressions</span>
            <span className="kpi-value">{wordsCompleted}</span>
            <span className="kpi-note">{stats?.words_sessions_completed || 0} sessions completed</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon bg-green">
            <CheckCircle2 size={22} />
          </div>
          <div className="kpi-info">
            <span className="kpi-title">Speaking Practice</span>
            <span className="kpi-value">{totalCompleted}</span>
            <span className="kpi-note">{stats?.speaking_sessions_completed || 0} sessions completed</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon bg-orange">
            <Flame size={22} />
          </div>
          <div className="kpi-info">
            <span className="kpi-title">Streak & Points</span>
            <span className="kpi-value">{currentStreak} Days / {profile?.total_points ?? 0} pts</span>
            <span className="kpi-note">Longest: {streakData?.longest_streak ?? 0} Days</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon bg-purple">
            <AlertOctagon size={22} />
          </div>
          <div className="kpi-info">
            <span className="kpi-title">Mistakes Resolved</span>
            <span className="kpi-value">{resolutionRate}%</span>
            <span className="kpi-note">{resolvedMistakes} of {totalMistakes} corrected</span>
          </div>
        </div>
      </div>

      <StreakCalendar streakData={streakData} />

      {/* Weekly Progress Breakdown Chart */}
      <div className="progress-chart-card">
        <div className="chart-header">
          <div className="chart-title-group">
            <BarChart3 size={18} className="text-blue" />
            <h3>Weekly Speaking Performance & Accuracy</h3>
          </div>
          <span className="accuracy-legend">Grammar & Structure Accuracy %</span>
        </div>

        <div className="chart-bars-wrap">
          {stats?.weekly_accuracy_trend?.map((item, idx) => (
            <div key={idx} className="chart-bar-item">
              <div className="bar-track">
                <div
                  className="bar-fill"
                  style={{ height: `${Math.max(15, item.accuracy)}%` }}
                >
                  <span className="bar-tooltip">{item.accuracy}%</span>
                </div>
              </div>
              <span className="bar-day">{item.day}</span>
              <span className="bar-date">{item.date.slice(5)}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Accuracy Diagnostics Breakdown */}
      <div className="diagnostics-grid">
        <div className="diagnostic-card">
          <h4>Grammar & Sentence Formation</h4>
          <p className="diag-desc">
            Evaluates verb tenses, subject-verb agreement, and structural completeness of sentences.
          </p>
          <div className="diag-bar-row">
            <div className="diag-bar-track">
              <div className="diag-bar-fill fill-blue" style={{ width: '85%' }} />
            </div>
            <span className="diag-score">85%</span>
          </div>
        </div>

        <div className="diagnostic-card">
          <h4>Vocabulary Selection & Relevance</h4>
          <p className="diag-desc">
            Checks natural vocabulary usage and relevance to the specific real-life scenario.
          </p>
          <div className="diag-bar-row">
            <div className="diag-bar-track">
              <div className="diag-bar-fill fill-green" style={{ width: '82%' }} />
            </div>
            <span className="diag-score">82%</span>
          </div>
        </div>

        <div className="diagnostic-card">
          <h4>Sentence Flow & Repeat Accuracy</h4>
          <p className="diag-desc">
            Measures your retention and repetition of corrected native expressions.
          </p>
          <div className="diag-bar-row">
            <div className="diag-bar-track">
              <div className="diag-bar-fill fill-purple" style={{ width: '88%' }} />
            </div>
            <span className="diag-score">88%</span>
          </div>
        </div>
      </div>

      <div className="pedagogical-disclaimer">
        <p>
          <strong>Note on Spoken Evaluation:</strong> SpeakMate AI evaluates sentence structure, grammar, vocabulary, and communication clarity from recognized English transcripts. Acoustic pitch and phonemic pronunciation accuracy are not measured from text alone.
        </p>
      </div>
    </div>
  );
}
