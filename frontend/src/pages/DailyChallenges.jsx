import React, { useState, useEffect } from 'react';
import { learningAPI, aiAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useTutor } from '../context/TutorContext';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';
import {
  CalendarCheck, Award, Mic, MicOff, Send, Sparkles, CheckCircle2,
  Clock, ArrowRight, RotateCw
} from 'lucide-react';

export function DailyChallenges() {
  const { refreshProfile } = useAuth();
  const { setRobotState, triggerCelebration } = useTutor();
  const [challenges, setChallenges] = useState([]);
  const [activeChallenge, setActiveChallenge] = useState(null);
  const [challengeSpeech, setChallengeSpeech] = useState('');
  const [evaluation, setEvaluation] = useState(null);
  const [evaluating, setEvaluating] = useState(false);
  const [loading, setLoading] = useState(true);

  const {
    transcript,
    isListening,
    startListening,
    stopListening,
    resetTranscript,
  } = useSpeechRecognition();

  useEffect(() => {
    setRobotState(
      'TEACHING',
      'Daily challenges keep your speaking habit active! Choose a challenge and record your answer.'
    );

    const loadChallenges = async () => {
      try {
        const res = await learningAPI.getDailyChallenges();
        setChallenges(res.data);
        if (res.data.length > 0) {
          setActiveChallenge(res.data[0]);
        }
      } catch (err) {
        console.warn('Daily challenges fetch error:', err);
      } finally {
        setLoading(false);
      }
    };
    loadChallenges();
  }, [setRobotState]);

  useEffect(() => {
    if (transcript) {
      setChallengeSpeech(transcript);
    }
  }, [transcript]);

  const handleSubmitChallenge = async () => {
    if (!challengeSpeech.trim() || evaluating) return;
    if (isListening) stopListening();

    setEvaluating(true);
    setRobotState('THINKING');

    try {
      const res = await aiAPI.correctSentence(challengeSpeech.trim());
      setEvaluation(res.data);
      if (res.data.is_grammatically_sound) {
        setRobotState('SUCCESS', 'Daily challenge completed successfully! +30 points awarded.');
        triggerCelebration();
      } else {
        setRobotState('TEACHING', 'Great effort! Take a look at the corrected phrasing.');
      }
      await refreshProfile();
    } catch (err) {
      console.error('Challenge submit error:', err);
    } finally {
      setEvaluating(false);
    }
  };

  return (
    <div className="daily-challenges-page">
      <div className="page-header-row">
        <div>
          <h2>Daily English Speaking Challenges</h2>
          <p className="subtitle">
            Complete daily speaking tasks to build consistency, earn points, and strengthen fluency.
          </p>
        </div>
      </div>

      <div className="challenges-layout-grid">
        {/* Left Column: Challenge Cards */}
        <div className="challenges-nav-col">
          <h4 className="sidebar-col-title">Today's Tasks</h4>
          <div className="challenge-cards-list">
            {challenges.map((c) => (
              <div
                key={c.id}
                className={`challenge-nav-card ${activeChallenge?.id === c.id ? 'active' : ''}`}
                onClick={() => {
                  setActiveChallenge(c);
                  setEvaluation(null);
                  setChallengeSpeech('');
                  resetTranscript();
                }}
              >
                <div className="challenge-nav-header">
                  <span className="challenge-topic-pill">{c.topic}</span>
                  <span className="points-pill-tag">+{c.points} pts</span>
                </div>
                <h4 className="challenge-nav-title">{c.title}</h4>
                <p className="challenge-nav-desc">{c.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: Active Challenge Workplace */}
        <div className="challenge-work-col">
          {activeChallenge && (
            <div className="challenge-active-card">
              <div className="challenge-active-header">
                <div>
                  <span className="challenge-topic-pill">{activeChallenge.topic}</span>
                  <h3>{activeChallenge.title}</h3>
                </div>
                <div className="points-reward-badge">
                  <Award size={18} />
                  <span>+{activeChallenge.points} Points</span>
                </div>
              </div>

              {/* Telugu Context Box */}
              <div className="telugu-challenge-box">
                <span className="telugu-label">తెలుగు నేపథ్యం:</span>
                <p className="telugu-body">{activeChallenge.telugu_context}</p>
              </div>

              {/* Speaking Prompt */}
              <div className="challenge-prompt-box">
                <strong>Your Task:</strong> {activeChallenge.speaking_prompt}
              </div>

              {/* Speaking / Typing Area */}
              <div className="challenge-input-box">
                <textarea
                  className="challenge-textarea"
                  rows={4}
                  value={challengeSpeech}
                  onChange={(e) => setChallengeSpeech(e.target.value)}
                  placeholder="Click the microphone to speak your response, or type here..."
                  disabled={evaluating}
                />

                <div className="challenge-actions-bar">
                  <button
                    type="button"
                    className={`btn-challenge-mic ${isListening ? 'listening' : ''}`}
                    onClick={isListening ? stopListening : startListening}
                    disabled={evaluating}
                  >
                    {isListening ? <MicOff size={18} /> : <Mic size={18} />}
                    <span>{isListening ? 'Stop Listening' : 'Record Speaking'}</span>
                  </button>

                  <button
                    type="button"
                    className="btn-challenge-submit"
                    onClick={handleSubmitChallenge}
                    disabled={evaluating || !challengeSpeech.trim()}
                  >
                    {evaluating ? <RotateCw className="spin-icon" size={16} /> : <Send size={16} />}
                    <span>Submit for Evaluation</span>
                  </button>
                </div>
              </div>

              {/* Evaluation Banner */}
              {evaluation && (
                <div
                  className={`challenge-eval-box ${
                    evaluation.is_grammatically_sound ? 'eval-pass' : 'eval-review'
                  }`}
                >
                  <div className="eval-status-row">
                    {evaluation.is_grammatically_sound ? (
                      <>
                        <CheckCircle2 size={20} className="text-green" />
                        <strong>Challenge Completed! Excellent Grammar</strong>
                      </>
                    ) : (
                      <>
                        <Sparkles size={20} className="text-blue" />
                        <strong>Review and Practice:</strong>
                      </>
                    )}
                  </div>
                  <p className="eval-sentence">"{evaluation.corrected}"</p>
                  <p className="eval-expl">{evaluation.explanation}</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
