import React from 'react';
import { Mic, MicOff, RotateCcw, Send, AlertCircle, Edit3 } from 'lucide-react';

export function VoiceInput({
  transcript,
  setTranscript,
  isListening,
  startListening,
  stopListening,
  resetTranscript,
  error,
  isSupported,
  onSubmit,
  disabled = false,
  placeholder = 'Speak your English response or type it here...',
}) {
  const handleToggleMic = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      if (transcript.trim() && !disabled) {
        onSubmit();
      }
    }
  };

  return (
    <div className="voice-input-card">
      <div className="voice-controls-row">
        {/* Main Microphone Button */}
        <button
          type="button"
          className={`mic-button ${isListening ? 'listening' : ''} ${!isSupported ? 'unsupported' : ''}`}
          onClick={handleToggleMic}
          disabled={disabled || !isSupported}
          title={
            !isSupported
              ? 'Voice recognition not supported in this browser. Please type below.'
              : isListening
              ? 'Click to stop listening'
              : 'Click to speak in English'
          }
        >
          {isListening ? (
            <>
              <MicOff size={22} className="pulse-mic" />
              <span>Stop Speaking</span>
            </>
          ) : (
            <>
              <Mic size={22} />
              <span>Tap to Speak English</span>
            </>
          )}
        </button>

        {/* Status Waveform when active */}
        {isListening && (
          <div className="audio-wave-bars">
            <span className="bar bar1" />
            <span className="bar bar2" />
            <span className="bar bar3" />
            <span className="bar bar4" />
            <span className="bar bar5" />
            <span className="listening-label">Listening... Speak now</span>
          </div>
        )}

        {/* Clear / Reset Button */}
        {transcript && (
          <button
            type="button"
            className="btn-icon-subtle"
            onClick={resetTranscript}
            title="Clear transcript"
            disabled={disabled}
          >
            <RotateCcw size={16} />
            <span>Clear</span>
          </button>
        )}
      </div>

      {/* Warning / Error Message if mic denied or unsupported */}
      {error && (
        <div className="voice-alert-notice">
          <AlertCircle size={16} />
          <span>{error}</span>
        </div>
      )}

      {/* Editable Transcript Textarea (allows editing transcribed speech or direct typing fallback) */}
      <div className="transcript-box-wrapper">
        <div className="transcript-label-bar">
          <span className="label-text">
            <Edit3 size={14} /> Your English Answer (Editable):
          </span>
          <span className="hint-text">Review transcript before submitting</span>
        </div>
        <textarea
          className="transcript-textarea"
          rows={3}
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
        />
      </div>

      {/* Submit Button */}
      <div className="voice-submit-row">
        <span className="submit-hint">Tip: Press Ctrl+Enter to submit</span>
        <button
          type="button"
          className="btn-submit-answer"
          onClick={onSubmit}
          disabled={disabled || !transcript.trim()}
        >
          <Send size={16} />
          <span>Submit for AI Analysis</span>
        </button>
      </div>
    </div>
  );
}
