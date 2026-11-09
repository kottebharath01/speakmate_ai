import React, { useState, useEffect } from 'react';
import { situationsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useTutor } from '../context/TutorContext';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';
import { RobotTutor } from '../components/RobotTutor';
import { VoiceInput } from '../components/VoiceInput';
import { FeedbackCard } from '../components/FeedbackCard';
import { DifficultyBadge } from '../components/DifficultyBadge';
import {
  Sparkles, RotateCcw, Volume2, Globe, HelpCircle, Layers,
  ChevronRight, RefreshCw, CheckCircle2
} from 'lucide-react';

export function SituationPractice() {
  const { profile, refreshProfile } = useAuth();
  const { setRobotState, triggerCelebration } = useTutor();

  const [situations, setSituations] = useState([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [isEvaluatingRepeat, setIsEvaluatingRepeat] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [repeatResult, setRepeatResult] = useState(null);
  const [showRomanized, setShowRomanized] = useState(false);
  const [generatingNew, setGeneratingNew] = useState(false);

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

  // Load situations for user's level
  const loadSituations = async () => {
    setLoading(true);
    try {
      const userLevel = profile?.current_level || 'BEGINNER';
      const res = await situationsAPI.getAll(userLevel);
      setSituations(res.data);
      setCurrentIdx(0);
      setFeedback(null);
      setRepeatResult(null);
      resetTranscript();
    } catch (err) {
      console.warn('Failed to load situations:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSituations();
  }, [profile?.current_level]);

  // Update robot state when situation changes
  const currentSituation = situations[currentIdx];

  useEffect(() => {
    if (currentSituation && !feedback) {
      setRobotState(
        'EXPLAINING',
        `Listen to this real-life situation in Telugu. How would you explain it in English?`
      );
    }
  }, [currentSituation, feedback, setRobotState]);

  // Sync robot listening state with microphone
  useEffect(() => {
    if (isListening) {
      setRobotState('LISTENING', "I'm listening to your English. Speak clearly!");
    } else if (!submitting && !feedback) {
      setRobotState('IDLE');
    }
  }, [isListening, submitting, feedback, setRobotState]);

  // Submit learner's answer for AI evaluation
  const handleSubmitAnswer = async () => {
    if (!currentSituation || !transcript.trim()) return;

    setSubmitting(true);
    setRobotState('THINKING', 'Analyzing your grammar, sentence structure, and vocabulary...');

    try {
      const res = await situationsAPI.submit({
        situation_id: currentSituation.id,
        original_answer: transcript.trim(),
        recognized_transcript: transcript.trim(),
      });

      setFeedback(res.data);
      setRobotState(
        'TEACHING',
        res.data.is_correct
          ? 'Well done! Your sentence is grammatically correct.'
          : "Good attempt! Let's examine the corrections and natural phrasing."
      );
      await refreshProfile();
    } catch (err) {
      console.error('Answer submission error:', err);
      setRobotState('IDLE', 'Something went wrong while analyzing. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  // Re-evaluation of repeated sentence
  const handleRepeatEvaluation = async (repeatedSentence) => {
    if (!feedback?.attempt_id) return;

    setIsEvaluatingRepeat(true);
    setRobotState('THINKING', 'Checking your repeat sentence accuracy...');

    try {
      const res = await situationsAPI.evaluateRepeat({
        attempt_id: feedback.attempt_id,
        target_sentence: feedback.corrected_sentence,
        repeated_sentence: repeatedSentence,
        previous_mistake: feedback.mistakes?.[0]?.explanation || null,
      });

      setRepeatResult(res.data);

      if (res.data.is_successful) {
        setRobotState(
          'SUCCESS',
          'Brilliant! You corrected the previous mistake and spoke accurately!'
        );
        triggerCelebration();
        await refreshProfile();
      } else {
        setRobotState(
          'TEACHING',
          res.data.feedback || "Almost there. Give it one more try!"
        );
      }
    } catch (err) {
      console.error('Repeat evaluation error:', err);
    } finally {
      setIsEvaluatingRepeat(false);
    }
  };

  // Move to next situation
  const handleNextSituation = () => {
    setFeedback(null);
    setRepeatResult(null);
    resetTranscript();

    if (currentIdx < situations.length - 1) {
      setCurrentIdx((prev) => prev + 1);
    } else {
      // Loop back or reload
      setCurrentIdx(0);
    }
  };

  // Generate a dynamic new situation using AI
  const handleGenerateNew = async () => {
    setGeneratingNew(true);
    try {
      const userLevel = profile?.current_level || 'BEGINNER';
      const res = await situationsAPI.generate('Daily Conversation', userLevel);
      setSituations((prev) => [res.data, ...prev]);
      setCurrentIdx(0);
      setFeedback(null);
      setRepeatResult(null);
      resetTranscript();
    } catch (err) {
      console.error('Generate situation error:', err);
    } finally {
      setGeneratingNew(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-state-screen">
        <RefreshCw className="spin-icon text-blue" size={36} />
        <p>Loading real-life speaking situations...</p>
      </div>
    );
  }

  return (
    <div className="situation-practice-page">
      {/* Top Header Bar */}
      <div className="page-header-row">
        <div className="header-titles">
          <h2>Situation-Based Speaking Practice</h2>
          <p className="subtitle">
            Understand the real-life situation in Telugu, then speak your response in English.
          </p>
        </div>

        <div className="header-actions">
          <button
            className="btn-generate-ai"
            onClick={handleGenerateNew}
            disabled={generatingNew}
            title="Generate a fresh daily situation with AI"
          >
            <Sparkles size={16} />
            <span>{generatingNew ? 'Generating...' : 'AI Generate New'}</span>
          </button>
        </div>
      </div>

      {/* Main Two-Column Layout: Left (Robot & Situation), Right (Input & Feedback) */}
      <div className="practice-layout-grid">
        {/* Left Column: Robot Tutor and Situation Scenario Card */}
        <div className="left-tutor-column">
          <div className="robot-wrapper-card">
            <RobotTutor size="medium" showMessage={true} />
          </div>

          {currentSituation && (
            <div className="situation-scenario-card">
              <div className="scenario-meta-row">
                <span className="category-pill">{currentSituation.category}</span>
                <DifficultyBadge level={currentSituation.level} />
                <span className="situation-counter">
                  {currentIdx + 1} of {situations.length}
                </span>
              </div>

              <h3 className="scenario-title">{currentSituation.title}</h3>

              {/* STEP 2: Situation in Telugu */}
              <div className="telugu-situation-box">
                <div className="telugu-box-header">
                  <span className="telugu-title-badge">
                    <Globe size={14} /> పరిస్థితి (Telugu Context):
                  </span>
                  {currentSituation.telugu_transliteration && (
                    <button
                      className="btn-toggle-roman"
                      onClick={() => setShowRomanized(!showRomanized)}
                    >
                      {showRomanized ? 'Show Telugu Script' : 'Phonetic English'}
                    </button>
                  )}
                </div>

                <p className="telugu-text">
                  {showRomanized && currentSituation.telugu_transliteration
                    ? currentSituation.telugu_transliteration
                    : currentSituation.telugu_explanation}
                </p>
              </div>

              {/* STEP 3: English Instruction Question */}
              <div className="english-prompt-box">
                <span className="prompt-label">
                  <HelpCircle size={14} /> What to say in English:
                </span>
                <p className="prompt-question">{currentSituation.english_prompt}</p>
                <div className="hidden-answer-banner">
                  <span>🔒 Complete answer is hidden. Challenge yourself to speak first!</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Voice Input & Detailed Feedback */}
        <div className="right-interactive-column">
          {!feedback ? (
            /* STEP 4: Voice Input Component */
            <div className="input-step-container">
              <div className="step-guide-banner">
                <span className="step-num">Step 4</span>
                <span>Speak your English answer into the microphone, or type it below.</span>
              </div>

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
                disabled={submitting}
                placeholder="Click the microphone to speak, or type how you would explain this to the other person in English..."
              />
            </div>
          ) : (
            /* STEP 6 & 7: Detailed Feedback Card (A to G) */
            <FeedbackCard
              feedback={feedback}
              onRepeatEvaluation={handleRepeatEvaluation}
              onNextSituation={handleNextSituation}
              isEvaluatingRepeat={isEvaluatingRepeat}
              repeatResult={repeatResult}
            />
          )}
        </div>
      </div>
    </div>
  );
}
