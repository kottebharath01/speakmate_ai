import React from 'react';
import { useTutor } from '../context/TutorContext';
import { Volume2, VolumeX, Sparkles, Brain, Mic, MessageSquare } from 'lucide-react';

export function RobotTutor({ size = 'medium', showMessage = true }) {
  const { robotState, currentMessage, voiceEnabled, setVoiceEnabled, isSpeaking } = useTutor();

  // Size dimensions
  const scale = size === 'small' ? 0.7 : size === 'large' ? 1.25 : 1.0;
  const width = 160 * scale;
  const height = 180 * scale;

  // Eye and expression configurations per robot state
  const isBlinking = robotState === 'IDLE' || robotState === 'GREETING';
  const isListening = robotState === 'LISTENING';
  const isThinking = robotState === 'THINKING';
  const isSuccess = robotState === 'SUCCESS';
  const isTeaching = robotState === 'TEACHING';

  return (
    <div className="robot-tutor-container">
      {/* Speech / Contextual Bubble */}
      {showMessage && (
        <div className={`tutor-speech-bubble state-${robotState.toLowerCase()}`}>
          <div className="bubble-header">
            <span className="state-badge">
              {robotState === 'LISTENING' && <Mic size={12} className="pulse-icon" />}
              {robotState === 'THINKING' && <Brain size={12} className="spin-icon" />}
              {robotState === 'SUCCESS' && <Sparkles size={12} />}
              {robotState}
            </span>
            <button
              className="voice-toggle-btn"
              onClick={() => setVoiceEnabled(!voiceEnabled)}
              title={voiceEnabled ? 'Mute AI Voice' : 'Enable AI Voice'}
              aria-label="Toggle AI Voice"
            >
              {voiceEnabled ? <Volume2 size={14} /> : <VolumeX size={14} />}
            </button>
          </div>
          <p className="bubble-text">{currentMessage}</p>
          <div className="bubble-arrow" />
        </div>
      )}

      {/* SVG 3D-Styled Friendly Blue & White Robot Character */}
      <div className={`robot-figure ${robotState.toLowerCase()}`}>
        <svg
          width={width}
          height={height}
          viewBox="0 0 160 180"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="robot-svg"
        >
          <defs>
            {/* Gradients for modern 3D lighting */}
            <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#ffffff" />
              <stop offset="60%" stopColor="#e2e8f0" />
              <stop offset="100%" stopColor="#cbd5e1" />
            </linearGradient>

            <linearGradient id="primaryBlueGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#60a5fa" />
              <stop offset="50%" stopColor="#3b82f6" />
              <stop offset="100%" stopColor="#1d4ed8" />
            </linearGradient>

            <linearGradient id="visorGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#0f172a" />
              <stop offset="100%" stopColor="#1e293b" />
            </linearGradient>

            <linearGradient id="cyanGlow" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#38bdf8" />
              <stop offset="100%" stopColor="#06b6d4" />
            </linearGradient>

            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>

            <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
              <feDropShadow dx="0" dy="6" stdDeviation="6" floodColor="#1e3a8a" floodOpacity="0.18" />
            </filter>
          </defs>

          {/* Floating Shadow */}
          <ellipse cx="80" cy="170" rx="42" ry="7" fill="#94a3b8" opacity="0.35" className="robot-ground-shadow" />

          {/* Robot Floating Body Group */}
          <g className="robot-body-group">
            {/* Antenna with LED sphere */}
            <path d="M80 32 L80 18" stroke="#3b82f6" strokeWidth="4" strokeLinecap="round" />
            <circle
              cx="80"
              cy="14"
              r="7"
              fill={isListening ? '#ef4444' : isThinking ? '#f59e0b' : isSuccess ? '#10b981' : '#38bdf8'}
              filter="url(#glow)"
              className="antenna-light"
            />

            {/* Left and Right Ears / Headset cushions */}
            <rect x="22" y="52" width="10" height="24" rx="4" fill="url(#primaryBlueGrad)" />
            <rect x="128" y="52" width="10" height="24" rx="4" fill="url(#primaryBlueGrad)" />

            {/* Head: Rounded glossy 3D head */}
            <rect
              x="28"
              y="32"
              width="104"
              height="72"
              rx="24"
              fill="url(#bodyGrad)"
              filter="url(#shadow)"
              stroke="#e2e8f0"
              strokeWidth="1.5"
            />

            {/* High-Tech Visor Screen */}
            <rect
              x="38"
              y="44"
              width="84"
              height="48"
              rx="16"
              fill="url(#visorGrad)"
              stroke="#334155"
              strokeWidth="2"
            />

            {/* Eyes */}
            {isSuccess ? (
              // Happy Arc Eyes
              <g stroke="#10b981" strokeWidth="3.5" strokeLinecap="round" filter="url(#glow)">
                <path d="M52 64 Q60 55 68 64" />
                <path d="M92 64 Q100 55 108 64" />
              </g>
            ) : isThinking ? (
              // Thinking Pulsing Concentric Eyes
              <g filter="url(#glow)">
                <circle cx="60" cy="62" r="7" fill="#fbbf24" className="thinking-eye-left" />
                <circle cx="100" cy="62" r="7" fill="#fbbf24" className="thinking-eye-right" />
              </g>
            ) : isListening ? (
              // Listening Glowing Wide Eyes
              <g filter="url(#glow)">
                <circle cx="60" cy="62" r="8" fill="#38bdf8" />
                <circle cx="60" cy="60" r="3" fill="#ffffff" />
                <circle cx="100" cy="62" r="8" fill="#38bdf8" />
                <circle cx="100" cy="60" r="3" fill="#ffffff" />
              </g>
            ) : (
              // Normal Friendly Eyes (with blinking animation)
              <g className={isBlinking ? 'blinking-eyes' : ''} filter="url(#glow)">
                <rect x="52" y="55" width="14" height="15" rx="7" fill="#38bdf8" />
                <circle cx="56" cy="59" r="2.5" fill="#ffffff" />
                <rect x="94" y="55" width="14" height="15" rx="7" fill="#38bdf8" />
                <circle cx="98" cy="59" r="2.5" fill="#ffffff" />
              </g>
            )}

            {/* Mouth / Voice Waveform */}
            {isSpeaking || robotState === 'TEACHING' ? (
              // Animated Speaking Mouth Waveform
              <g stroke="#38bdf8" strokeWidth="2.5" strokeLinecap="round" className="speaking-mouth">
                <line x1="66" y1="78" x2="66" y2="82" />
                <line x1="73" y1="76" x2="73" y2="84" />
                <line x1="80" y1="75" x2="80" y2="85" />
                <line x1="87" y1="76" x2="87" y2="84" />
                <line x1="94" y1="78" x2="94" y2="82" />
              </g>
            ) : isListening ? (
              // Listening Audio Wave
              <g stroke="#ef4444" strokeWidth="2.5" strokeLinecap="round" className="listening-wave">
                <line x1="68" y1="80" x2="72" y2="80" />
                <line x1="76" y1="78" x2="84" y2="78" />
                <line x1="88" y1="80" x2="92" y2="80" />
              </g>
            ) : (
              // Friendly Gentle Smile
              <path
                d="M72 79 Q80 84 88 79"
                stroke="#38bdf8"
                strokeWidth="2.5"
                strokeLinecap="round"
                fill="none"
              />
            )}

            {/* Neck Joint */}
            <rect x="72" y="104" width="16" height="8" rx="2" fill="#64748b" />

            {/* Torso / Body */}
            <rect
              x="42"
              y="112"
              width="76"
              height="48"
              rx="18"
              fill="url(#bodyGrad)"
              filter="url(#shadow)"
              stroke="#e2e8f0"
              strokeWidth="1.5"
            />

            {/* Chest Core Emblem / Glowing Heart */}
            <rect
              x="58"
              y="122"
              width="44"
              height="24"
              rx="10"
              fill="url(#primaryBlueGrad)"
            />
            <circle
              cx="80"
              cy="134"
              r="6"
              fill="#38bdf8"
              filter="url(#glow)"
              className="chest-pulse"
            />

            {/* Hands / Floating Arms */}
            <rect x="22" y="118" width="12" height="28" rx="6" fill="url(#primaryBlueGrad)" className="left-arm" />
            <rect x="126" y="118" width="12" height="28" rx="6" fill="url(#primaryBlueGrad)" className="right-arm" />
          </g>
        </svg>
      </div>
    </div>
  );
}
