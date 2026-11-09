import React, { useState, useEffect } from 'react';
import { learningAPI, aiAPI } from '../services/api';
import { useTutor } from '../context/TutorContext';
import { DifficultyBadge } from '../components/DifficultyBadge';
import {
  Boxes, Volume2, Mic, CheckCircle2, Sparkles, ArrowRight,
  Lightbulb, RefreshCw
} from 'lucide-react';

export function SentencePatterns() {
  const { setRobotState, speak } = useTutor();
  const [patterns, setPatterns] = useState([]);
  const [activePattern, setActivePattern] = useState(null);
  const [userSentence, setUserSentence] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [checking, setChecking] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setRobotState(
      'TEACHING',
      'Sentence patterns are the secret to fluent English! Master these core structures.'
    );

    const loadPatterns = async () => {
      try {
        const res = await learningAPI.getPatterns();
        setPatterns(res.data);
        if (res.data.length > 0) {
          setActivePattern(res.data[0]);
        }
      } catch (err) {
        console.warn('Failed to load patterns:', err);
      } finally {
        setLoading(false);
      }
    };

    loadPatterns();
  }, [setRobotState]);

  const handleCheckSentence = async () => {
    if (!userSentence.trim() || checking) return;
    setChecking(true);
    setRobotState('THINKING');

    try {
      const res = await aiAPI.correctSentence(userSentence.trim());
      setFeedback(res.data);
      if (res.data.is_grammatically_sound) {
        setRobotState('SUCCESS', 'Excellent usage of this sentence pattern!');
      } else {
        setRobotState('TEACHING', 'Good try! Look at the corrected structure.');
      }
    } catch (err) {
      console.error('Pattern check error:', err);
    } finally {
      setChecking(false);
    }
  };

  return (
    <div className="sentence-patterns-page">
      <div className="page-header-row">
        <div>
          <h2>Reusable Sentence Pattern Practice</h2>
          <p className="subtitle">
            Learn high-frequency sentence formulas that native speakers use every day.
          </p>
        </div>
      </div>

      <div className="patterns-layout-grid">
        {/* Left Column: Pattern Selector */}
        <div className="patterns-list-col">
          <h4 className="sidebar-col-title">Core Patterns</h4>
          <div className="patterns-nav-list">
            {patterns.map((p) => (
              <button
                key={p.id}
                className={`pattern-nav-item ${activePattern?.id === p.id ? 'active' : ''}`}
                onClick={() => {
                  setActivePattern(p);
                  setFeedback(null);
                  setUserSentence('');
                }}
              >
                <span className="pattern-name">{p.pattern}</span>
                <DifficultyBadge level={p.level} showIcon={false} />
              </button>
            ))}
          </div>
        </div>

        {/* Right Column: Pattern Details & Exercise */}
        <div className="pattern-detail-col">
          {activePattern && (
            <div className="pattern-detail-card">
              <div className="pattern-header-card">
                <div className="pattern-title-group">
                  <span className="pattern-pill">{activePattern.pattern}</span>
                  <DifficultyBadge level={activePattern.level} />
                </div>
                <div className="formula-box">
                  <span className="formula-label">Formula:</span>
                  <code className="formula-code">{activePattern.structure_formula}</code>
                </div>
              </div>

              {/* Purpose & Explanation */}
              <div className="pattern-info-grid">
                <div className="info-box">
                  <div className="box-title">
                    <Lightbulb size={16} /> Purpose
                  </div>
                  <p>{activePattern.purpose}</p>
                </div>
                <div className="info-box">
                  <div className="box-title">
                    <Boxes size={16} /> Explanation
                  </div>
                  <p>{activePattern.explanation}</p>
                </div>
              </div>

              {/* Practical Examples */}
              <div className="pattern-examples-section">
                <h4>Practical Daily Examples</h4>
                <div className="examples-cards-grid">
                  {activePattern.examples_json?.map((ex, idx) => (
                    <div key={idx} className="pattern-example-card">
                      <div className="example-top">
                        <span className="example-eng">"{ex.sentence}"</span>
                        <button
                          className="btn-tiny-audio"
                          onClick={() => speak(ex.sentence)}
                          title="Listen to pronunciation"
                        >
                          <Volume2 size={15} />
                        </button>
                      </div>
                      <span className="example-telugu">{ex.meaning}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Interactive Challenge */}
              <div className="pattern-practice-box">
                <div className="practice-box-header">
                  <Sparkles size={18} className="text-blue" />
                  <h4>Speaking Challenge</h4>
                </div>
                <p className="practice-prompt-text">{activePattern.speaking_prompt}</p>

                <div className="practice-input-row">
                  <input
                    type="text"
                    className="pattern-text-input"
                    value={userSentence}
                    onChange={(e) => setUserSentence(e.target.value)}
                    placeholder={`e.g. ${activePattern.pattern.replace(' + verb', '...')} `}
                  />
                  <button
                    className="btn-pattern-submit"
                    onClick={handleCheckSentence}
                    disabled={checking || !userSentence.trim()}
                  >
                    <span>{checking ? 'Checking...' : 'Check My Sentence'}</span>
                  </button>
                </div>

                {feedback && (
                  <div
                    className={`pattern-feedback-result ${
                      feedback.is_grammatically_sound ? 'feedback-good' : 'feedback-fix'
                    }`}
                  >
                    <div className="feedback-top-badge">
                      {feedback.is_grammatically_sound ? (
                        <>
                          <CheckCircle2 size={18} className="text-green" />
                          <strong>Correct Pattern Usage!</strong>
                        </>
                      ) : (
                        <>
                          <Boxes size={18} className="text-amber" />
                          <strong>Suggested Improvement:</strong>
                        </>
                      )}
                    </div>
                    <p className="feedback-corrected">"{feedback.corrected}"</p>
                    <p className="feedback-expl">{feedback.explanation}</p>
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
