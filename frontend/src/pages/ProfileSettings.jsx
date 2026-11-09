import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { profileAPI } from '../services/api';
import { DifficultyBadge } from '../components/DifficultyBadge';
import {
  User, Settings, Save, CheckCircle2, Cpu, HardDrive, HelpCircle,
  Clock, Target, ShieldCheck
} from 'lucide-react';

export function ProfileSettings() {
  const { user, profile, refreshProfile } = useAuth();

  const [fullName, setFullName] = useState('');
  const [currentLevel, setCurrentLevel] = useState('BEGINNER');
  const [dailyGoalMinutes, setDailyGoalMinutes] = useState(20);
  const [targetFocus, setTargetFocus] = useState('Spoken English & Real Situations');
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (user) {
      setFullName(user.full_name || '');
    }
    if (profile) {
      setCurrentLevel(profile.current_level || 'BEGINNER');
      setDailyGoalMinutes(profile.daily_goal_minutes || 20);
      setTargetFocus(profile.target_focus || 'Spoken English & Real Situations');
    }
  }, [user, profile]);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSavedSuccess(false);

    try {
      await profileAPI.update({
        full_name: fullName,
        current_level: currentLevel,
        daily_goal_minutes: Number(dailyGoalMinutes),
        target_focus: targetFocus,
      });
      await refreshProfile();
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err) {
      console.error('Failed to update profile:', err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="profile-settings-page">
      <div className="page-header-row">
        <div>
          <h2>Profile & Learning Settings</h2>
          <p className="subtitle">Customize your learning pace, target focus, and AI tutor preferences.</p>
        </div>
      </div>

      <div className="settings-layout-grid">
        {/* Left Column: Form Settings */}
        <div className="settings-card-col">
          <form onSubmit={handleSave} className="settings-form-card">
            <h3 className="form-card-title">
              <User size={18} className="text-blue" />
              <span>Learner Profile</span>
            </h3>

            {savedSuccess && (
              <div className="save-success-banner">
                <CheckCircle2 size={16} />
                <span>Profile settings saved successfully!</span>
              </div>
            )}

            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                className="form-control"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Enter your name"
              />
            </div>

            <div className="form-group">
              <label>Current Difficulty Level</label>
              <select
                className="form-control"
                value={currentLevel}
                onChange={(e) => setCurrentLevel(e.target.value)}
              >
                <option value="BEGINNER">Beginner (Daily life, simple sentences)</option>
                <option value="INTERMEDIATE">Intermediate (Workplace, descriptive conversation)</option>
                <option value="ADVANCED">Advanced (Job interviews, professional presentations)</option>
              </select>
              <span className="field-hint">
                SpeakMate's adaptive engine also automatically adjusts this based on your performance.
              </span>
            </div>

            <div className="form-group">
              <label>Daily Speaking Practice Goal (Minutes)</label>
              <input
                type="number"
                min="5"
                max="120"
                className="form-control"
                value={dailyGoalMinutes}
                onChange={(e) => setDailyGoalMinutes(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Primary Learning Target</label>
              <input
                type="text"
                className="form-control"
                value={targetFocus}
                onChange={(e) => setTargetFocus(e.target.value)}
                placeholder="e.g. Spoken English, Job Interview, Office Communication"
              />
            </div>

            <button type="submit" className="btn-save-settings" disabled={saving}>
              <Save size={16} />
              <span>{saving ? 'Saving...' : 'Save Changes'}</span>
            </button>
          </form>
        </div>

        {/* Right Column: AI Tutor & Ollama Guidance */}
        <div className="settings-info-col">
          <div className="ai-status-card">
            <div className="card-top-icon">
              <Cpu size={24} className="text-blue" />
              <h4>AI Tutor Architecture</h4>
            </div>
            <p className="ai-status-desc">
              SpeakMate AI is designed with an interchangeable AI engine architecture:
            </p>

            <div className="ai-engine-checklist">
              <div className="engine-item active">
                <CheckCircle2 size={16} className="text-green" />
                <div>
                  <strong>Built-in Intelligent English NLP Engine (Active)</strong>
                  <p>Analyzes grammar, tenses, subject-verb agreement, and articles with instant zero-latency feedback.</p>
                </div>
              </div>

              <div className="engine-item">
                <HardDrive size={16} className="text-blue" />
                <div>
                  <strong>Ollama Local Model Integration (Optional)</strong>
                  <p>Connects automatically to Ollama at <code>http://localhost:11434</code> with Qwen / Llama models when running.</p>
                </div>
              </div>
            </div>

            {/* Quick Ollama Setup Guide */}
            <div className="ollama-guide-box">
              <div className="guide-title">
                <HelpCircle size={15} /> How to run Ollama locally (Optional):
              </div>
              <ol className="guide-steps">
                <li>Download Ollama from <code>https://ollama.com</code>.</li>
                <li>Run in terminal: <code>ollama run qwen2.5:3b</code></li>
                <li>SpeakMate AI automatically detects and uses your local model!</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
