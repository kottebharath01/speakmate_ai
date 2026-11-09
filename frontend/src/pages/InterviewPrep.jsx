import React, { useState, useEffect } from 'react';
import { interviewAPI } from '../services/api';
import { useTutor } from '../context/TutorContext';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';
import { RobotTutor } from '../components/RobotTutor';
import {
  Briefcase, Mic, MicOff, Send, Award, CheckCircle2,
  AlertTriangle, Sparkles, Volume2, ArrowRight, RotateCw
} from 'lucide-react';

const INTERVIEW_TRACKS = [
  { id: 'Self-Introduction', label: 'Self-Introduction', desc: 'Craft a compelling 90-second intro.' },
  { id: 'Python Developer', label: 'Python Developer', desc: 'FastAPI, OOP, decorators & memory.' },
  { id: 'SQL & Database', label: 'SQL & Database', desc: 'Joins, indexing, and optimization.' },
  { id: 'Project Explanation', label: 'Project Explanation', desc: 'Architecture, technical challenges & impact.' },
  { id: 'HR & Behavioral', label: 'HR & Behavioral', desc: 'Strengths, teamwork, and conflict handling.' },
];

export function InterviewPrep() {
  const { setRobotState, speak, triggerCelebration } = useTutor();
  const [selectedTrack, setSelectedTrack] = useState('Self-Introduction');
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [candidateAnswer, setCandidateAnswer] = useState('');
  const [evaluation, setEvaluation] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const {
    transcript,
    setTranscript,
    isListening,
    startListening,
    stopListening,
    resetTranscript,
  } = useSpeechRecognition();

  // Start interview session when track changes
  useEffect(() => {
    const initTrack = async () => {
      try {
        const res = await interviewAPI.start(selectedTrack);
        setCurrentQuestion(res.data.first_question);
        setCandidateAnswer('');
        setEvaluation(null);
        resetTranscript();
        setRobotState(
          'TEACHING',
          `Welcome to the ${selectedTrack} mock interview. Listen to the question and answer confidently.`
        );
      } catch (err) {
        console.warn('Interview start error:', err);
      }
    };
    initTrack();
  }, [selectedTrack, setRobotState]);

  // Sync speech transcript
  useEffect(() => {
    if (transcript) {
      setCandidateAnswer(transcript);
    }
  }, [transcript]);

  const handleSubmitInterviewAnswer = async () => {
    const answerToSubmit = candidateAnswer.trim();
    if (!answerToSubmit || submitting) return;

    if (isListening) stopListening();

    setSubmitting(true);
    setRobotState('THINKING', 'Analyzing your interview response structure, clarity, and technical terminology...');

    try {
      const res = await interviewAPI.answer({
        topic: selectedTrack,
        question: currentQuestion,
        answer: answerToSubmit,
      });

      setEvaluation(res.data);
      if (res.data.score >= 80) {
        setRobotState('SUCCESS', 'Strong answer! You communicated your points clearly.');
        triggerCelebration();
      } else {
        setRobotState('TEACHING', 'Good effort. Review the improved model answer below.');
      }
    } catch (err) {
      console.error('Interview answer error:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleNextQuestion = () => {
    if (evaluation?.next_question) {
      setCurrentQuestion(evaluation.next_question);
      setCandidateAnswer('');
      setEvaluation(null);
      resetTranscript();
      setRobotState('TEACHING', 'Here is your next question. Take your time to formulate your answer.');
    }
  };

  return (
    <div className="interview-prep-page">
      <div className="page-header-row">
        <div>
          <h2>Technical & HR Interview Preparation</h2>
          <p className="subtitle">
            Practice answering common job interview questions with instant AI scoring and model answers.
          </p>
        </div>

        {/* Tracks Selector */}
        <div className="interview-tracks-scroll">
          {INTERVIEW_TRACKS.map((track) => (
            <button
              key={track.id}
              className={`track-pill-btn ${selectedTrack === track.id ? 'active' : ''}`}
              onClick={() => setSelectedTrack(track.id)}
            >
              <Briefcase size={14} />
              <span>{track.label}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="interview-grid-layout">
        {/* Left Column: Robot Interviewer */}
        <div className="interviewer-card-col">
          <RobotTutor size="medium" showMessage={true} />

          <div className="interview-tips-box">
            <h4>💡 Pro Interview Tips</h4>
            <ul>
              <li>Use the STAR format (Situation, Task, Action, Result).</li>
              <li>Avoid starting with "Myself [Name]"; say "My name is [Name]".</li>
              <li>Speak at a steady, measured pace without rushing.</li>
            </ul>
          </div>
        </div>

        {/* Right Column: Question, Microphone & Feedback */}
        <div className="interview-action-col">
          {/* Question Card */}
          <div className="interview-question-card">
            <div className="card-top-row">
              <span className="question-track-tag">{selectedTrack}</span>
              <button
                className="btn-speak-question"
                onClick={() => speak(currentQuestion)}
                title="Hear question"
              >
                <Volume2 size={16} />
                <span>Listen</span>
              </button>
            </div>
            <h3 className="question-text">"{currentQuestion}"</h3>
          </div>

          {!evaluation ? (
            /* Candidate Speaking / Typing Area */
            <div className="interview-response-card">
              <div className="response-header">
                <span>Your Spoken Answer:</span>
                <span className="mic-hint">Click mic to record or type below</span>
              </div>

              <textarea
                className="interview-answer-textarea"
                rows={5}
                value={candidateAnswer}
                onChange={(e) => setCandidateAnswer(e.target.value)}
                placeholder="Speak your answer or type it here..."
                disabled={submitting}
              />

              <div className="interview-controls-row">
                <button
                  type="button"
                  className={`btn-interview-mic ${isListening ? 'listening' : ''}`}
                  onClick={isListening ? stopListening : startListening}
                  disabled={submitting}
                >
                  {isListening ? <MicOff size={18} /> : <Mic size={18} />}
                  <span>{isListening ? 'Stop Speaking' : 'Tap to Speak Answer'}</span>
                </button>

                <button
                  type="button"
                  className="btn-interview-submit"
                  onClick={handleSubmitInterviewAnswer}
                  disabled={submitting || !candidateAnswer.trim()}
                >
                  {submitting ? <RotateCw className="spin-icon" size={16} /> : <Send size={16} />}
                  <span>{submitting ? 'Evaluating...' : 'Submit Answer'}</span>
                </button>
              </div>
            </div>
          ) : (
            /* Evaluation Results */
            <div className="interview-evaluation-card">
              <div className="eval-header-row">
                <div className="score-badge-circle">
                  <Award size={20} />
                  <span>{Math.round(evaluation.score)}%</span>
                </div>
                <div className="eval-summary">
                  <h4>Interviewer Evaluation</h4>
                  <p>{evaluation.interviewer_feedback}</p>
                </div>
              </div>

              <div className="strengths-improvements-grid">
                <div className="strengths-card">
                  <div className="eval-sub-title text-green">
                    <CheckCircle2 size={16} /> Key Strengths
                  </div>
                  <ul>
                    {evaluation.strengths?.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>

                <div className="improvements-card">
                  <div className="eval-sub-title text-amber">
                    <AlertTriangle size={16} /> Areas to Improve
                  </div>
                  <ul>
                    {evaluation.areas_for_improvement?.map((imp, i) => (
                      <li key={i}>{imp}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Improved Model Answer */}
              <div className="model-answer-card">
                <div className="model-top">
                  <Sparkles size={16} className="text-blue" />
                  <strong>Polished Model Answer:</strong>
                  <button
                    className="btn-tiny-audio"
                    onClick={() => speak(evaluation.improved_model_answer)}
                    title="Listen to model answer"
                  >
                    <Volume2 size={14} />
                  </button>
                </div>
                <p className="model-text">"{evaluation.improved_model_answer}"</p>
              </div>

              <div className="eval-footer-row">
                <button className="btn-next-question" onClick={handleNextQuestion}>
                  <span>Continue to Next Question</span>
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
