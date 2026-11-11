import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { WordsExpressions } from '../pages/WordsExpressions/WordsExpressions';
import { wordsExpressionsAPI } from '../services/api';

vi.mock('../context/AuthContext', () => ({
  useAuth: () => ({
    user: { id: 1, username: 'learner' },
    profile: { streak_count: 1, longest_streak: 3, total_points: 20 },
    refreshProfile: vi.fn(),
  }),
}));

vi.mock('../context/TutorContext', () => ({
  useTutor: () => ({
    robotState: 'IDLE',
    currentMessage: 'Ready to practice!',
    setRobotState: vi.fn(),
    triggerCelebration: vi.fn(),
    voiceEnabled: false,
    setVoiceEnabled: vi.fn(),
    isSpeaking: false,
  }),
}));

vi.mock('../hooks/useSpeechSynthesis', () => ({
  useSpeechSynthesis: () => ({
    speak: vi.fn(),
    isSpeaking: false,
  }),
}));

vi.mock('../hooks/useSpeechRecognition', () => ({
  useSpeechRecognition: () => ({
    isListening: false,
    transcript: '',
    setTranscript: vi.fn(),
    startListening: vi.fn(),
    stopListening: vi.fn(),
    resetTranscript: vi.fn(),
    isSupported: true,
    error: null,
  }),
}));

vi.mock('../services/api', () => ({
  wordsExpressionsAPI: {
    getModesSummary: vi.fn().mockResolvedValue({
      data: {
        modes: [
          {
            mode: 'words',
            label: 'Words',
            description: 'Everyday words',
            total_items: 60,
            remaining_new_items: 58,
            categories: [{ name: 'Daily Use Words', total_count: 10, remaining_new_count: 10 }],
          },
          {
            mode: 'expressions',
            label: 'Expressions',
            description: 'Daily expressions',
            total_items: 36,
            remaining_new_items: 36,
            categories: [{ name: 'Daily Conversations', total_count: 8, remaining_new_count: 8 }],
          },
          {
            mode: 'situation_expressions',
            label: 'Situation Expressions',
            description: 'Situation phrases',
            total_items: 30,
            remaining_new_items: 30,
            categories: [{ name: 'Office', total_count: 3, remaining_new_count: 3 }],
          },
        ],
        total_learned_by_user: 2,
      },
    }),
    getActiveSession: vi.fn().mockResolvedValue({ data: null }),
    startSession: vi.fn().mockResolvedValue({
      data: {
        id: 101,
        mode: 'words',
        category: 'All',
        daily_target: 10,
        completed_count: 0,
        current_index: 0,
        status: 'active',
        is_revision: false,
        local_date: '2026-11-11',
        current_item: {
          id: 1,
          mode: 'words',
          category: 'Daily Use Words',
          level: 'BEGINNER',
          telugu_text: 'వాయిదా వేయడం',
          telugu_transliteration: 'Vaayida veyadam',
          prompt_question: 'How do you say this in English?',
        },
        pending_attempt: null,
        started_at: '2026-11-11T10:00:00Z',
      },
    }),
    submitSessionAnswer: vi.fn(),
    submitSessionRepeat: vi.fn(),
    getSessionHistory: vi.fn().mockResolvedValue({
      data: [
        {
          id: 99,
          mode: 'words',
          category: 'All',
          daily_target: 10,
          completed_count: 10,
          status: 'completed',
          is_revision: false,
          local_date: '2026-11-10',
          started_at: '2026-11-10T09:00:00Z',
          completed_at: '2026-11-10T09:15:00Z',
          attempts: [],
        },
      ],
    }),
    getItems: vi.fn().mockResolvedValue({ data: { items: [], total: 0, page: 1, total_pages: 1 } }),
    abandonSession: vi.fn().mockResolvedValue({ data: {} }),
  },
}));

describe('Words & Expressions Guided Module', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('displays the 3 learning modes, target picker, and launches guided session', async () => {
    render(<WordsExpressions />);

    await waitFor(() => {
      expect(screen.getByText('1. Select Learning Mode')).toBeInTheDocument();
      expect(screen.getByText('Words')).toBeInTheDocument();
      expect(screen.getByText('Expressions')).toBeInTheDocument();
      expect(screen.getByText('Situation Expressions')).toBeInTheDocument();
    });

    // Target default is 10 -> click Start button
    const startBtn = screen.getByRole('button', { name: /Start 10-Word Session/i });
    fireEvent.click(startBtn);

    await waitFor(() => {
      expect(wordsExpressionsAPI.startSession).toHaveBeenCalledWith(
        expect.objectContaining({ mode: 'words', daily_target: 10 })
      );
      expect(screen.getByTestId('words-telugu-prompt')).toHaveTextContent('వాయిదా వేయడం');
      expect(screen.getByText(/"How do you say this in English\?"/i)).toBeInTheDocument();
    });
  });

  it('handles incorrect answer -> enforces 1/2 -> 2/2 repetitions workflow', async () => {
    wordsExpressionsAPI.submitSessionAnswer.mockResolvedValueOnce({
      data: {
        attempt_id: 55,
        is_correct: false,
        accepted_answer: 'Postpone',
        valid_alternatives: ['Postpone', 'put off', 'delay'],
        evaluation_feedback: "Not quite. The natural English is 'Postpone'.",
        correction_details: 'Postpone means moving an event to a later time.',
        example_sentence: 'We had to postpone the meeting.',
        repetition_required: true,
        repetitions_completed: 0,
        repetitions_required: 2,
        item_completed: false,
        session_completed: false,
        completed_count: 0,
        daily_target: 10,
      },
    });

    wordsExpressionsAPI.submitSessionRepeat
      .mockResolvedValueOnce({
        data: {
          attempt_id: 55,
          is_successful: true,
          accuracy_score: 100,
          feedback: 'First repetition (1/2) complete!',
          accepted_answer: 'Postpone',
          repetitions_completed: 1,
          repetitions_required: 2,
          item_completed: false,
          session_completed: false,
          completed_count: 0,
          daily_target: 10,
        },
      })
      .mockResolvedValueOnce({
        data: {
          attempt_id: 55,
          is_successful: true,
          accuracy_score: 100,
          feedback: 'Both repetitions (2/2) completed cleanly!',
          accepted_answer: 'Postpone',
          repetitions_completed: 2,
          repetitions_required: 2,
          item_completed: true,
          session_completed: false,
          completed_count: 1,
          daily_target: 10,
          next_item: {
            id: 2,
            mode: 'words',
            category: 'Daily Use Words',
            level: 'BEGINNER',
            telugu_text: 'సౌకర్యవంతమైన',
            prompt_question: 'How do you say this in English?',
          },
        },
      });

    render(<WordsExpressions />);
    await waitFor(() => expect(screen.getByRole('button', { name: /Start 10-Word Session/i })).toBeInTheDocument());
    fireEvent.click(screen.getByRole('button', { name: /Start 10-Word Session/i }));

    await waitFor(() => expect(screen.getByTestId('words-telugu-prompt')).toBeInTheDocument());

    // Submit wrong answer
    const answerInput = screen.getByLabelText('English answer input');
    fireEvent.change(answerInput, { target: { value: 'wrong guess' } });
    fireEvent.click(screen.getByRole('button', { name: /^Submit$/i }));

    // Verify Correction + 2-repetition requirement appears
    await waitFor(() => {
      expect(screen.getByTestId('words-correction-panel')).toBeInTheDocument();
      expect(screen.getByTestId('words-correct-answer')).toHaveTextContent('"Postpone"');
      expect(screen.getByTestId('rep-step-1')).toHaveTextContent('0/2');
    });

    // Submit 1st repetition -> 1/2
    const repInput = screen.getByLabelText('Repetition input');
    fireEvent.change(repInput, { target: { value: 'Postpone' } });
    fireEvent.click(screen.getByRole('button', { name: /Verify \(1\/2\)/i }));

    await waitFor(() => {
      expect(screen.getByTestId('rep-step-1')).toHaveTextContent('1/2');
      expect(screen.getByRole('button', { name: /Verify \(2\/2\)/i })).toBeInTheDocument();
    });

    // Submit 2nd repetition -> 2/2
    fireEvent.change(screen.getByLabelText('Repetition input'), { target: { value: 'Postpone' } });
    fireEvent.click(screen.getByRole('button', { name: /Verify \(2\/2\)/i }));

    await waitFor(() => {
      expect(screen.getByTestId('rep-step-2')).toHaveTextContent('2/2');
    });
  });

  it('switches to Learning History tab and renders saved sessions', async () => {
    render(<WordsExpressions />);

    const histTab = screen.getByRole('button', { name: /Learning History/i });
    fireEvent.click(histTab);

    await waitFor(() => {
      expect(screen.getByTestId('words-history-view')).toBeInTheDocument();
      expect(screen.getByText('10 / 10 Items')).toBeInTheDocument();
      expect(screen.getByText(/Completed/i)).toBeInTheDocument();
    });
  });
});
