import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { SituationPractice } from '../pages/SituationPractice';
import { StreakCalendar } from '../components/StreakCalendar';
import { situationsAPI } from '../services/api';

vi.mock('../context/AuthContext', () => ({
  useAuth: () => ({
    user: { id: 1, username: 'learner' },
    profile: { streak_count: 2, longest_streak: 4, total_points: 50 },
    refreshProfile: vi.fn(),
  }),
}));

vi.mock('../context/TutorContext', () => ({
  useTutor: () => ({
    robotState: 'IDLE',
    currentMessage: 'Ready to practice speaking!',
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
  situationsAPI: {
    getCategoryStats: vi.fn().mockResolvedValue({
      data: [
        { name: 'Talking with Managers', total_count: 3, remaining_new_count: 3 },
        { name: 'Shopping', total_count: 3, remaining_new_count: 3 },
      ],
    }),
    getActiveSession: vi.fn().mockResolvedValue({ data: null }),
    startSession: vi.fn().mockResolvedValue({
      data: {
        id: 201,
        category: 'All',
        daily_target: 5,
        completed_count: 0,
        current_index: 0,
        status: 'active',
        is_revision: false,
        local_date: '2026-11-11',
        current_situation: {
          id: 11,
          title: 'Asking Manager for Permission to Leave Early',
          category: 'Talking with Managers',
          level: 'INTERMEDIATE',
          telugu_explanation: 'ఈరోజు త్వరగా వెళ్ళాలని మేనేజర్‌ని అడగడం.',
          telugu_transliteration: 'Eeroju thvaraga vellalani manager ni adagadam.',
          english_prompt: 'How would you ask your manager for permission to leave early today?',
          is_system: true,
          created_at: '2026-11-11T10:00:00Z',
        },
        pending_attempt: null,
        started_at: '2026-11-11T10:00:00Z',
      },
    }),
    getSessionHistory: vi.fn().mockResolvedValue({
      data: [
        {
          id: 150,
          category: 'All',
          daily_target: 5,
          completed_count: 5,
          status: 'completed',
          is_revision: false,
          local_date: '2026-11-10',
          started_at: '2026-11-10T10:00:00Z',
          completed_at: '2026-11-10T10:25:00Z',
          attempts: [],
        },
      ],
    }),
    submitSessionAnswer: vi.fn(),
    submitSessionRepeat: vi.fn(),
    abandonSession: vi.fn().mockResolvedValue({ data: {} }),
  },
}));

describe('Speaking Practice Guided Workflow', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('starts a 5-situation guided session and displays Telugu explanation + English question', async () => {
    render(<SituationPractice />);

    await waitFor(() => {
      expect(screen.getByText('1. Situation Category')).toBeInTheDocument();
      expect(screen.getByText('2. Today\'s Speaking Target')).toBeInTheDocument();
    });

    const startBtn = screen.getByRole('button', { name: /Start 5-Situation Session/i });
    fireEvent.click(startBtn);

    await waitFor(() => {
      expect(situationsAPI.startSession).toHaveBeenCalledWith(
        expect.objectContaining({ category: 'All', daily_target: 5 })
      );
      expect(screen.getByTestId('speaking-situation-title')).toHaveTextContent(
        'Asking Manager for Permission to Leave Early'
      );
      expect(screen.getByText(/ఈరోజు త్వరగా వెళ్ళాలని/i)).toBeInTheDocument();
    });
  });

  it('renders Speaking Practice history cleanly', async () => {
    render(<SituationPractice />);

    fireEvent.click(screen.getByRole('button', { name: /Practice History/i }));

    await waitFor(() => {
      expect(screen.getByTestId('speaking-history-view')).toBeInTheDocument();
      expect(screen.getByText('5 / 5 Situations')).toBeInTheDocument();
    });
  });
});

describe('StreakCalendar Component', () => {
  it('renders current streak, longest streak, active days and 28-day calendar', () => {
    render(
      <StreakCalendar
        streakData={{
          current_streak: 3,
          longest_streak: 7,
          completed_days_count: 10,
          calendar_days: [],
        }}
      />
    );

    expect(screen.getByTestId('current-streak-value')).toHaveTextContent('3 Days');
    expect(screen.getByTestId('longest-streak-value')).toHaveTextContent('7 Days');
    expect(screen.getByText('10 Days')).toBeInTheDocument();
  });
});
