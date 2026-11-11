import React, { useState, useEffect, useRef } from 'react';
import { wordsExpressionsAPI } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { useTutor } from '../../context/TutorContext';
import { useSpeechSynthesis } from '../../hooks/useSpeechSynthesis';
import { useSpeechRecognition } from '../../hooks/useSpeechRecognition';
import { RobotTutor } from '../../components/RobotTutor';
import { DifficultyBadge } from '../../components/DifficultyBadge';
import {
  BookOpen, MessageSquare, Compass, CheckCircle2, Bookmark,
  Volume2, Search, Sparkles, RefreshCw, ArrowRight, Award,
  Lightbulb, AlertTriangle, Check, X, Mic, MicOff, History,
  Library, Play, RotateCcw, Target, Flame
} from 'lucide-react';

const MODULE_TABS = [
  { id: 'session', label: 'AI Tutor Session', icon: Play },
  { id: 'history', label: 'Learning History', icon: History },
  { id: 'library', label: 'Content Library', icon: Library },
];

const MODE_OPTIONS = [
  {
    id: 'words',
    title: 'Words',
    icon: BookOpen,
    subtitle: 'Individual Telugu words & natural English equivalents',
  },
  {
    id: 'expressions',
    title: 'Expressions',
    icon: MessageSquare,
    subtitle: 'Daily-use expressions, complete sentences & office phrases',
  },
  {
    id: 'situation_expressions',
    title: 'Situation Expressions',
    icon: Compass,
    subtitle: 'Topic-based phrases for Daily Life, Office, Travel & Interviews',
  },
];

const TARGET_PRESETS = [5, 10, 15, 20];

export function WordsExpressions() {
  const { refreshProfile } = useAuth();
  const { setRobotState, triggerCelebration } = useTutor();
  const { speak } = useSpeechSynthesis();

  const {
    transcript,
    setTranscript,
    interimTranscript,
    isListening,
    startListening,
    stopListening,
    resetTranscript,
    error: speechError,
    isSupported: speechSupported,
  } = useSpeechRecognition();

  // Top-level view within module: 'session' | 'history' | 'library'
  const [activeTab, setActiveTab] = useState('session');

  // Modes summary & setup state
  const [modesSummary, setModesSummary] = useState(null);
  const [selectedMode, setSelectedMode] = useState('words');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [dailyTarget, setDailyTarget] = useState(10);
  const [isRevision, setIsRevision] = useState(false);
  const [setupError, setSetupError] = useState('');
  const [startingSession, setStartingSession] = useState(false);

  // Active AI Tutor Session state
  const [activeSession, setActiveSession] = useState(null);
  const [sessionLoading, setSessionLoading] = useState(true);
  const [typedAnswer, setTypedAnswer] = useState('');
  const [submittingAnswer, setSubmittingAnswer] = useState(false);

  // Step feedback state (when item just evaluated)
  const [stepFeedback, setStepFeedback] = useState(null);
  const [repeatTyped, setRepeatTyped] = useState('');
  const [repeatErrorMsg, setRepeatErrorMsg] = useState('');
  const [submittingRepeat, setSubmittingRepeat] = useState(false);
  const [completionInfo, setCompletionInfo] = useState(null);

  // History tab state
  const [historySessions, setHistorySessions] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [expandedSessionId, setExpandedSessionId] = useState(null);

  // Library browser tab state
  const [libraryItems, setLibraryItems] = useState([]);
  const [librarySearch, setLibrarySearch] = useState('');
  const [libraryModeFilter, setLibraryModeFilter] = useState('ALL');
  const [loadingLibrary, setLoadingLibrary] = useState(false);

  const autoAdvanceTimerRef = useRef(null);

  // Clear auto-advance timer safely on cleanup
  useEffect(() => {
    return () => {
      if (autoAdvanceTimerRef.current) {
        clearTimeout(autoAdvanceTimerRef.current);
      }
    };
  }, []);

  // Load initial modes summary & check for existing active session
  const loadInitialSessionData = async () => {
    setSessionLoading(true);
    try {
      const [summaryRes, activeRes] = await Promise.all([
        wordsExpressionsAPI.getModesSummary(),
        wordsExpressionsAPI.getActiveSession(),
      ]);
      setModesSummary(summaryRes.data);

      if (activeRes.data && activeRes.data.status === 'active') {
        const sess = activeRes.data;
        setActiveSession(sess);

        // If refreshing mid-way through a 2-repetition correction, restore feedback state!
        if (sess.pending_attempt) {
          const pa = sess.pending_attempt;
          setStepFeedback({
            attempt_id: pa.id,
            is_correct: false,
            accepted_answer: pa.accepted_answer,
            valid_alternatives: pa.valid_alternatives_json || [],
            evaluation_feedback: pa.evaluation_feedback,
            correction_details: pa.correction_details,
            example_sentence: pa.example_sentence,
            repetition_required: true,
            repetitions_completed: pa.repetition_success_count,
            repetitions_required: 2,
          });
          setRobotState(
            'TEACHING',
            `Welcome back! Repeat "${pa.accepted_answer}" (${pa.repetition_success_count}/2 completed).`
          );
        } else if (sess.current_item) {
          setStepFeedback(null);
          setRobotState(
            'EXPLAINING',
            `Telugu: "${sess.current_item.telugu_text}". How do you say this in English?`
          );
        }
      } else {
        setActiveSession(null);
        setRobotState(
          'GREETING',
          'Choose a learning mode and set your daily target to begin Words & Expressions!'
        );
      }
    } catch (err) {
      console.warn('Error initializing Words & Expressions module:', err);
    } finally {
      setSessionLoading(false);
    }
  };

  useEffect(() => {
    loadInitialSessionData();
  }, []);

  // Sync voice transcript and listening visual state cleanly
  useEffect(() => {
    if (isListening) {
      setRobotState('LISTENING', 'Listening... Speak your English answer clearly!');
    }
  }, [isListening, setRobotState]);

  useEffect(() => {
    if (!transcript && !interimTranscript) return;
    const text = transcript || interimTranscript;
    if (stepFeedback?.repetition_required) {
      setRepeatTyped(text);
    } else {
      setTypedAnswer(text);
    }
  }, [transcript, interimTranscript, stepFeedback]);

  // Load Learning History when switching to history tab
  const loadHistory = async () => {
    setLoadingHistory(true);
    try {
      const res = await wordsExpressionsAPI.getSessionHistory();
      setHistorySessions(res.data || []);
    } catch (err) {
      console.warn('Failed to load word session history:', err);
    } finally {
      setLoadingHistory(false);
    }
  };

  // Load Library browser items
  const loadLibrary = async () => {
    setLoadingLibrary(true);
    try {
      const params = { page: 1, page_size: 40 };
      if (librarySearch.trim()) params.search = librarySearch.trim();
      if (libraryModeFilter === 'WORDS') params.section = 'words';
      if (libraryModeFilter === 'PHRASES') params.section = 'phrases';
      if (libraryModeFilter === 'SITUATIONS') params.section = 'situations';
      if (libraryModeFilter === 'BOOKMARKED') params.bookmarked_only = true;
      const res = await wordsExpressionsAPI.getItems(params);
      setLibraryItems(res.data.items || []);
    } catch (err) {
      console.warn('Failed to load content library:', err);
    } finally {
      setLoadingLibrary(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'history') {
      loadHistory();
    } else if (activeTab === 'library') {
      loadLibrary();
    }
  }, [activeTab, librarySearch, libraryModeFilter]);

  // Derived mode stats for setup screen
  const activeModeObj = modesSummary?.modes?.find((m) => m.mode === selectedMode);
  const availableCategories = activeModeObj?.categories || [];
  const selectedCatObj = availableCategories.find((c) => c.name === selectedCategory);
  const eligibleCountForSelection = isRevision
    ? (selectedCategory === 'All'
        ? (activeModeObj ? activeModeObj.total_items - activeModeObj.remaining_new_items : 0)
        : (selectedCatObj ? selectedCatObj.total_count - selectedCatObj.remaining_new_count : 0))
    : (selectedCategory === 'All'
        ? (activeModeObj?.remaining_new_items ?? 0)
        : (selectedCatObj?.remaining_new_count ?? 0));

  // Start Guided Learning Session
  const handleStartSession = async (e) => {
    e.preventDefault();
    setSetupError('');
    setCompletionInfo(null);
    setStepFeedback(null);
    setTypedAnswer('');
    setRepeatTyped('');
    resetTranscript();

    const targetNum = parseInt(dailyTarget, 10);
    if (!targetNum || targetNum < 1) {
      setSetupError('Please enter a daily target of at least 1.');
      return;
    }

    setStartingSession(true);
    try {
      const res = await wordsExpressionsAPI.startSession({
        mode: selectedMode,
        category: selectedCategory,
        daily_target: targetNum,
        is_revision: isRevision,
      });
      setActiveSession(res.data);
      if (res.data.current_item) {
        setRobotState(
          'EXPLAINING',
          `Let's start! Telugu: "${res.data.current_item.telugu_text}". How do you say this in English?`
        );
      }
    } catch (err) {
      setSetupError(err.response?.data?.detail || 'Could not start session. Please check target count.');
    } finally {
      setStartingSession(false);
    }
  };

  // Helper to move session smoothly to next item or complete
  const advanceSessionView = async (nextItem, completedCount, totalTarget, isDone, streakData) => {
    setStepFeedback(null);
    setTypedAnswer('');
    setRepeatTyped('');
    setRepeatErrorMsg('');
    resetTranscript();

    if (isDone) {
      setActiveSession(null);
      setCompletionInfo({
        completed_count: completedCount,
        daily_target: totalTarget,
        mode: selectedMode,
        category: selectedCategory,
        streak_info: streakData,
      });
      setRobotState('SUCCESS', `Congratulations! You completed today's target of ${totalTarget} items!`);
      triggerCelebration();
      await refreshProfile();
      const summaryRes = await wordsExpressionsAPI.getModesSummary();
      setModesSummary(summaryRes.data);
      return;
    }

    if (nextItem) {
      setActiveSession((prev) =>
        prev
          ? {
              ...prev,
              completed_count: completedCount,
              current_index: prev.current_index + 1,
              current_item: nextItem,
            }
          : null
      );
      setRobotState(
        'EXPLAINING',
        `Next item (${completedCount + 1}/${totalTarget}): How do you say this in English?`
      );
    }
  };

  // Step 2 & 3: Submit Learner Answer
  const handleSubmitAnswer = async (e) => {
    if (e) e.preventDefault();
    const answerText = (typedAnswer || transcript).trim();
    if (!answerText || !activeSession?.current_item || submittingAnswer) return;
    if (isListening) stopListening();

    setSubmittingAnswer(true);
    setRepeatErrorMsg('');
    setRobotState('THINKING', 'Evaluating your English answer...');

    try {
      const res = await wordsExpressionsAPI.submitSessionAnswer(activeSession.id, {
        item_id: activeSession.current_item.id,
        answer: answerText,
      });
      const data = res.data;

      if (data.is_correct) {
        // Correct -> Show confirmation + example sentence, then automatically progress!
        setStepFeedback({ ...data, repetition_required: false });
        setRobotState('SUCCESS', data.evaluation_feedback);
        await refreshProfile();

        autoAdvanceTimerRef.current = setTimeout(() => {
          advanceSessionView(
            data.next_item,
            data.completed_count,
            data.daily_target,
            data.session_completed,
            data.streak_info
          );
        }, 2200);
      } else {
        // Incorrect -> Enter mandatory 2-repetition workflow (1/2, 2/2)
        setStepFeedback(data);
        setTypedAnswer('');
        resetTranscript();
        setRobotState(
          'TEACHING',
          `Almost! Correct English: "${data.accepted_answer}". Please repeat it twice (1/2).`
        );
      }
    } catch (err) {
      setRobotState('IDLE', err.response?.data?.detail || 'Error checking your answer.');
    } finally {
      setSubmittingAnswer(false);
    }
  };

  // Step 5: Submit Repetition (Enforces 1/2 -> 2/2)
  const handleSubmitRepeat = async (e) => {
    if (e) e.preventDefault();
    const repText = (repeatTyped || transcript).trim();
    if (!repText || !stepFeedback?.attempt_id || submittingRepeat) return;
    if (isListening) stopListening();

    setSubmittingRepeat(true);
    setRepeatErrorMsg('');
    setRobotState('THINKING', 'Checking your repetition...');

    try {
      const res = await wordsExpressionsAPI.submitSessionRepeat(activeSession.id, {
        attempt_id: stepFeedback.attempt_id,
        repeated_answer: repText,
      });
      const data = res.data;

      if (!data.is_successful) {
        setRepeatErrorMsg(data.feedback);
        setRobotState('TEACHING', data.feedback);
        return;
      }

      setRepeatTyped('');
      resetTranscript();

      if (!data.item_completed) {
        // 1/2 completed -> update count and wait for 2/2
        setStepFeedback((prev) => ({
          ...prev,
          repetitions_completed: data.repetitions_completed,
        }));
        setRobotState('SUCCESS', data.feedback);
      } else {
        // 2/2 completed -> automatically advance to next item!
        setStepFeedback((prev) => ({
          ...prev,
          repetitions_completed: 2,
          item_completed: true,
        }));
        setRobotState('SUCCESS', data.feedback);
        await refreshProfile();

        autoAdvanceTimerRef.current = setTimeout(() => {
          advanceSessionView(
            data.next_item,
            data.completed_count,
            data.daily_target,
            data.session_completed,
            data.streak_info
          );
        }, 1600);
      }
    } catch (err) {
      setRepeatErrorMsg(err.response?.data?.detail || 'Could not verify repetition.');
    } finally {
      setSubmittingRepeat(false);
    }
  };

  const handleAbandonSession = async () => {
    if (!activeSession) return;
    if (autoAdvanceTimerRef.current) clearTimeout(autoAdvanceTimerRef.current);
    try {
      await wordsExpressionsAPI.abandonSession(activeSession.id);
    } catch (e) {}
    setActiveSession(null);
    setStepFeedback(null);
    setTypedAnswer('');
    setRepeatTyped('');
    resetTranscript();
    loadInitialSessionData();
  };

  const handleToggleBookmarkLibrary = async (itemId) => {
    try {
      const res = await wordsExpressionsAPI.toggleBookmark(itemId);
      setLibraryItems((prev) =>
        prev.map((item) =>
          item.id === itemId ? { ...item, is_bookmarked: res.data.is_bookmarked } : item
        )
      );
    } catch (err) {
      console.warn('Bookmark failed:', err);
    }
  };

  const handleManualNext = () => {
    if (autoAdvanceTimerRef.current) clearTimeout(autoAdvanceTimerRef.current);
    if (!stepFeedback) return;
    advanceSessionView(
      stepFeedback.next_item,
      stepFeedback.completed_count,
      stepFeedback.daily_target,
      stepFeedback.session_completed,
      stepFeedback.streak_info
    );
  };

  return (
    <div className="words-module-container">
      {/* Clean Header & Module Sub-Navigation */}
      <div className="module-top-header">
        <div>
          <span className="module-tag-pill">
            <Sparkles size={14} /> Module 1 • Independent Learning
          </span>
          <h2>Words & Expressions</h2>
          <p className="module-subtitle">
            Learn Telugu words, daily expressions, and real-life situation phrases guided step-by-step by your AI Tutor.
          </p>
        </div>

        <div className="module-subnav-pills">
          {MODULE_TABS.map((tab) => {
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
          TAB 1: AI TUTOR SESSION WORKSPACE
         ===================================================================== */}
      {activeTab === 'session' && (
        <div className="we-session-workspace">
          {sessionLoading ? (
            <div className="loading-state-box">
              <RefreshCw size={32} className="spin-icon text-blue" />
              <p>Loading your Words & Expressions session...</p>
            </div>
          ) : completionInfo ? (
            /* SESSION COMPLETED CELEBRATION VIEW */
            <div className="session-complete-card" data-testid="words-session-complete">
              <div className="complete-robot-wrap">
                <RobotTutor size="medium" showMessage={true} />
              </div>
              <div className="complete-badge">
                <Award size={20} />
                <span>SESSION COMPLETE</span>
              </div>
              <h3>Great Job! Today's Target Completed!</h3>
              <p className="complete-desc">
                You completed <strong>{completionInfo.completed_count} / {completionInfo.daily_target}</strong>{' '}
                items in <strong>{MODE_OPTIONS.find((m) => m.id === completionInfo.mode)?.title}</strong>{' '}
                ({completionInfo.category}).
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
                  <span>View Learning History</span>
                </button>
                <button
                  type="button"
                  className="btn-secondary-action"
                  onClick={() => {
                    setCompletionInfo(null);
                    loadInitialSessionData();
                  }}
                >
                  <RotateCcw size={17} />
                  <span>Start New Session</span>
                </button>
              </div>
            </div>
          ) : !activeSession ? (
            /* SESSION SETUP SCREEN (3 Modes + Category + Target) */
            <div className="session-setup-grid">
              <div className="setup-main-card">
                <div className="setup-step-block">
                  <h3>1. Select Learning Mode</h3>
                  <div className="mode-cards-grid">
                    {MODE_OPTIONS.map((mode) => {
                      const Icon = mode.icon;
                      const stats = modesSummary?.modes?.find((m) => m.mode === mode.id);
                      const remaining = stats?.remaining_new_items ?? 0;
                      const isSelected = selectedMode === mode.id;

                      return (
                        <button
                          key={mode.id}
                          type="button"
                          className={`mode-select-card ${isSelected ? 'selected' : ''}`}
                          onClick={() => {
                            setSelectedMode(mode.id);
                            setSelectedCategory('All');
                            setSetupError('');
                          }}
                        >
                          <div className="mode-card-icon">
                            <Icon size={22} />
                          </div>
                          <div className="mode-card-body">
                            <h4>{mode.title}</h4>
                            <p>{mode.subtitle}</p>
                            <span className="mode-count-chip">
                              {remaining} new items ready
                            </span>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                </div>

                <form onSubmit={handleStartSession} className="setup-config-form">
                  <div className="setup-row-two">
                    {/* Step 2: Category Selection */}
                    <div className="setup-field">
                      <label htmlFor="we-category-select">2. Category</label>
                      <select
                        id="we-category-select"
                        value={selectedCategory}
                        onChange={(e) => {
                          setSelectedCategory(e.target.value);
                          setSetupError('');
                        }}
                      >
                        <option value="All">
                          All Categories ({isRevision
                            ? (activeModeObj ? activeModeObj.total_items - activeModeObj.remaining_new_items : 0)
                            : (activeModeObj?.remaining_new_items ?? 0)} available)
                        </option>
                        {availableCategories.map((cat) => {
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

                    {/* New Learning vs Revision Toggle */}
                    <div className="setup-field">
                      <label>Learning Type</label>
                      <div className="type-toggle-group">
                        <button
                          type="button"
                          className={`toggle-btn ${!isRevision ? 'active' : ''}`}
                          onClick={() => {
                            setIsRevision(false);
                            setSetupError('');
                          }}
                        >
                          New Learning
                        </button>
                        <button
                          type="button"
                          className={`toggle-btn ${isRevision ? 'active' : ''}`}
                          onClick={() => {
                            setIsRevision(true);
                            setSetupError('');
                          }}
                        >
                          Revision ({activeModeObj ? activeModeObj.total_items - activeModeObj.remaining_new_items : 0})
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Step 3: Daily Target */}
                  <div className="setup-field">
                    <label htmlFor="we-target-input">3. Today's Learning Target</label>
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
                            {num} items
                          </button>
                        ))}
                      </div>
                      <input
                        id="we-target-input"
                        type="number"
                        min={1}
                        max={50}
                        value={dailyTarget}
                        onChange={(e) => {
                          setDailyTarget(e.target.value);
                          setSetupError('');
                        }}
                        className="target-number-input"
                        aria-label="Custom daily target"
                      />
                    </div>
                    <p className="field-hint">
                      Eligible items in this selection: <strong>{eligibleCountForSelection}</strong>
                      {isRevision ? ' (Revision does not count toward new item progress)' : ' (Duplicates automatically prevented)'}
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
                        Only <strong>{eligibleCountForSelection}</strong> items available here. Lower target to{' '}
                        <strong>{eligibleCountForSelection}</strong> or choose another category.
                      </span>
                    </div>
                  )}

                  <button
                    type="submit"
                    className="btn-start-session"
                    disabled={startingSession || eligibleCountForSelection === 0}
                  >
                    <Play size={18} />
                    <span>
                      {startingSession ? 'Preparing Session...' : `Start ${dailyTarget}-${selectedMode === 'words' ? 'Word' : 'Item'} Session`}
                    </span>
                    <ArrowRight size={18} />
                  </button>
                </form>
              </div>

              <div className="setup-robot-aside">
                <RobotTutor size="medium" showMessage={true} />
                <div className="aside-stats-card">
                  <Target size={18} className="text-blue" />
                  <div>
                    <strong>{modesSummary?.total_learned_by_user ?? 0} Mastered</strong>
                    <span>Total words & expressions completed</span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            /* ACTIVE AI TUTOR LEARNING WORKFLOW */
            <div className="active-tutor-stage" data-testid="words-active-stage">
              {/* Session Progress Bar */}
              <div className="stage-progress-bar">
                <div className="stage-meta-badges">
                  <span className="meta-chip mode">{MODE_OPTIONS.find((m) => m.id === activeSession.mode)?.title}</span>
                  <span className="meta-chip cat">{activeSession.category}</span>
                  {activeSession.is_revision && <span className="meta-chip rev">Revision</span>}
                </div>

                <div className="stage-counter-wrap">
                  <span className="counter-label" data-testid="words-session-progress">
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

              {/* Main Teaching Card: Robot + Telugu Prompt + Step Controls */}
              <div className="tutor-teaching-layout">
                <div className="tutor-stage-robot">
                  <RobotTutor size="medium" showMessage={true} />
                </div>

                <div className="tutor-interaction-card">
                  {activeSession.current_item && (
                    <div className="telugu-prompt-panel">
                      <div className="prompt-top-tags">
                        <span className="prompt-label">తెలుగు • TELUGU</span>
                        <DifficultyBadge level={activeSession.current_item.level} showIcon={false} />
                      </div>
                      <h2 className="prominent-telugu-text" data-testid="words-telugu-prompt">
                        {activeSession.current_item.telugu_text}
                      </h2>
                      {activeSession.current_item.telugu_transliteration && (
                        <span className="prompt-translit">
                          ({activeSession.current_item.telugu_transliteration})
                        </span>
                      )}
                      <p className="tutor-question-line">
                        "How do you say this in English?"
                      </p>
                    </div>
                  )}

                  {/* PHASE 1: Awaiting Learner's Initial Answer */}
                  {!stepFeedback ? (
                    <form onSubmit={handleSubmitAnswer} className="answer-input-panel">
                      {!speechSupported && (
                        <div className="voice-fallback-notice">
                          Voice recording is unavailable in this browser. Type your English answer below.
                        </div>
                      )}
                      {speechError && (
                        <div className="voice-error-notice">
                          <AlertTriangle size={15} />
                          <span>{speechError}</span>
                        </div>
                      )}

                      <div className="voice-text-input-row">
                        <button
                          type="button"
                          className={`btn-mic-circle ${isListening ? 'listening' : ''}`}
                          onClick={isListening ? stopListening : startListening}
                          disabled={!speechSupported || submittingAnswer}
                          title={isListening ? 'Stop recording' : 'Speak English answer'}
                          aria-label={isListening ? 'Stop recording' : 'Speak English answer'}
                        >
                          {isListening ? <MicOff size={20} /> : <Mic size={20} />}
                        </button>

                        <input
                          type="text"
                          className="english-answer-input"
                          value={typedAnswer}
                          onChange={(e) => {
                            setTypedAnswer(e.target.value);
                            setTranscript(e.target.value);
                          }}
                          placeholder={isListening ? 'Listening... speak in English' : 'Type or speak the English answer...'}
                          disabled={submittingAnswer}
                          aria-label="English answer input"
                          autoFocus
                        />

                        <button
                          type="submit"
                          className="btn-submit-answer"
                          disabled={submittingAnswer || !(typedAnswer.trim() || transcript.trim())}
                        >
                          <span>{submittingAnswer ? 'Checking...' : 'Submit'}</span>
                          <ArrowRight size={16} />
                        </button>
                      </div>
                      {isListening && (
                        <div className="audio-wave-bars" style={{ marginTop: '4px' }}>
                          <span className="bar bar1" />
                          <span className="bar bar2" />
                          <span className="bar bar3" />
                          <span className="listening-label">Listening... Speak in English now (click Stop or Submit when done)</span>
                        </div>
                      )}
                      <p className="input-helper-caption">
                        Evaluates meaning, natural English usage & grammar (Voice converts speech to text).
                      </p>
                    </form>
                  ) : !stepFeedback.repetition_required ? (
                    /* PHASE 2A: Answer Was Correct -> Show Confirmation & Natural Example -> Auto Advance */
                    <div className="eval-feedback-panel pass" data-testid="words-correct-feedback">
                      <div className="eval-status-row">
                        <CheckCircle2 size={22} className="text-green" />
                        <h4>Correct Answer!</h4>
                      </div>
                      <div className="accepted-answer-row">
                        <strong>"{stepFeedback.accepted_answer}"</strong>
                        <button
                          type="button"
                          className="btn-speak-pill"
                          onClick={() => speak(stepFeedback.accepted_answer)}
                          title="Listen pronunciation"
                        >
                          <Volume2 size={15} /> Listen
                        </button>
                      </div>
                      <p className="eval-msg">{stepFeedback.evaluation_feedback}</p>

                      {stepFeedback.example_sentence && (
                        <div className="eval-example-box">
                          <span className="mini-cap">Natural Example:</span>
                          <p>"{stepFeedback.example_sentence}"</p>
                        </div>
                      )}

                      <button type="button" className="btn-next-now" onClick={handleManualNext}>
                        <span>{stepFeedback.session_completed ? 'View Completion Summary' : 'Next Item'}</span>
                        <ArrowRight size={16} />
                      </button>
                    </div>
                  ) : (
                    /* PHASE 2B: Answer Incorrect -> Explanation + Exact 2 Repetitions (1/2, 2/2) */
                    <div className="eval-feedback-panel correction" data-testid="words-correction-panel">
                      <div className="eval-status-row">
                        <AlertTriangle size={20} className="text-amber" />
                        <h4>Let's Correct & Practice Together</h4>
                      </div>

                      <div className="correction-target-card">
                        <span className="mini-cap">Correct Natural English:</span>
                        <div className="accepted-answer-row">
                          <strong className="correct-eng" data-testid="words-correct-answer">
                            "{stepFeedback.accepted_answer}"
                          </strong>
                          <button
                            type="button"
                            className="btn-speak-pill"
                            onClick={() => speak(stepFeedback.accepted_answer)}
                          >
                            <Volume2 size={15} /> Listen
                          </button>
                        </div>

                        {stepFeedback.valid_alternatives?.length > 1 && (
                          <p className="alts-line">
                            Also valid: {stepFeedback.valid_alternatives.slice(0, 4).join(', ')}
                          </p>
                        )}
                      </div>

                      {stepFeedback.correction_details && (
                        <p className="eval-explanation">{stepFeedback.correction_details}</p>
                      )}

                      {stepFeedback.example_sentence && (
                        <div className="eval-example-box">
                          <span className="mini-cap">Example Sentence:</span>
                          <p>"{stepFeedback.example_sentence}"</p>
                        </div>
                      )}

                      {/* EXACT TWO-REPETITION ENFORCEMENT (1/2, 2/2) */}
                      <div className="two-rep-box">
                        <div className="rep-steps-header">
                          <span className="rep-title">Repeat Corrected Answer Twice:</span>
                          <div className="rep-badges">
                            <span
                              className={`rep-badge ${stepFeedback.repetitions_completed >= 1 ? 'done' : 'active'}`}
                              data-testid="rep-step-1"
                            >
                              {stepFeedback.repetitions_completed >= 1 ? <Check size={13} /> : '1'} First repetition: {Math.min(1, stepFeedback.repetitions_completed)}/2
                            </span>
                            <span
                              className={`rep-badge ${stepFeedback.repetitions_completed >= 2 ? 'done' : stepFeedback.repetitions_completed === 1 ? 'active' : ''}`}
                              data-testid="rep-step-2"
                            >
                              {stepFeedback.repetitions_completed >= 2 ? <Check size={13} /> : '2'} Second repetition: {stepFeedback.repetitions_completed}/2
                            </span>
                          </div>
                        </div>

                        {speechError && (
                          <div className="voice-error-notice">
                            <AlertTriangle size={15} />
                            <span>{speechError}</span>
                          </div>
                        )}

                        {stepFeedback.repetitions_completed < 2 && (
                          <form onSubmit={handleSubmitRepeat} className="voice-text-input-row">
                            <button
                              type="button"
                              className={`btn-mic-circle ${isListening ? 'listening' : ''}`}
                              onClick={isListening ? stopListening : startListening}
                              disabled={!speechSupported || submittingRepeat}
                              title="Speak repetition"
                            >
                              {isListening ? <MicOff size={20} /> : <Mic size={20} />}
                            </button>

                            <input
                              type="text"
                              className="english-answer-input"
                              value={repeatTyped}
                              onChange={(e) => {
                                setRepeatTyped(e.target.value);
                                setTranscript(e.target.value);
                              }}
                              placeholder={`Repeat "${stepFeedback.accepted_answer}" (${stepFeedback.repetitions_completed === 0 ? '1st time: 1/2' : '2nd time: 2/2'})...`}
                              disabled={submittingRepeat}
                              aria-label="Repetition input"
                              autoFocus
                            />

                            <button
                              type="submit"
                              className="btn-submit-answer"
                              disabled={submittingRepeat || !(repeatTyped.trim() || transcript.trim())}
                            >
                              <span>
                                {submittingRepeat
                                  ? 'Checking...'
                                  : `Verify (${stepFeedback.repetitions_completed + 1}/2)`}
                              </span>
                            </button>
                          </form>
                        )}

                        {isListening && stepFeedback.repetitions_completed < 2 && (
                          <div className="audio-wave-bars">
                            <span className="bar bar1" />
                            <span className="bar bar2" />
                            <span className="bar bar3" />
                            <span className="listening-label">Listening... Repeat the sentence aloud now</span>
                          </div>
                        )}

                        {repeatErrorMsg && (
                          <p className="rep-error-text">{repeatErrorMsg}</p>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* =====================================================================
          TAB 2: PERSISTENT LEARNING HISTORY
         ===================================================================== */}
      {activeTab === 'history' && (
        <div className="history-list-container" data-testid="words-history-view">
          {loadingHistory ? (
            <div className="loading-state-box">
              <RefreshCw size={28} className="spin-icon text-blue" />
              <p>Loading your Words & Expressions history...</p>
            </div>
          ) : historySessions.length === 0 ? (
            <div className="empty-state-box">
              <History size={38} className="text-muted" />
              <h3>No learning sessions yet</h3>
              <p>Complete an AI Tutor Words & Expressions session to track your words and scores here.</p>
            </div>
          ) : (
            <div className="sessions-history-stack">
              {historySessions.map((sess) => {
                const isExpanded = expandedSessionId === sess.id;
                const modeTitle = MODE_OPTIONS.find((m) => m.id === sess.mode)?.title || sess.mode;
                return (
                  <div key={sess.id} className="history-session-card">
                    <div
                      className="history-session-summary"
                      onClick={() => setExpandedSessionId(isExpanded ? null : sess.id)}
                    >
                      <div className="hs-left">
                        <div className="hs-badges">
                          <span className="meta-chip mode">{modeTitle}</span>
                          <span className="meta-chip cat">{sess.category}</span>
                          <span className={`status-pill ${sess.status}`}>
                            {sess.status === 'completed' ? 'Completed' : sess.status}
                          </span>
                          {sess.is_revision && <span className="meta-chip rev">Revision</span>}
                        </div>
                        <span className="hs-date">Date: {sess.local_date}</span>
                      </div>

                      <div className="hs-right">
                        <strong>{sess.completed_count} / {sess.daily_target} Items</strong>
                        <span className="expand-hint">{isExpanded ? 'Hide Details' : 'View Items'}</span>
                      </div>
                    </div>

                    {isExpanded && (
                      <div className="history-attempts-list">
                        {sess.attempts.length === 0 ? (
                          <p className="no-attempts-msg">No items answered in this session yet.</p>
                        ) : (
                          sess.attempts.map((att) => (
                            <div key={att.id} className={`history-attempt-row ${att.is_correct ? 'ok' : 'corrected'}`}>
                              <div className="ha-main">
                                <span className="ha-telugu">{att.telugu_text}</span>
                                <span className="ha-ans">Your Answer: <strong>"{att.original_answer}"</strong></span>
                                <span className="ha-correct">
                                  Accepted English: <strong>"{att.accepted_answer}"</strong>
                                </span>
                              </div>
                              <div className="ha-meta">
                                <span className={`eval-pill ${att.is_correct ? 'pass' : 'fixed'}`}>
                                  {att.is_correct ? 'Correct First Try' : `Corrected (${att.repetition_success_count}/2 repeats)`}
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

      {/* =====================================================================
          TAB 3: BUILT-IN CONTENT LIBRARY REFERENCE BROWSER
         ===================================================================== */}
      {activeTab === 'library' && (
        <div className="library-browser-container">
          <div className="library-controls-row">
            <div className="search-box-wrap">
              <Search size={16} className="search-icon" />
              <input
                type="text"
                value={librarySearch}
                onChange={(e) => setLibrarySearch(e.target.value)}
                placeholder="Search Telugu or English words & expressions..."
              />
            </div>

            <div className="library-filter-pills">
              {[
                { id: 'ALL', label: 'All' },
                { id: 'WORDS', label: 'Words' },
                { id: 'PHRASES', label: 'Expressions' },
                { id: 'SITUATIONS', label: 'Situations' },
                { id: 'BOOKMARKED', label: 'Saved' },
              ].map((f) => (
                <button
                  key={f.id}
                  type="button"
                  className={`level-pill-btn ${libraryModeFilter === f.id ? 'active' : ''}`}
                  onClick={() => setLibraryModeFilter(f.id)}
                >
                  {f.label}
                </button>
              ))}
            </div>
          </div>

          {loadingLibrary ? (
            <div className="loading-state-box">
              <RefreshCw size={28} className="spin-icon text-blue" />
              <p>Loading library items...</p>
            </div>
          ) : (
            <div className="words-items-grid">
              {libraryItems.map((item) => (
                <div key={item.id} className={`word-card-item ${item.is_learned ? 'card-learned' : ''}`}>
                  <div className="card-top-bar">
                    <span className="card-cat-badge">{item.category}</span>
                    <button
                      type="button"
                      className={`btn-action-icon ${item.is_bookmarked ? 'bookmarked' : ''}`}
                      onClick={() => handleToggleBookmarkLibrary(item.id)}
                      title="Bookmark"
                    >
                      <Bookmark size={16} fill={item.is_bookmarked ? '#8b5cf6' : 'none'} />
                    </button>
                  </div>
                  <div className="card-main-content">
                    <span className="telugu-main-text">{item.telugu_text}</span>
                    <div className="english-header-row">
                      <h4 className="english-main-text">{item.english_text}</h4>
                      <button
                        type="button"
                        className="btn-tiny-speak"
                        onClick={() => speak(item.english_text)}
                        title="Listen"
                      >
                        <Volume2 size={15} />
                      </button>
                    </div>
                    {item.english_definition && (
                      <p className="english-def-snippet">{item.english_definition}</p>
                    )}
                    {item.valid_alternatives_json?.length > 0 && (
                      <p className="alts-snippet">
                        Also valid: {item.valid_alternatives_json.slice(0, 3).join(', ')}
                      </p>
                    )}
                  </div>
                  <div className="card-footer-bar">
                    <DifficultyBadge level={item.level} showIcon={false} />
                    {item.is_learned && (
                      <span className="learned-tag">
                        <CheckCircle2 size={13} /> Learned
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
