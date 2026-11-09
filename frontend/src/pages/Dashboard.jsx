import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTutor } from '../context/TutorContext';
import { progressAPI, situationsAPI, learningAPI } from '../services/api';
import { RobotTutor } from '../components/RobotTutor';
import { DifficultyBadge } from '../components/DifficultyBadge';
import {
  Flame, Award, ArrowRight, Play, CheckCircle2, AlertOctagon,
  TrendingUp, Sparkles, Clock, Target, Calendar
} from 'lucide-react';

export function Dashboard() {
  const { user, profile } = useAuth();
  const { setRobotState } = useTutor();
  const navigate = useNavigate();

  const [stats, setStats] = useState(null);
  const [dailyChallenge, setDailyChallenge] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setRobotState(
      'GREETING',
      `Welcome back${user?.full_name ? `, ${user.full_name}` : ''}! Ready to practice your spoken English today?`
    );

    const loadData = async () => {
      try {
        const [statsRes, challengesRes] = await Promise.all([
          progressAPI.getStats(),
          learningAPI.getDailyChallenges(),
        ]);
        setStats(statsRes.data);
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
  const dailyGoal = profile?.daily_goal_minutes || stats?.daily_goal_minutes || 20;
  const practicedToday = stats?.minutes_practiced_today || 0;
  const goalPercent = Math.min(100, Math.round((practicedToday / dailyGoal) * 100));

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
            Practice real-life English speaking situations today. Get instant feedback on grammar, sentence formation, and natural expression.
          </p>

          <div className="hero-actions">
            <Link to="/situations" className="btn-primary-action">
              <Play size={18} />
              <span>Start Situation Practice</span>
              <ArrowRight size={18} />
            </Link>
            <Link to="/conversation" className="btn-secondary-action">
              <span>Talk in AI Conversation Room</span>
            </Link>
          </div>
        </div>

        <div className="hero-robot-wrapper">
          <RobotTutor size="large" showMessage={true} />
        </div>
      </div>

      {/* Quick Metrics Bar */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon bg-blue">
            <Target size={22} />
          </div>
          <div className="metric-details">
            <span className="metric-label">Current Level</span>
            <div className="metric-val-row">
              <DifficultyBadge level={currentLevel} />
            </div>
            <span className="metric-subtext">Adapts automatically to performance</span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon bg-orange">
            <Flame size={22} />
          </div>
          <div className="metric-details">
            <span className="metric-label">Daily Streak</span>
            <span className="metric-val">{profile?.streak_count || 1} Days</span>
            <span className="metric-subtext">Practice daily to keep streak</span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon bg-green">
            <Clock size={22} />
          </div>
          <div className="metric-details">
            <span className="metric-label">Daily Practice Goal</span>
            <span className="metric-val">{practicedToday} / {dailyGoal} mins</span>
            <div className="goal-progress-bar">
              <div className="goal-fill" style={{ width: `${goalPercent}%` }} />
            </div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon bg-purple">
            <Award size={22} />
          </div>
          <div className="metric-details">
            <span className="metric-label">Total Points</span>
            <span className="metric-val">{profile?.total_points || 120} pts</span>
            <span className="metric-subtext">{stats?.total_situations_completed || 0} situations completed</span>
          </div>
        </div>
      </div>

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
