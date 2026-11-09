import React, { createContext, useContext, useState, useCallback } from 'react';
import confetti from 'canvas-confetti';
import { useSpeechSynthesis } from '../hooks/useSpeechSynthesis';

const TutorContext = createContext(null);

const DEFAULT_MESSAGES = {
  IDLE: 'Hello! Ready to practice English speaking?',
  GREETING: "Welcome to SpeakMate AI! I'm your personal AI English Tutor.",
  EXPLAINING: 'Here is your situation in Telugu. Listen carefully and get ready!',
  LISTENING: "I'm listening. Speak naturally at your own pace!",
  THINKING: 'Analyzing your grammar, vocabulary, and communication clarity...',
  TEACHING: "Let's improve your English together! Here is your feedback.",
  SUCCESS: 'Fantastic! You corrected the sentence and spoke with confidence!',
};

export function TutorProvider({ children }) {
  const [robotState, setRobotStateInternal] = useState('IDLE');
  const [customMessage, setCustomMessage] = useState(null);
  const [voiceEnabled, setVoiceEnabled] = useState(true);

  const { speak, stop, isSpeaking } = useSpeechSynthesis();

  const setRobotState = useCallback(
    (state, message = null) => {
      setRobotStateInternal(state);
      setCustomMessage(message);

      if (voiceEnabled && message) {
        speak(message);
      }
    },
    [voiceEnabled, speak]
  );

  const triggerCelebration = useCallback(() => {
    confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#3b82f6', '#6366f1', '#10b981', '#fbbf24', '#ec4899'],
    });
  }, []);

  const currentMessage = customMessage || DEFAULT_MESSAGES[robotState] || DEFAULT_MESSAGES.IDLE;

  return (
    <TutorContext.Provider
      value={{
        robotState,
        setRobotState,
        currentMessage,
        setCustomMessage,
        voiceEnabled,
        setVoiceEnabled,
        speak,
        stop,
        isSpeaking,
        triggerCelebration,
      }}
    >
      {children}
    </TutorContext.Provider>
  );
}

export function useTutor() {
  const context = useContext(TutorContext);
  if (!context) {
    throw new Error('useTutor must be used within a TutorProvider');
  }
  return context;
}
