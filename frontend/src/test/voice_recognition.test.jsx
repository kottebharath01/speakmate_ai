import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';

describe('useSpeechRecognition Hook (Voice Capture & Edge Cases)', () => {
  let lastInstance = null;
  let cancelMock;

  beforeEach(() => {
    lastInstance = null;
    cancelMock = vi.fn();

    window.speechSynthesis = {
      cancel: cancelMock,
      speak: vi.fn(),
      getVoices: () => [],
    };

    class MockSpeechRecognition {
      constructor() {
        this.continuous = false;
        this.interimResults = false;
        this.lang = '';
        this.onstart = null;
        this.onresult = null;
        this.onerror = null;
        this.onend = null;
        lastInstance = this;
      }
      start() {
        if (this.onstart) this.onstart();
      }
      stop() {
        if (this.onend) this.onend();
      }
      abort() {
        // silent abort
      }
    }

    window.SpeechRecognition = MockSpeechRecognition;
  });

  it('stops active AI TTS and streams interim voice transcript live before finalization', () => {
    const { result } = renderHook(() => useSpeechRecognition());

    act(() => {
      result.current.startListening();
    });

    // AI Tutor TTS must be cancelled immediately when mic starts
    expect(cancelMock).toHaveBeenCalled();
    expect(result.current.isListening).toBe(true);

    // Emit interim (non-final) spoken word while user is still speaking
    act(() => {
      lastInstance.onresult({
        resultIndex: 0,
        results: [
          Object.assign([{ transcript: 'postpone', confidence: 0.9 }], { isFinal: false }),
        ],
      });
    });

    // Transcript must ALREADY show live speech so user sees it & can submit
    expect(result.current.transcript).toBe('postpone');
    expect(result.current.interimTranscript).toBe('postpone');

    // Stopping mic promotes uncommitted interim text instead of erasing it!
    act(() => {
      result.current.stopListening();
    });

    expect(result.current.isListening).toBe(false);
    expect(result.current.transcript).toBe('postpone');
  });

  it('prevents duplicate final segments and allows clean repeated recordings', () => {
    const { result } = renderHook(() => useSpeechRecognition());

    act(() => {
      result.current.startListening();
    });

    const firstInst = lastInstance;

    // Simulate Android Chrome duplicate final segments quirk
    act(() => {
      firstInst.onresult({
        resultIndex: 0,
        results: [
          Object.assign([{ transcript: 'I would like to buy a shirt', confidence: 0.9 }], { isFinal: true }),
          Object.assign([{ transcript: 'I would like to buy a shirt', confidence: 0.0 }], { isFinal: true }),
        ],
      });
    });

    expect(result.current.transcript).toBe('I would like to buy a shirt');

    act(() => {
      result.current.stopListening();
    });

    // Start a second recording -> creates a fresh instance cleanly without InvalidStateError
    act(() => {
      result.current.startListening();
    });

    expect(lastInstance).not.toBe(firstInst);
    expect(result.current.isListening).toBe(true);
  });

  it('surfaces clear error message when mic access is denied or no speech heard', () => {
    const { result } = renderHook(() => useSpeechRecognition());

    act(() => {
      result.current.startListening();
    });

    act(() => {
      lastInstance.onerror({ error: 'not-allowed' });
    });

    expect(result.current.isListening).toBe(false);
    expect(result.current.error).toMatch(/Microphone access was blocked/i);
  });
});
