import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTutor } from '../context/TutorContext';
import { progressAPI, situationsAPI, learningAPI } from '../services/api';
import { RobotTutor } from '../components/RobotTutor';
import { DifficultyBadge } from '../components/DifficultyBadge';
import { StreakCalendar } from '../components/StreakCalendar';
import {
  Flame, Award, ArrowRight, Play, CheckCircle2, AlertOctagon,
  TrendingUp, Sparkles, Clock, Target, Calendar, Languages, MessageSquareText
} from 'lucide-react';

export function Dashboard() {
  const { user, profile } = useAuth();
  const { setRobotState } = useTutor();
  const navigate = useNavigate();

  const [stats, setStats] = useState(null);
  const [streakData, setStreakData] = useState(null);
  const [dailyChallenge, setDailyChallenge] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setRobotState(
      'GREETING',
      `Welcome back${user?.full_name ? `, ${user.full_name}` : ''}! Choose Words & Expressions or Speaking Practice today.`
    );

    const loadData = async () => {
      try {
        const [statsRes, streakRes, challengesRes] = await Promise.all([
          progressAPI.getStats(),
          progressAPI.getStreak(),
          learningAPI.getDailyChallenges(),
        ]);
        setStats(statsRes.data);
        setStreakData(streakRes.data);
        if (challengesRes.data && challengesRes.data.length > 0) {
          setDailyChallenge(challengesRes.data[0]);
        }
      } catch (err) {
        console.warn('Dashboard data fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [user, setRobotState]);

  const currentLevel = profile?.current_level || stats?.current_level || 'BEGINNER';
  const dailyGoal = profile?.daily_goal_minutes || stats?.daily_goal_minutes || 15;
  const practicedToday = stats?.minutes_practiced_today || 0;
  const goalPercent = Math.min(100, Math.round((practicedToday / dailyGoal) * 100));
  const currentStreak = streakData?.current_streak ?? stats?.streak_count ?? profile?.streak_count ?? 0;
  const longestStreak = streakData?.longest_streak ?? stats?.longest_streak ?? profile?.longest_streak ?? 0;

  return (
    <div className="dashboard-page">
      {/* Hero Welcome Banner with Robot Character */}
      <div className="hero-banner">
        <div className="hero-text-content">
          <div className="hero-badge">
            <Sparkles size={14} />
            <span>AI English Tutor Ready</span>
          </div>
          <h1 className="hero-title">
            Hello, <span className="highlight-name">{user?.full_name || user?.username || 'Learner'}</span>!
          </h1>
          <p className="hero-subtitle">
            Build confidence step-by-step through two independent guided learning modules led by your AI Tutor.
          </p>

          <div className="hero-actions">
            <Link to="/words-expressions" className="btn-primary-action">
              <Languages size={18} />
              <span>Words & Expressions</span>
              <ArrowRight size={18} />
            </Link>
            <Link to="/situations" className="btn-secondary-action">
              <MessageSquareText size={18} />
              <span>Speaking Practice</span>
              <ArrowRight size={18} />
            </Link>
          </div>
        </div>

        <div className="hero-robot-wrapper">
          <RobotTutor size="large" showMessage={true} />
        </div>
      </div>

      {/* Quick Metrics Bar (Strict Independent Module Metrics) */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon bg-blue">
            <Languages size={22} />
          </div>
          <div className="metric-details">
            <span className="metric-label">Words & Expressions</span>
            <span className="metric-val">{stats?.words_completed_count ?? 0} Learned</span>
            <span className="metric-subtext">{stats?.words_sessions_completed ?? 0} sessions completed</span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon bg-green">
            <MessageSquareText size={22} />
          </div>
          <div className="metric-details">
            <span className="metric-label">Speaking Practice</span>
            <span className="metric-val">{stats?.total_situations_completed ?? 0} Situations</span>
            <span className="metric-subtext">{stats?.speaking_sessions_completed ?? 0} sessions completed</span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon bg-orange">
            <Flame size={22} />
          </div>
          <div className="metric-details">
            <span className="metric-label">Daily Streak</span>
            <span className="metric-val">{currentStreak} Days</span>
            <span className="metric-subtext">Longest: {longestStreak} Days</span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon bg-purple">
            <Award size={22} />
          </div>
          <div className="metric-details">
            <span className="metric-label">Level & Points</span>
            <span className="metric-val">{profile?.total_points ?? stats?.total_points ?? 0} pts</span>
            <div className="metric-val-row" style={{ marginTop: '4px' }}>
              <DifficultyBadge level={currentLevel} />
            </div>
          </div>
        </div>
      </div>

      {/* Daily Streak Activity Calendar */}
      <StreakCalendar streakData={streakData} />

      {/* Main Content Split: Daily Challenge & Mistake Journal Overview */}
      <div className="dashboard-columns-grid">
        {/* Left Column: Daily Challenge */}
        <div className="dashboard-col">
          <div className="card-box challenge-box">
            <div className="card-box-header">
              <div className="header-title-group">
                <Calendar size={18} className="text-blue" />
                <h3>Today's Speaking Challenge</h3>
              </div>
              <span className="points-tag">+{dailyChallenge?.points || 25} pts</span>
            </div>

            {dailyChallenge && (
              <div className="challenge-body">
                <h4 className="challenge-title">{dailyChallenge.title}</h4>
                <p className="challenge-desc">{dailyChallenge.description}</p>
                <div className="challenge-telugu-hint">
                  <span className="telugu-label">తెలుగు వివరణ:</span>
                  <p>{dailyChallenge.telugu_context}</p>
                </div>
                <div className="challenge-prompt">
                  <strong>Speaking Prompt:</strong> {dailyChallenge.speaking_prompt}
                </div>
                <Link to="/challenges" className="btn-start-challenge">
                  <span>Take Daily Challenge</span>
                  <ArrowRight size={16} />
                </Link>
              </div>
            )}
          </div>

          {/* Weekly Accuracy Trend */}
          <div className="card-box">
            <div className="card-box-header">
              <div className="header-title-group">
                <TrendingUp size={18} className="text-purple" />
                <h3>Weekly Performance Trend</h3>
              </div>
              <Link to="/progress" className="view-all-link">Full Analytics</Link>
            </div>
            <div className="weekly-bars-container">
              {stats?.weekly_accuracy_trend?.map((day, idx) => (
                <div key={idx} className="trend-bar-col">
                  <div className="trend-bar-track">
                    <div
                      className="trend-bar-fill"
                      style={{ height: `${Math.max(10, day.accuracy)}%` }}
                      title={`${day.date}: ${day.accuracy}% accuracy (${day.situations} situations)`}
                    />
                  </div>
                  <span className="trend-bar-label">{day.day}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Mistake Journal Recent Items */}
        <div className="dashboard-col">
          <div className="card-box">
            <div className="card-box-header">
              <div className="header-title-group">
                <AlertOctagon size={18} className="text-amber" />
                <h3>Recent Mistakes Tracked</h3>
              </div>
              <Link to="/mistakes" className="view-all-link">Mistake Journal</Link>
            </div>

            <div className="recent-mistakes-list">
              {stats?.recent_mistakes && stats.recent_mistakes.length > 0 ? (
                stats.recent_mistakes.map((m) => (
                  <div key={m.id} className="mini-mistake-card">
                    <div className="mini-mistake-header">
                      <span className="mistake-cat-pill">{m.category}</span>
                      <span className="repetition-badge">x{m.repetition_count}</span>
                    </div>
                    <div className="mini-mistake-diff">
                      <span className="incorrect-strike">{m.original_sentence}</span>
                      <ArrowRight size={14} className="arrow-diff" />
                      <span className="correct-highlight">{m.corrected_sentence}</span>
                    </div>
                    <p className="mini-mistake-expl">{m.explanation}</p>
                  </div>
                ))
              ) : (
                <div className="empty-state-notice">
                  <CheckCircle2 size={28} className="text-green" />
                  <p>No recurring mistakes currently tracked! Start practicing situations to test your speaking.</p>
                </div>
              )}
            </div>

            <div className="card-box-footer">
              <Link to="/situations" className="btn-card-link">
                <span>Practice a Situation Now</span>
                <ArrowRight size={16} />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
