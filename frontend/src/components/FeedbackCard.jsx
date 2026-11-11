import React, { useState } from 'react';
import {
  CheckCircle2, XCircle, Volume2, Sparkles, AlertTriangle,
  Lightbulb, ArrowRight, RotateCw, Award, Mic, Check
} from 'lucide-react';
import { useSpeechSynthesis } from '../hooks/useSpeechSynthesis';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';

export function FeedbackCard({
  feedback,
  onRepeatEvaluation,
  onNextSituation,
  isEvaluatingRepeat,
  repeatResult,
  repetitionsCompleted = 0,
  repetitionsRequired = 2,
  sessionMode = false,
}) {
  const { speak } = useSpeechSynthesis();
  const [repeatText, setRepeatText] = useState('');

  const {
    isListening,
    transcript,
    startListening,
    stopListening,
    resetTranscript,
    error: speechError,
    isSupported,
  } = useSpeechRecognition();

  if (!feedback) return null;

  const {
    original_answer,
    is_correct,
    score,
    mistakes = [],
    corrected_sentence,
    simple_explanation,
    natural_expression,
    additional_examples = [],
    encouragement,
  } = feedback;

  const handleSpeakCorrect = () => {
    speak(corrected_sentence);
  };

  const handleSpeakNatural = () => {
    speak(natural_expression);
  };

  const handleRepeatSubmit = async () => {
    const speechToEvaluate = (transcript || repeatText).trim();
    if (!speechToEvaluate) return;
    if (isListening) stopListening();
    await onRepeatEvaluation(speechToEvaluate);
    setRepeatText('');
    resetTranscript();
  };

  const repsDoneCount = repetitionsCompleted;
  const canProceedToNext = is_correct || !sessionMode || repsDoneCount >= repetitionsRequired;

  return (
    <div className={`feedback-card-container ${is_correct ? 'card-success' : 'card-improvement'}`}>
      {/* Header Score & Result Badge */}
      <div className="feedback-header">
        <div className="feedback-title-row">
          {is_correct ? (
            <div className="status-badge badge-green">
              <CheckCircle2 size={18} />
              <span>Accurate English!</span>
            </div>
          ) : (
            <div className="status-badge badge-amber">
              <AlertTriangle size={18} />
              <span>Needs Minor Correction</span>
            </div>
          )}
          <div className="score-pill">
            <Award size={16} />
            <span>Score: {Math.round(score)} / 100</span>
          </div>
        </div>
        <p className="encouragement-quote">{encouragement}</p>
      </div>

      <div className="feedback-sections-list">
        {/* SECTION A: Original Answer */}
        <div className="feedback-section section-original">
          <div className="section-title">
            <span className="section-letter">A</span>
            <h4>Original Answer</h4>
          </div>
          <div className="original-box">
            <p className="original-text">"{original_answer}"</p>
          </div>
        </div>

        {/* SECTION B: Mistakes Identified */}
        <div className="feedback-section section-mistakes">
          <div className="section-title">
            <span className="section-letter">B</span>
            <h4>Mistakes Identified</h4>
          </div>
          {mistakes.length === 0 ? (
            <div className="no-mistakes-box">
              <Check size={16} className="text-green" />
              <span>No grammatical mistakes detected! Your sentence structure is sound.</span>
            </div>
          ) : (
            <div className="mistakes-table">
              {mistakes.map((m, idx) => (
                <div key={idx} className="mistake-item-card">
                  <div className="mistake-badge-row">
                    <span className="mistake-cat-tag">{m.category.toUpperCase()}</span>
                    <span className="mistake-diff">
                      <span className="incorrect-part">{m.incorrect_part}</span>
                      <ArrowRight size={14} className="arrow-icon" />
                      <span className="correct-part">{m.correction}</span>
                    </span>
                  </div>
                  <p className="mistake-expl">{m.explanation}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* SECTION C: Corrected Sentence */}
        <div className="feedback-section section-corrected">
          <div className="section-title">
            <span className="section-letter">C</span>
            <h4>Corrected Sentence</h4>
          </div>
          <div className="corrected-box">
            <span className="corrected-text">{corrected_sentence}</span>
            <button
              className="btn-audio-listen"
              onClick={handleSpeakCorrect}
              title="Listen to native pronunciation"
              aria-label="Listen to corrected sentence"
            >
              <Volume2 size={18} />
              <span>Listen</span>
            </button>
          </div>
        </div>

        {/* SECTION D: Explanation */}
        <div className="feedback-section section-explanation">
          <div className="section-title">
            <span className="section-letter">D</span>
            <h4>Explanation</h4>
          </div>
          <div className="explanation-box">
            <Lightbulb size={18} className="bulb-icon" />
            <p>{simple_explanation}</p>
          </div>
        </div>

        {/* SECTION E: Better Natural Expression */}
        {natural_expression && natural_expression !== corrected_sentence && (
          <div className="feedback-section section-natural">
            <div className="section-title">
              <span className="section-letter">E</span>
              <h4>Better Natural Expression</h4>
            </div>
            <div className="natural-box">
              <Sparkles size={18} className="sparkle-icon" />
              <div className="natural-content">
                <p className="natural-text">"{natural_expression}"</p>
                <span className="natural-hint">Native speakers commonly express it like this.</span>
              </div>
              <button
                className="btn-audio-listen subtle"
                onClick={handleSpeakNatural}
                title="Listen to natural phrasing"
              >
                <Volume2 size={16} />
              </button>
            </div>
          </div>
        )}

        {/* SECTION F: Additional Examples */}
        {additional_examples.length > 0 && (
          <div className="feedback-section section-examples">
            <div className="section-title">
              <span className="section-letter">F</span>
              <h4>Additional Practical Examples</h4>
            </div>
            <ul className="examples-list">
              {additional_examples.map((ex, idx) => (
                <li key={idx} className="example-bullet">
                  <span>{ex}</span>
                  <button
                    className="btn-tiny-audio"
                    onClick={() => speak(ex)}
                    title="Listen to example"
                  >
                    <Volume2 size={14} />
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* SECTION G: Practice Again (Only shown when corrections are needed; requires 2 repetitions in guided session) */}
        {!is_correct && (
          <div className="feedback-section section-repeat">
            <div className="section-title">
              <span className="section-letter">G</span>
              <h4>Practice Again – Repeat Corrected Sentence</h4>
            </div>
            <p className="repeat-instructions">
              Repeat the corrected response out loud or type it <strong>{repetitionsRequired} times</strong> to master it:
            </p>

            <div className="rep-badges" style={{ marginBottom: '12px' }}>
              <span
                className={`rep-badge ${repsDoneCount >= 1 ? 'done' : 'active'}`}
                data-testid="speaking-rep-1"
              >
                {repsDoneCount >= 1 ? <Check size={13} /> : '1'} First repetition: {Math.min(1, repsDoneCount)}/{repetitionsRequired}
              </span>
              <span
                className={`rep-badge ${repsDoneCount >= 2 ? 'done' : repsDoneCount === 1 ? 'active' : ''}`}
                data-testid="speaking-rep-2"
              >
                {repsDoneCount >= 2 ? <Check size={13} /> : '2'} Second repetition: {repsDoneCount}/{repetitionsRequired}
              </span>
            </div>

            <div className="target-repeat-card">
              <p className="target-sentence">"{corrected_sentence}"</p>
            </div>

            {(!isSupported || speechError) && (
              <div className="voice-fallback-notice" style={{ marginBottom: '10px' }}>
                {speechError || 'Voice recognition is unavailable here. Type the corrected sentence below.'}
              </div>
            )}

            {/* Repeat Voice Input & Manual Fallback (Hidden once 2/2 succeeded in sessionMode) */}
            {(!sessionMode || repsDoneCount < repetitionsRequired) && (
              <div className="repeat-input-bar">
                <button
                  type="button"
                  className={`btn-repeat-mic ${isListening ? 'listening' : ''}`}
                  onClick={isListening ? stopListening : startListening}
                  disabled={!isSupported || isEvaluatingRepeat}
                >
                  <Mic size={18} />
                  <span>{isListening ? 'Stop Speaking' : 'Tap to Repeat Sentence'}</span>
                </button>

                <input
                  type="text"
                  className="repeat-text-input"
                  value={transcript || repeatText}
                  onChange={(e) => {
                    setRepeatText(e.target.value);
                    if (transcript) resetTranscript();
                  }}
                  placeholder={`Repeat corrected sentence (${repsDoneCount + 1}/${repetitionsRequired})...`}
                  disabled={isEvaluatingRepeat}
                  aria-label="Repeat corrected sentence input"
                />

                <button
                  type="button"
                  className="btn-repeat-verify"
                  onClick={handleRepeatSubmit}
                  disabled={isEvaluatingRepeat || (!transcript.trim() && !repeatText.trim())}
                >
                  {isEvaluatingRepeat ? <RotateCw className="spin-icon" size={16} /> : <Check size={16} />}
                  <span>Verify Repeat {sessionMode ? `(${repsDoneCount + 1}/${repetitionsRequired})` : ''}</span>
                </button>
              </div>
            )}

            {/* Repeat Result Banner */}
            {repeatResult && (
              <div
                className={`repeat-result-banner ${
                  repeatResult.is_successful ? 'banner-success' : 'banner-retry'
                }`}
              >
                <div className="banner-top">
                  {repeatResult.is_successful ? (
                    <>
                      <CheckCircle2 size={20} className="text-green" />
                      <strong>Awesome Job! Accuracy: {Math.round(repeatResult.accuracy_score)}%</strong>
                    </>
                  ) : (
                    <>
                      <XCircle size={20} className="text-red" />
                      <strong>Let's Try Again. Accuracy: {Math.round(repeatResult.accuracy_score)}%</strong>
                    </>
                  )}
                </div>
                <p className="banner-feedback">{repeatResult.feedback}</p>
                {repeatResult.remaining_mistake && (
                  <p className="remaining-mistake-hint">{repeatResult.remaining_mistake}</p>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Action Footer: Next Situation */}
      <div className="feedback-footer">
        <button
          className="btn-next-situation"
          onClick={onNextSituation}
          disabled={!canProceedToNext}
          title={!canProceedToNext ? `Complete ${repetitionsRequired} repetitions to continue` : 'Move to next situation'}
        >
          <span>
            {canProceedToNext
              ? 'Continue to Next Situation'
              : `Complete ${repetitionsRequired - repsDoneCount} more repetition(s) to continue`}
          </span>
          <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
}
