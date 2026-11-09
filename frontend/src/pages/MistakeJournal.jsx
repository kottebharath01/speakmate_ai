import React, { useState, useEffect } from 'react';
import { progressAPI } from '../services/api';
import { useTutor } from '../context/TutorContext';
import {
  AlertOctagon, CheckCircle2, ArrowRight, RotateCw, Filter,
  Volume2, BookOpen, Sparkles
} from 'lucide-react';

export function MistakeJournal() {
  const { setRobotState, speak } = useTutor();
  const [mistakes, setMistakes] = useState([]);
  const [filterResolved, setFilterResolved] = useState('ALL');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setRobotState(
      'TEACHING',
      'The Mistake Journal is your learning treasure! Review recurring patterns to stop making the same mistakes.'
    );

    const loadMistakes = async () => {
      try {
        const res = await progressAPI.getMistakes();
        setMistakes(res.data);
      } catch (err) {
        console.warn('Failed to load mistakes:', err);
      } finally {
        setLoading(false);
      }
    };

    loadMistakes();
  }, [setRobotState]);

  const filteredMistakes = mistakes.filter((m) => {
    if (filterResolved === 'UNRESOLVED') return !m.is_resolved;
    if (filterResolved === 'RESOLVED') return m.is_resolved;
    return true;
  });

  return (
    <div className="mistake-journal-page">
      <div className="page-header-row">
        <div>
          <h2>Personal Mistake Journal</h2>
          <p className="subtitle">
            Every mistake you make during practice is recorded here with corrections and explanations.
          </p>
        </div>

        {/* Filter Buttons */}
        <div className="journal-filter-pills">
          <button
            className={`filter-pill ${filterResolved === 'ALL' ? 'active' : ''}`}
            onClick={() => setFilterResolved('ALL')}
          >
            All Mistakes ({mistakes.length})
          </button>
          <button
            className={`filter-pill ${filterResolved === 'UNRESOLVED' ? 'active' : ''}`}
            onClick={() => setFilterResolved('UNRESOLVED')}
          >
            Needs Practice ({mistakes.filter((m) => !m.is_resolved).length})
          </button>
          <button
            className={`filter-pill ${filterResolved === 'RESOLVED' ? 'active' : ''}`}
            onClick={() => setFilterResolved('RESOLVED')}
          >
            Resolved ({mistakes.filter((m) => m.is_resolved).length})
          </button>
        </div>
      </div>

      {/* Mistake Cards List */}
      <div className="mistakes-journal-list">
        {filteredMistakes.length > 0 ? (
          filteredMistakes.map((item) => (
            <div
              key={item.id}
              className={`journal-entry-card ${item.is_resolved ? 'entry-resolved' : 'entry-active'}`}
            >
              <div className="entry-header-row">
                <div className="entry-category-group">
                  <span className="category-pill">{item.category.toUpperCase()}</span>
                  <span className="repetition-count-badge">
                    Seen {item.repetition_count} time{item.repetition_count > 1 ? 's' : ''}
                  </span>
                </div>

                <div className="entry-status-badge">
                  {item.is_resolved ? (
                    <span className="badge-resolved">
                      <CheckCircle2 size={15} /> Corrected in Repeat
                    </span>
                  ) : (
                    <span className="badge-needs-revision">
                      <AlertOctagon size={15} /> Needs Revision
                    </span>
                  )}
                </div>
              </div>

              {/* Diff Display */}
              <div className="entry-diff-row">
                <div className="diff-item incorrect">
                  <span className="diff-label">Original error:</span>
                  <p className="diff-text">"{item.original_sentence}"</p>
                </div>

                <ArrowRight size={20} className="diff-arrow-icon" />

                <div className="diff-item correct">
                  <span className="diff-label">Corrected form:</span>
                  <div className="correct-line">
                    <p className="diff-text">"{item.corrected_sentence}"</p>
                    <button
                      className="btn-tiny-audio"
                      onClick={() => speak(item.corrected_sentence)}
                      title="Listen to correct sentence"
                    >
                      <Volume2 size={15} />
                    </button>
                  </div>
                </div>
              </div>

              {/* Explanation Box */}
              <div className="entry-explanation-box">
                <strong>Why it was incorrect:</strong> {item.explanation}
              </div>

              <div className="entry-footer-meta">
                <span>Recorded: {new Date(item.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))
        ) : (
          <div className="empty-journal-box">
            <CheckCircle2 size={40} className="text-green" />
            <h3>No mistakes found in this filter!</h3>
            <p>Keep speaking and practicing to build and refine your skills.</p>
          </div>
        )}
      </div>
    </div>
  );
}
