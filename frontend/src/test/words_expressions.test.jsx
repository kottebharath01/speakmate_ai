import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { WordsExpressions } from '../pages/WordsExpressions/WordsExpressions';

// Mock contexts and hooks
vi.mock('../context/AuthContext', () => ({
  useAuth: () => ({
    user: { id: 'u1', username: 'testuser' },
    profile: { xp: 100, streak: 3 },
    refreshProfile: vi.fn(),
  }),
}));

vi.mock('../context/TutorContext', () => ({
  useTutor: () => ({
    robotState: 'IDLE',
    tutorSpeech: '',
    setRobotState: vi.fn(),
    triggerCelebration: vi.fn(),
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
    startListening: vi.fn(),
    stopListening: vi.fn(),
    resetTranscript: vi.fn(),
    isSupported: true,
    error: null,
  }),
}));

// Mock API
vi.mock('../services/api', () => ({
  wordsExpressionsAPI: {
    getDailyFeatured: vi.fn().mockResolvedValue({
      data: {
        word_of_the_day: {
          id: 'w1',
          section: 'words',
          category: 'Daily Use Words',
          english_text: 'Diligent',
          telugu_text: 'కష్టపడి పనిచేసే',
          english_definition: 'Showing care and conscientiousness in work.',
          part_of_speech: 'adjective',
          level: 'INTERMEDIATE',
        },
        expression_of_the_day: {
          id: 'p1',
          section: 'phrases',
          category: 'Daily Conversations',
          english_text: 'Never mind',
          telugu_text: 'పోనీ లే / పర్లేదు',
          when_to_use: 'When telling someone not to worry about something trivial.',
          level: 'BEGINNER',
        },
        sentence_of_the_day: {
          id: 's1',
          section: 'sentences',
          category: 'Daily Life',
          english_text: 'I will call you when I reach there',
          telugu_text: 'నేను అక్కడికి చేరుకోగానే నీకు కాల్ చేస్తాను',
          sentence_structure: 'Future simple (will) + Time clause (when + present simple)',
          level: 'INTERMEDIATE',
        },
      },
    }),
    getItems: vi.fn().mockResolvedValue({
      data: {
        items: [
          {
            id: 'item1',
            section: 'words',
            category: 'Daily Use Words',
            english_text: 'Reluctant',
            telugu_text: 'ఇష్టం లేని / అయిష్టంగా ఉన్న',
            telugu_transliteration: 'ishtaṁ lēni',
            english_definition: 'Unwilling and hesitant.',
            when_to_use: 'When someone hesitates to do something.',
            level: 'INTERMEDIATE',
            is_learned: false,
            is_bookmarked: false,
          },
        ],
        total: 1,
        page: 1,
        page_size: 20,
        total_pages: 1,
      },
    }),
    getCategories: vi.fn().mockResolvedValue({
      data: [
        { name: 'Daily Use Words', count: 12 },
        { name: 'Workplace Vocabulary', count: 8 },
      ],
    }),
    getProgress: vi.fn().mockResolvedValue({
      data: {
        learned_count: 7,
        bookmarked_count: 3,
        total_items: 50,
      },
    }),
    getRandom: vi.fn().mockResolvedValue({
      data: {
        id: 'rand1',
        english_text: 'Hang in there',
        telugu_text: 'ఓపిక పట్టు',
        level: 'BEGINNER',
      },
    }),
    getExercises: vi.fn().mockResolvedValue({
      data: [
        {
          id: 'ex1',
          exercise_type: 'multiple_choice',
          question: 'How do you say "పోనీ లే" naturally in English?',
          telugu_prompt: 'పోనీ లే',
          options: ['Never mind', 'Get lost', 'Go away', 'Shut up'],
          level: 'BEGINNER',
        },
      ],
    }),
    toggleBookmark: vi.fn().mockResolvedValue({
      data: { is_bookmarked: true },
    }),
    toggleLearned: vi.fn().mockResolvedValue({
      data: { is_learned: true },
    }),
    checkSentence: vi.fn().mockResolvedValue({
      data: {
        is_correct: true,
        score: 95,
        feedback: 'Great sentence formation and natural usage!',
        corrected_sentence: 'I was reluctant to join the meeting.',
        encouragement: 'Keep up the fantastic work!',
      },
    }),
  },
}));

describe('Words & Expressions Module', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders page header and daily showcase correctly', async () => {
    render(<WordsExpressions />);

    // Header checks
    expect(screen.getByText('Words & Expressions')).toBeInTheDocument();
    expect(screen.getByText(/Telugu to Natural English/i)).toBeInTheDocument();

    // Stats checks
    await waitFor(() => {
      expect(screen.getByText('Learned')).toBeInTheDocument();
      expect(screen.getByText('Saved')).toBeInTheDocument();
      expect(screen.getByText('Surprise Me')).toBeInTheDocument();
    });

    // Daily showcase cards check
    await waitFor(() => {
      expect(screen.getByText('WORD OF THE DAY')).toBeInTheDocument();
      expect(screen.getByText('Diligent')).toBeInTheDocument();
      expect(screen.getByText('EXPRESSION OF THE DAY')).toBeInTheDocument();
      expect(screen.getByText('Never mind')).toBeInTheDocument();
    });
  });

  it('renders the 4 learning section tabs plus Quizzes & Bookmarks', async () => {
    render(<WordsExpressions />);

    await waitFor(() => {
      expect(screen.getByText('Individual Words')).toBeInTheDocument();
      expect(screen.getByText('Daily Phrases & Expressions')).toBeInTheDocument();
      expect(screen.getByText('Complete Telugu-to-English Sentences')).toBeInTheDocument();
      expect(screen.getByText('Situation-Based Expressions')).toBeInTheDocument();
      expect(screen.getByText('Interactive Quizzes & Practice')).toBeInTheDocument();
      expect(screen.getByText('My Saved & Learned')).toBeInTheDocument();
    });
  });

  it('displays word cards with Telugu and English conversions', async () => {
    render(<WordsExpressions />);

    await waitFor(() => {
      expect(screen.getByText('Reluctant')).toBeInTheDocument();
      expect(screen.getByText(/ఇష్టం లేని/)).toBeInTheDocument();
      expect(screen.getByText('Practice with AI Tutor')).toBeInTheDocument();
    });
  });

  it('switches to quiz section when clicking Interactive Quizzes tab', async () => {
    render(<WordsExpressions />);

    const quizTab = screen.getByText('Interactive Quizzes & Practice');
    fireEvent.click(quizTab);

    await waitFor(() => {
      expect(screen.getByText('PRACTICE QUIZ')).toBeInTheDocument();
      expect(screen.getByText(/Test Your Telugu-to-English Mastery/i)).toBeInTheDocument();
      expect(screen.getByText(/How do you say "పోనీ లే" naturally in English/i)).toBeInTheDocument();
    });
  });
});
