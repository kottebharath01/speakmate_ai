import { useState, useEffect, useRef, useCallback } from 'react';

// Global tracker ensures two components never fight over the microphone simultaneously
let activeGlobalRecognition = null;

function stopGlobalActiveRecognition() {
  if (activeGlobalRecognition) {
    try {
      activeGlobalRecognition.abort();
    } catch (e) {}
    activeGlobalRecognition = null;
  }
}

export function useSpeechRecognition() {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscriptState] = useState('');
  const [interimTranscript, setInterimTranscript] = useState('');
  const [error, setError] = useState(null);
  const [isSupported, setIsSupported] = useState(true);

  const recognitionRef = useRef(null);
  const finalTextRef = useRef('');
  const interimTextRef = useRef('');
  const baseTextBeforeStartRef = useRef('');

  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setIsSupported(false);
      setError('Voice input is not supported in this browser. Please use Chrome/Edge or type below.');
    }

    return () => {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.abort();
        } catch (e) {}
        if (activeGlobalRecognition === recognitionRef.current) {
          activeGlobalRecognition = null;
        }
      }
    };
  }, []);

  // Keep refs in sync whenever user edits text manually
  const setTranscript = useCallback((value) => {
    const next = typeof value === 'function' ? value(finalTextRef.current) : value;
    const safeText = next || '';
    finalTextRef.current = safeText;
    interimTextRef.current = '';
    baseTextBeforeStartRef.current = safeText;
    setTranscriptState(safeText);
    setInterimTranscript('');
  }, []);

  const resetTranscript = useCallback(() => {
    finalTextRef.current = '';
    interimTextRef.current = '';
    baseTextBeforeStartRef.current = '';
    setTranscriptState('');
    setInterimTranscript('');
    setError(null);
  }, []);

  const startListening = useCallback(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setIsSupported(false);
      setError('Voice input is not supported in this browser. Please type your answer below.');
      return;
    }

    // 1. Stop AI voice output so speakers do not talk over the microphone
    if ('speechSynthesis' in window) {
      try {
        window.speechSynthesis.cancel();
      } catch (e) {}
    }

    // 2. Cleanly release any previous SpeechRecognition lock across components
    stopGlobalActiveRecognition();
    if (recognitionRef.current) {
      try {
        recognitionRef.current.abort();
      } catch (e) {}
    }

    setError(null);
    baseTextBeforeStartRef.current = finalTextRef.current.trim();

    try {
      // Create a fresh instance per tap so repeated clicks never fail with InvalidStateError
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-US';
      recognition.maxAlternatives = 1;

      recognition.onstart = () => {
        setIsListening(true);
        setError(null);
      };

      recognition.onresult = (event) => {
        let sessionFinals = '';
        let sessionInterim = '';
        let lastFinal = '';

        for (let i = 0; i < event.results.length; i++) {
          const item = event.results[i];
          const rawText = (item[0]?.transcript || '').trim();
          if (!rawText) continue;

          if (item.isFinal) {
            // Avoid Android Chrome duplicate final segment bug
            if (rawText !== lastFinal) {
              sessionFinals = sessionFinals ? `${sessionFinals} ${rawText}` : rawText;
              lastFinal = rawText;
            }
          } else {
            sessionInterim = sessionInterim ? `${sessionInterim} ${rawText}` : rawText;
          }
        }

        const mergedFinals = [baseTextBeforeStartRef.current, sessionFinals]
          .filter(Boolean)
          .join(' ')
          .trim();

        const liveFull = [mergedFinals, sessionInterim]
          .filter(Boolean)
          .join(' ')
          .trim();

        finalTextRef.current = mergedFinals;
        interimTextRef.current = sessionInterim;
        setInterimTranscript(sessionInterim);
        // Expose live interim + final text immediately in transcript so UI updates as user speaks
        setTranscriptState(liveFull);
      };

      recognition.onerror = (event) => {
        console.warn('Speech recognition error:', event.error);
        if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
          setError('Microphone access was blocked. Click the lock/mic icon in your browser address bar to allow microphone access.');
        } else if (event.error === 'audio-capture') {
          setError('No working microphone found. Check your mic connection or type your answer below.');
        } else if (event.error === 'no-speech') {
          setError('No voice was detected. Speak clearly closer to your mic or type below.');
        } else if (event.error === 'network') {
          setError('Speech service network error. Ensure internet connection or type your answer below.');
        } else if (event.error !== 'aborted') {
          setError(`Voice input paused (${event.error}). You can tap the mic again or type below.`);
        }
        setIsListening(false);
      };

      recognition.onend = () => {
        // Commit any pending interim text cleanly so spoken words are never lost on stop/pause
        const committed = [finalTextRef.current, interimTextRef.current]
          .filter(Boolean)
          .join(' ')
          .trim();
        finalTextRef.current = committed;
        interimTextRef.current = '';
        setTranscriptState(committed);
        setInterimTranscript('');
        setIsListening(false);
        if (activeGlobalRecognition === recognition) {
          activeGlobalRecognition = null;
        }
      };

      recognitionRef.current = recognition;
      activeGlobalRecognition = recognition;
      recognition.start();
    } catch (err) {
      console.warn('Start recognition error:', err);
      setIsListening(false);
      setError('Could not start microphone. Ensure mic permissions are allowed or type below.');
    }
  }, []);

  const stopListening = useCallback(() => {
    if (!recognitionRef.current) return;
    try {
      recognitionRef.current.stop();
    } catch (err) {
      console.warn('Stop recognition error:', err);
      setIsListening(false);
    }
  }, []);

  return {
    isListening,
    transcript,
    setTranscript,
    interimTranscript,
    error,
    isSupported,
    startListening,
    stopListening,
    resetTranscript,
  };
}
