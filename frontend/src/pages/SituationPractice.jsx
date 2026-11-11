import React, { useState, useEffect, useRef } from 'react';
import { situationsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useTutor } from '../context/TutorContext';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';
import { useSpeechSynthesis } from '../hooks/useSpeechSynthesis';
import { RobotTutor } from '../components/RobotTutor';
import { VoiceInput } from '../components/VoiceInput';
import { FeedbackCard } from '../components/FeedbackCard';
import { DifficultyBadge } from '../components/DifficultyBadge';
import {
  Sparkles, Volume2, Globe, HelpCircle, Play, History,
  RefreshCw, ArrowRight, AlertTriangle, Lightbulb, Award,
  Flame, RotateCcw, Target
} from 'lucide-react';

const SPEAKING_TABS = [
  { id: 'session', label: 'AI Practice Session', icon: Play },
  { id: 'history', label: 'Practice History', icon: History },
];

const TARGET_PRESETS = [3, 5, 10];

export function SituationPractice() {
  const { refreshProfile } = useAuth();
  const { setRobotState, triggerCelebration } = useTutor();
  const { speak } = useSpeechSynthesis();

  const {
    transcript,
    setTranscript,
    isListening,
    startListening,
    stopListening,
    resetTranscript,
    error: speechError,
    isSupported,
  } = useSpeechRecognition();

  // Tab: 'session' | 'history'
  const [activeTab, setActiveTab] = useState('session');

  // Setup state
  const [categoryStats, setCategoryStats] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [dailyTarget, setDailyTarget] = useState(5);
  const [isRevision, setIsRevision] = useState(false);
  const [setupError, setSetupError] = useState('');
  const [startingSession, setStartingSession] = useState(false);

  // Active session state
  const [loading, setLoading] = useState(true);
  const [activeSession, setActiveSession] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [isEvaluatingRepeat, setIsEvaluatingRepeat] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [repeatResult, setRepeatResult] = useState(null);
  const [repetitionsCompleted, setRepetitionsCompleted] = useState(0);
  const [pendingNextData, setPendingNextData] = useState(null);
  const [showRomanized, setShowRomanized] = useState(false);
  const [completionInfo, setCompletionInfo] = useState(null);

  // History state
  const [historySessions, setHistorySessions] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [expandedSessionId, setExpandedSessionId] = useState(null);

  const autoAdvanceTimerRef = useRef(null);

  useEffect(() => {
    return () => {
      if (autoAdvanceTimerRef.current) clearTimeout(autoAdvanceTimerRef.current);
    };
  }, []);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      const [statsRes, activeRes] = await Promise.all([
        situationsAPI.getCategoryStats(),
        situationsAPI.getActiveSession(),
      ]);
      setCategoryStats(statsRes.data || []);

      if (activeRes.data && activeRes.data.status === 'active') {
        const sess = activeRes.data;
        setActiveSession(sess);

        if (sess.pending_attempt) {
          const pa = sess.pending_attempt;
          setFeedback({
            attempt_id: pa.id,
            original_answer: pa.original_answer,
            is_correct: false,
            score: pa.score,
            mistakes: pa.mistakes_json || [],
            corrected_sentence: pa.corrected_sentence,
            simple_explanation: pa.explanation || '',
            natural_expression: pa.natural_expression || '',
            additional_examples: pa.examples_json || [],
            encouragement: 'Let’s complete the repetitions cleanly!',
          });
          setRepetitionsCompleted(pa.repetition_success_count || 0);
          setRobotState(
            'TEACHING',
            `Welcome back! Please repeat the improved sentence (${pa.repetition_success_count || 0}/2 completed).`
          );
        } else if (sess.current_situation) {
          setFeedback(null);
          setRepetitionsCompleted(0);
          setRobotState(
            'EXPLAINING',
            `Listen to this situation in Telugu, then answer: "${sess.current_situation.english_prompt}"`
          );
        }
      } else {
        setActiveSession(null);
        setRobotState(
          'GREETING',
          'Select a category and set how many situations you want to practice today!'
        );
      }
    } catch (err) {
      console.warn('Failed to initialize Speaking Practice:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadHistory = async () => {
    setLoadingHistory(true);
    try {
      const res = await situationsAPI.getSessionHistory();
      setHistorySessions(res.data || []);
    } catch (err) {
      console.warn('Failed to load speaking practice history:', err);
    } finally {
      setLoadingHistory(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'history') {
      loadHistory();
    }
  }, [activeTab]);

  // Sync robot listening indicator
  useEffect(() => {
    if (isListening) {
      setRobotState('LISTENING', "I'm listening to your English response. Speak clearly!");
    }
  }, [isListening, setRobotState]);

  // Calculate eligible count for setup form
  const totalAvailableAll = categoryStats.reduce((sum, c) => sum + c.total_count, 0);
  const remainingNewAll = categoryStats.reduce((sum, c) => sum + c.remaining_new_count, 0);
  const selectedCatObj = categoryStats.find((c) => c.name === selectedCategory);
  const eligibleCountForSelection = isRevision
    ? (selectedCategory === 'All'
        ? totalAvailableAll - remainingNewAll
        : (selectedCatObj ? selectedCatObj.total_count - selectedCatObj.remaining_new_count : 0))
    : (selectedCategory === 'All'
        ? remainingNewAll
        : (selectedCatObj?.remaining_new_count ?? 0));

  const handleStartSession = async (e) => {
    e.preventDefault();
    setSetupError('');
    setCompletionInfo(null);
    setFeedback(null);
    setRepeatResult(null);
    setRepetitionsCompleted(0);
    setPendingNextData(null);
    resetTranscript();

    const targetNum = parseInt(dailyTarget, 10);
    if (!targetNum || targetNum < 1) {
      setSetupError('Please enter a daily target of at least 1 situation.');
      return;
    }

    setStartingSession(true);
    try {
      const res = await situationsAPI.startSession({
        category: selectedCategory,
        daily_target: targetNum,
        is_revision: isRevision,
      });
      setActiveSession(res.data);
      if (res.data.current_situation) {
        setRobotState(
          'EXPLAINING',
          `Situation 1/${targetNum}: Listen in Telugu, then respond in English.`
        );
      }
    } catch (err) {
      setSetupError(err.response?.data?.detail || 'Could not start speaking session.');
    } finally {
      setStartingSession(false);
    }
  };

  const advanceToNextSituation = async (nextSit, completedCount, totalTarget, isDone, streakData) => {
    setFeedback(null);
    setRepeatResult(null);
    setRepetitionsCompleted(0);
    setPendingNextData(null);
    resetTranscript();

    if (isDone) {
      setActiveSession(null);
      setCompletionInfo({
        completed_count: completedCount,
        daily_target: totalTarget,
        category: selectedCategory,
        streak_info: streakData,
      });
      setRobotState('SUCCESS', `Amazing work! You completed all ${totalTarget} speaking situations today!`);
      triggerCelebration();
      await refreshProfile();
      const statsRes = await situationsAPI.getCategoryStats();
      setCategoryStats(statsRes.data || []);
      return;
    }

    if (nextSit) {
      setActiveSession((prev) =>
        prev
          ? {
              ...prev,
              completed_count: completedCount,
              current_index: prev.current_index + 1,
              current_situation: nextSit,
            }
          : null
      );
      setRobotState(
        'EXPLAINING',
        `Next Situation (${completedCount + 1}/${totalTarget}): Read the Telugu context and answer in English!`
      );
    }
  };

  const handleSubmitAnswer = async () => {
    if (!activeSession?.current_situation || !transcript.trim() || submitting) return;
    if (isListening) stopListening();

    setSubmitting(true);
    setRobotState('THINKING', 'Analyzing your grammar, sentence formation, and vocabulary...');

    try {
      const res = await situationsAPI.submitSessionAnswer(activeSession.id, {
        situation_id: activeSession.current_situation.id,
        original_answer: transcript.trim(),
        recognized_transcript: transcript.trim(),
      });
      const data = res.data;

      setFeedback(data);
      setRepetitionsCompleted(data.repetitions_completed || 0);
      await refreshProfile();

      if (data.is_correct) {
        setRobotState('SUCCESS', 'Well done! Your English response is natural and grammatically accurate.');
        setPendingNextData({
          next_situation: data.next_situation,
          completed_count: data.completed_count,
          daily_target: data.daily_target,
          session_completed: data.session_completed,
          streak_info: data.streak_info,
        });

        autoAdvanceTimerRef.current = setTimeout(() => {
          advanceToNextSituation(
            data.next_situation,
            data.completed_count,
            data.daily_target,
            data.session_completed,
            data.streak_info
          );
        }, 2600);
      } else {
        setRobotState(
          'TEACHING',
          "Good effort! Let's review the corrections and practice the improved sentence twice (1/2)."
        );
      }
    } catch (err) {
      setRobotState('IDLE', err.response?.data?.detail || 'Something went wrong while analyzing.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleRepeatEvaluation = async (repeatedSentence) => {
    if (!feedback?.attempt_id || !activeSession || isEvaluatingRepeat) return;

    setIsEvaluatingRepeat(true);
    setRobotState('THINKING', 'Checking your repeat sentence accuracy...');

    try {
      const res = await situationsAPI.submitSessionRepeat(activeSession.id, {
        attempt_id: feedback.attempt_id,
        repeated_sentence: repeatedSentence,
      });
      const data = res.data;

      setRepeatResult(data);
      setRepetitionsCompleted(data.repetitions_completed || 0);

      if (!data.is_successful) {
        setRobotState('TEACHING', data.feedback || 'Almost there. Try repeating carefully!');
        return;
      }

      if (!data.item_completed) {
        // 1/2 completed -> prompt for 2/2
        setRobotState('SUCCESS', data.feedback);
      } else {
        // 2/2 completed -> update profile & auto-advance!
        setRobotState('SUCCESS', data.feedback);
        triggerCelebration();
        await refreshProfile();

        setPendingNextData({
          next_situation: data.next_situation,
          completed_count: data.completed_count,
          daily_target: data.daily_target,
          session_completed: data.session_completed,
          streak_info: data.streak_info,
        });

        autoAdvanceTimerRef.current = setTimeout(() => {
          advanceToNextSituation(
            data.next_situation,
            data.completed_count,
            data.daily_target,
            data.session_completed,
            data.streak_info
          );
        }, 1800);
      }
    } catch (err) {
      console.error('Repeat evaluation error:', err);
    } finally {
      setIsEvaluatingRepeat(false);
    }
  };

  const handleManualNext = () => {
    if (autoAdvanceTimerRef.current) clearTimeout(autoAdvanceTimerRef.current);
    if (!pendingNextData) return;
    advanceToNextSituation(
      pendingNextData.next_situation,
      pendingNextData.completed_count,
      pendingNextData.daily_target,
      pendingNextData.session_completed,
      pendingNextData.streak_info
    );
  };

  const handleAbandonSession = async () => {
    if (!activeSession) return;
    if (autoAdvanceTimerRef.current) clearTimeout(autoAdvanceTimerRef.current);
    try {
      await situationsAPI.abandonSession(activeSession.id);
    } catch (e) {}
    setActiveSession(null);
    setFeedback(null);
    setRepeatResult(null);
    setRepetitionsCompleted(0);
    setPendingNextData(null);
    resetTranscript();
    loadInitialData();
  };

  const currentSituation = activeSession?.current_situation;

  return (
    <div className="practice-page-container">
      {/* Header & Sub-Navigation */}
      <div className="module-top-header">
        <div>
          <span className="module-tag-pill">
            <Sparkles size={14} /> Module 2 • Real-Life Speaking
          </span>
          <h2>Speaking Practice</h2>
          <p className="module-subtitle">
            Understand real-life Telugu situations, respond naturally in English, and master improved responses with your AI Tutor.
          </p>
        </div>

        <div className="module-subnav-pills">
          {SPEAKING_TABS.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                type="button"
                className={`subnav-pill-btn ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
              >
                <Icon size={16} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* =====================================================================
          TAB 1: AI SPEAKING PRACTICE SESSION
         ===================================================================== */}
      {activeTab === 'session' && (
        <div>
          {loading ? (
            <div className="loading-state-box">
              <RefreshCw size={32} className="spin-icon text-blue" />
              <p>Loading Speaking Practice...</p>
            </div>
          ) : completionInfo ? (
            <div className="session-complete-card" data-testid="speaking-session-complete">
              <div className="complete-robot-wrap">
                <RobotTutor size="medium" showMessage={true} />
              </div>
              <div className="complete-badge">
                <Award size={20} />
                <span>SPEAKING TARGET COMPLETE</span>
              </div>
              <h3>Fantastic Speaking Practice!</h3>
              <p className="complete-desc">
                You completed <strong>{completionInfo.completed_count} / {completionInfo.daily_target}</strong> real-life situations
                in <strong>{completionInfo.category}</strong>.
              </p>

              {completionInfo.streak_info && (
                <div className="complete-streak-banner">
                  <Flame size={20} className="flame-icon" />
                  <span>
                    Current Streak: <strong>{completionInfo.streak_info.current_streak} Days</strong>
                    {' '}• Longest Streak: <strong>{completionInfo.streak_info.longest_streak} Days</strong>
                  </span>
                </div>
              )}

              <div className="complete-actions-row">
                <button
                  type="button"
                  className="btn-primary-action"
                  onClick={() => {
                    setCompletionInfo(null);
                    setActiveTab('history');
                  }}
                >
                  <History size={17} />
                  <span>View Practice History</span>
                </button>
                <button
                  type="button"
                  className="btn-secondary-action"
                  onClick={() => {
                    setCompletionInfo(null);
                    loadInitialData();
                  }}
                >
                  <RotateCcw size={17} />
                  <span>Start New Session</span>
                </button>
              </div>
            </div>
          ) : !activeSession ? (
            /* SPEAKING SESSION SETUP */
            <div className="session-setup-grid">
              <div className="setup-main-card">
                <form onSubmit={handleStartSession} className="setup-config-form">
                  <div className="setup-row-two">
                    <div className="setup-field">
                      <label htmlFor="sp-category-select">1. Situation Category</label>
                      <select
                        id="sp-category-select"
                        value={selectedCategory}
                        onChange={(e) => {
                          setSelectedCategory(e.target.value);
                          setSetupError('');
                        }}
                      >
                        <option value="All">
                          All Categories ({isRevision ? totalAvailableAll - remainingNewAll : remainingNewAll} available)
                        </option>
                        {categoryStats.map((cat) => {
                          const cnt = isRevision
                            ? cat.total_count - cat.remaining_new_count
                            : cat.remaining_new_count;
                          return (
                            <option key={cat.name} value={cat.name}>
                              {cat.name} ({cnt} available)
                            </option>
                          );
                        })}
                      </select>
                    </div>

                    <div className="setup-field">
                      <label>Practice Mode</label>
                      <div className="type-toggle-group">
                        <button
                          type="button"
                          className={`toggle-btn ${!isRevision ? 'active' : ''}`}
                          onClick={() => {
                            setIsRevision(false);
                            setSetupError('');
                          }}
                        >
                          New Situations
                        </button>
                        <button
                          type="button"
                          className={`toggle-btn ${isRevision ? 'active' : ''}`}
                          onClick={() => {
                            setIsRevision(true);
                            setSetupError('');
                          }}
                        >
                          Revision ({totalAvailableAll - remainingNewAll})
                        </button>
                      </div>
                    </div>
                  </div>

                  <div className="setup-field">
                    <label htmlFor="sp-target-input">2. Today's Speaking Target</label>
                    <div className="target-picker-row">
                      <div className="target-presets">
                        {TARGET_PRESETS.map((num) => (
                          <button
                            key={num}
                            type="button"
                            className={`preset-chip ${Number(dailyTarget) === num ? 'active' : ''}`}
                            onClick={() => {
                              setDailyTarget(num);
                              setSetupError('');
                            }}
                          >
                            {num} situations
                          </button>
                        ))}
                      </div>
                      <input
                        id="sp-target-input"
                        type="number"
                        min={1}
                        max={25}
                        value={dailyTarget}
                        onChange={(e) => {
                          setDailyTarget(e.target.value);
                          setSetupError('');
                        }}
                        className="target-number-input"
                        aria-label="Speaking daily target"
                      />
                    </div>
                    <p className="field-hint">
                      Eligible situations in this selection: <strong>{eligibleCountForSelection}</strong>
                      {isRevision ? ' (Revision does not count toward new situation progress)' : ' (Already completed situations are never repeated as new)'}
                    </p>
                  </div>

                  {setupError && (
                    <div className="setup-error-banner">
                      <AlertTriangle size={16} />
                      <span>{setupError}</span>
                    </div>
                  )}

                  {eligibleCountForSelection < Number(dailyTarget) && (
                    <div className="setup-warning-note">
                      <Lightbulb size={16} />
                      <span>
                        Only <strong>{eligibleCountForSelection}</strong> situations available in this category. Lower your target or choose "All Categories".
                      </span>
                    </div>
                  )}

                  <button
                    type="submit"
                    className="btn-start-session"
                    disabled={startingSession || eligibleCountForSelection === 0}
                  >
                    <Play size={18} />
                    <span>{startingSession ? 'Preparing...' : `Start ${dailyTarget}-Situation Session`}</span>
                    <ArrowRight size={18} />
                  </button>
                </form>
              </div>

              <div className="setup-robot-aside">
                <RobotTutor size="medium" showMessage={true} />
                <div className="aside-stats-card">
                  <Target size={18} className="text-blue" />
                  <div>
                    <strong>{totalAvailableAll - remainingNewAll} / {totalAvailableAll} Mastered</strong>
                    <span>Unique real-life situations completed</span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            /* ACTIVE SPEAKING SESSION STAGE */
            <div data-testid="speaking-active-stage">
              <div className="stage-progress-bar">
                <div className="stage-meta-badges">
                  <span className="meta-chip mode">{activeSession.category}</span>
                  {activeSession.is_revision && <span className="meta-chip rev">Revision</span>}
                </div>

                <div className="stage-counter-wrap">
                  <span className="counter-label" data-testid="speaking-session-progress">
                    Completed: <strong>{activeSession.completed_count} / {activeSession.daily_target}</strong>
                  </span>
                  <div className="linear-progress-track">
                    <div
                      className="linear-progress-fill"
                      style={{
                        width: `${Math.round((activeSession.completed_count / activeSession.daily_target) * 100)}%`,
                      }}
                    />
                  </div>
                </div>

                <button
                  type="button"
                  className="btn-abandon-session"
                  onClick={handleAbandonSession}
                >
                  End Session
                </button>
              </div>

              <div className="practice-workspace-grid">
                <div className="tutor-side-column">
                  <RobotTutor size="medium" showMessage={true} />
                </div>

                <div className="practice-main-column">
                  {currentSituation && (
                    <div className="situation-prompt-card">
                      <div className="situation-card-top">
                        <span className="category-badge">{currentSituation.category}</span>
                        <DifficultyBadge level={currentSituation.level} />
                      </div>

                      <h3 className="situation-title" data-testid="speaking-situation-title">
                        {currentSituation.title}
                      </h3>

                      <div className="telugu-situation-box">
                        <div className="box-label-row">
                          <span className="telugu-flag-pill">
                            <Globe size={14} /> తెలుగులో వివరణ (Situation in Telugu)
                          </span>
                          {currentSituation.telugu_transliteration && (
                            <button
                              type="button"
                              className="btn-toggle-translit"
                              onClick={() => setShowRomanized(!showRomanized)}
                            >
                              {showRomanized ? 'Hide Phonetics' : 'Show Romanized Telugu'}
                            </button>
                          )}
                        </div>

                        <p className="telugu-script-text">{currentSituation.telugu_explanation}</p>

                        {showRomanized && currentSituation.telugu_transliteration && (
                          <p className="romanized-text">({currentSituation.telugu_transliteration})</p>
                        )}
                      </div>

                      <div className="english-question-box">
                        <div className="question-label">
                          <HelpCircle size={16} className="text-blue" />
                          <span>Now Explain in English:</span>
                          <button
                            type="button"
                            className="btn-tiny-audio"
                            onClick={() => speak(currentSituation.english_prompt)}
                            title="Listen to Question"
                          >
                            <Volume2 size={14} />
                          </button>
                        </div>
                        <p className="english-prompt-text" data-testid="speaking-english-prompt">
                          "{currentSituation.english_prompt}"
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Focused Interaction: Voice & Text Input OR Evaluation Feedback */}
                  {!feedback ? (
                    <VoiceInput
                      transcript={transcript}
                      setTranscript={setTranscript}
                      isListening={isListening}
                      startListening={startListening}
                      stopListening={stopListening}
                      resetTranscript={resetTranscript}
                      error={speechError}
                      isSupported={isSupported}
                      onSubmit={handleSubmitAnswer}
                      isLoading={submitting}
                    />
                  ) : (
                    <FeedbackCard
                      feedback={feedback}
                      onRepeatEvaluation={handleRepeatEvaluation}
                      onNextSituation={handleManualNext}
                      isEvaluatingRepeat={isEvaluatingRepeat}
                      repeatResult={repeatResult}
                      repetitionsCompleted={repetitionsCompleted}
                      repetitionsRequired={2}
                      sessionMode={true}
                    />
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* =====================================================================
          TAB 2: PERSISTENT SPEAKING PRACTICE HISTORY
         ===================================================================== */}
      {activeTab === 'history' && (
        <div className="history-list-container" data-testid="speaking-history-view">
          {loadingHistory ? (
            <div className="loading-state-box">
              <RefreshCw size={28} className="spin-icon text-blue" />
              <p>Loading your Speaking Practice history...</p>
            </div>
          ) : historySessions.length === 0 ? (
            <div className="empty-state-box">
              <History size={38} className="text-muted" />
              <h3>No speaking sessions recorded yet</h3>
              <p>Start and complete a Speaking Practice session to build your history here.</p>
            </div>
          ) : (
            <div className="sessions-history-stack">
              {historySessions.map((sess) => {
                const isExpanded = expandedSessionId === sess.id;
                return (
                  <div key={sess.id} className="history-session-card">
                    <div
                      className="history-session-summary"
                      onClick={() => setExpandedSessionId(isExpanded ? null : sess.id)}
                    >
                      <div className="hs-left">
                        <div className="hs-badges">
                          <span className="meta-chip mode">{sess.category}</span>
                          <span className={`status-pill ${sess.status}`}>
                            {sess.status === 'completed' ? 'Completed' : sess.status}
                          </span>
                          {sess.is_revision && <span className="meta-chip rev">Revision</span>}
                        </div>
                        <span className="hs-date">Date: {sess.local_date}</span>
                      </div>

                      <div className="hs-right">
                        <strong>{sess.completed_count} / {sess.daily_target} Situations</strong>
                        <span className="expand-hint">{isExpanded ? 'Hide Details' : 'View Situations'}</span>
                      </div>
                    </div>

                    {isExpanded && (
                      <div className="history-attempts-list">
                        {sess.attempts.length === 0 ? (
                          <p className="no-attempts-msg">No situations answered in this session yet.</p>
                        ) : (
                          sess.attempts.map((att) => (
                            <div key={att.id} className={`history-attempt-row ${att.mistakes_json?.length === 0 ? 'ok' : 'corrected'}`}>
                              <div className="ha-main">
                                <span className="ha-title">{att.situation_title || 'Situation'}</span>
                                <span className="ha-ans">Your Answer: <strong>"{att.original_answer}"</strong></span>
                                <span className="ha-correct">
                                  Natural/Improved: <strong>"{att.natural_expression || att.corrected_sentence}"</strong>
                                </span>
                              </div>
                              <div className="ha-meta">
                                <span className={`eval-pill ${att.mistakes_json?.length === 0 ? 'pass' : 'fixed'}`}>
                                  {att.mistakes_json?.length === 0
                                    ? `Accurate (${Math.round(att.score)}%)`
                                    : `Corrected (${att.repetition_success_count}/2 repeats)`}
                                </span>
                              </div>
                            </div>
                          ))
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
