import React, { useState, useEffect } from 'react';
import { learningAPI, aiAPI } from '../services/api';
import { useTutor } from '../context/TutorContext';
import { DifficultyBadge } from '../components/DifficultyBadge';
import {
  BookOpen, CheckCircle2, AlertTriangle, ArrowRight, Lightbulb,
  Sparkles, Check, HelpCircle
} from 'lucide-react';

export function GrammarAcademy() {
  const { setRobotState } = useTutor();
  const [lessons, setLessons] = useState([]);
  const [activeLesson, setActiveLesson] = useState(null);
  const [practiceSentence, setPracticeSentence] = useState('');
  const [practiceResult, setPracticeResult] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setRobotState('TEACHING', 'Welcome to the Grammar Academy! Master the fundamentals of English grammar.');
    const fetchLessons = async () => {
      try {
        const res = await learningAPI.getLessons('grammar');
        setLessons(res.data);
        if (res.data.length > 0) {
          setActiveLesson(res.data[0]);
        }
      } catch (err) {
        console.warn('Failed to load grammar lessons:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchLessons();
  }, [setRobotState]);

  const handleTestSentence = async () => {
    if (!practiceSentence.trim() || analyzing) return;
    setAnalyzing(true);
    setRobotState('THINKING');

    try {
      const res = await aiAPI.correctSentence(practiceSentence.trim());
      setPracticeResult(res.data);
      if (res.data.is_grammatically_sound) {
        setRobotState('SUCCESS', 'Great job! That sentence is grammatically correct.');
      } else {
        setRobotState('TEACHING', 'Check the explanation to see how to improve this sentence.');
      }
    } catch (err) {
      console.error('Correction test error:', err);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="grammar-academy-page">
      <div className="page-header-row">
        <div>
          <h2>Grammar Academy</h2>
          <p className="subtitle">Clear definitions, practical rules, common learner mistakes, and exercises.</p>
        </div>
      </div>

      <div className="academy-layout-grid">
        {/* Left Column: Lesson Directory */}
        <div className="lessons-sidebar-col">
          <h4 className="sidebar-col-title">Topics & Lessons</h4>
          <div className="lessons-nav-list">
            {lessons.map((lesson) => (
              <button
                key={lesson.id}
                className={`lesson-nav-item ${activeLesson?.id === lesson.id ? 'active' : ''}`}
                onClick={() => {
                  setActiveLesson(lesson);
                  setPracticeResult(null);
                  setPracticeSentence('');
                }}
              >
                <div className="lesson-nav-top">
                  <span className="lesson-nav-order">#{lesson.order_num}</span>
                  <DifficultyBadge level={lesson.level} showIcon={false} />
                </div>
                <span className="lesson-nav-title">{lesson.title}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Right Column: Active Lesson View & Exercise */}
        <div className="lesson-content-col">
          {activeLesson && (
            <div className="lesson-detail-card">
              <div className="lesson-detail-header">
                <div>
                  <div className="lesson-badge-row">
                    <span className="category-pill">Grammar</span>
                    <DifficultyBadge level={activeLesson.level} />
                  </div>
                  <h3>{activeLesson.title}</h3>
                </div>
              </div>

              <p className="lesson-desc">{activeLesson.description}</p>

              {activeLesson.content_json && (
                <div className="lesson-body-sections">
                  {/* Definition */}
                  {activeLesson.content_json.definition && (
                    <div className="lesson-box definition-box">
                      <div className="box-title">
                        <BookOpen size={16} /> Definition
                      </div>
                      <p>{activeLesson.content_json.definition}</p>
                    </div>
                  )}

                  {/* Simple Explanation */}
                  {activeLesson.content_json.explanation && (
                    <div className="lesson-box explanation-box">
                      <div className="box-title">
                        <Lightbulb size={16} /> Simple Explanation (Why it matters)
                      </div>
                      <p>{activeLesson.content_json.explanation}</p>
                    </div>
                  )}

                  {/* Key Rules */}
                  {activeLesson.content_json.key_rules && (
                    <div className="lesson-box rules-box">
                      <div className="box-title">
                        <CheckCircle2 size={16} /> Key Rules to Remember
                      </div>
                      <ul className="rules-bullet-list">
                        {activeLesson.content_json.key_rules.map((rule, idx) => (
                          <li key={idx}>{rule}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Common Mistakes */}
                  {activeLesson.content_json.common_mistakes && (
                    <div className="lesson-box mistakes-box">
                      <div className="box-title">
                        <AlertTriangle size={16} /> Common Telugu Learner Mistakes
                      </div>
                      <div className="mistakes-compare-list">
                        {activeLesson.content_json.common_mistakes.map((cm, idx) => (
                          <div key={idx} className="mistake-compare-row">
                            <div className="compare-sides">
                              <span className="side-incorrect">❌ {cm.incorrect}</span>
                              <ArrowRight size={14} className="side-arrow" />
                              <span className="side-correct">✔️ {cm.correct}</span>
                            </div>
                            <p className="compare-reason">{cm.reason}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Interactive Sentence Check Exercise */}
              <div className="lesson-exercise-card">
                <div className="exercise-header">
                  <Sparkles size={18} className="text-blue" />
                  <h4>Interactive Practice: Test a Sentence</h4>
                </div>
                <p className="exercise-hint">
                  Write or speak a sentence applying what you just learned. The AI will check if it is grammatically sound.
                </p>

                <div className="exercise-input-group">
                  <input
                    type="text"
                    className="exercise-input"
                    value={practiceSentence}
                    onChange={(e) => setPracticeSentence(e.target.value)}
                    placeholder="e.g. He speaks English fluently..."
                  />
                  <button
                    className="btn-exercise-check"
                    onClick={handleTestSentence}
                    disabled={analyzing || !practiceSentence.trim()}
                  >
                    <span>{analyzing ? 'Checking...' : 'Check Sentence'}</span>
                  </button>
                </div>

                {practiceResult && (
                  <div
                    className={`exercise-result-box ${
                      practiceResult.is_grammatically_sound ? 'result-good' : 'result-bad'
                    }`}
                  >
                    <div className="result-top">
                      {practiceResult.is_grammatically_sound ? (
                        <>
                          <CheckCircle2 size={18} className="text-green" />
                          <strong>Grammatically Correct!</strong>
                        </>
                      ) : (
                        <>
                          <AlertTriangle size={18} className="text-amber" />
                          <strong>Correction Needed:</strong>
                        </>
                      )}
                    </div>
                    <p className="result-corrected">"{practiceResult.corrected}"</p>
                    <p className="result-expl">{practiceResult.explanation}</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
