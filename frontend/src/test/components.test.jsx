import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TutorProvider } from '../context/TutorContext';
import { RobotTutor } from '../components/RobotTutor';
import { DifficultyBadge } from '../components/DifficultyBadge';
import { VoiceInput } from '../components/VoiceInput';
import { FeedbackCard } from '../components/FeedbackCard';

describe('RobotTutor Component', () => {
  it('renders successfully with default speech message', () => {
    render(
      <TutorProvider>
        <RobotTutor />
      </TutorProvider>
    );
    expect(screen.getByText(/Ready to practice English speaking/i)).toBeInTheDocument();
  });
});

describe('DifficultyBadge Component', () => {
  it('renders Beginner badge correctly', () => {
    render(<DifficultyBadge level="BEGINNER" />);
    expect(screen.getByText('Beginner')).toBeInTheDocument();
  });

  it('renders Intermediate and Advanced badges', () => {
    const { rerender } = render(<DifficultyBadge level="INTERMEDIATE" />);
    expect(screen.getByText('Intermediate')).toBeInTheDocument();

    rerender(<DifficultyBadge level="ADVANCED" />);
    expect(screen.getByText('Advanced')).toBeInTheDocument();
  });
});

describe('VoiceInput Component', () => {
  it('renders microphone toggle and editable textarea', () => {
    const setTranscript = () => {};
    render(
      <VoiceInput
        transcript="I want to buy a blue shirt"
        setTranscript={setTranscript}
        isListening={false}
        startListening={() => {}}
        stopListening={() => {}}
        resetTranscript={() => {}}
        error={null}
        isSupported={true}
        onSubmit={() => {}}
      />
    );

    expect(screen.getByText(/Tap to Speak English/i)).toBeInTheDocument();
    expect(screen.getByDisplayValue('I want to buy a blue shirt')).toBeInTheDocument();
    expect(screen.getByText(/Submit for AI Analysis/i)).toBeInTheDocument();
  });

  it('shows listening state when active', () => {
    render(
      <VoiceInput
        transcript=""
        setTranscript={() => {}}
        isListening={true}
        startListening={() => {}}
        stopListening={() => {}}
        resetTranscript={() => {}}
        error={null}
        isSupported={true}
        onSubmit={() => {}}
      />
    );
    expect(screen.getByText(/Stop Speaking/i)).toBeInTheDocument();
    expect(screen.getByText(/Listening... Speak now/i)).toBeInTheDocument();
  });
});

describe('FeedbackCard Component', () => {
  const mockFeedback = {
    original_answer: 'I am want a blue shirt',
    is_correct: false,
    score: 70,
    mistakes: [
      {
        category: 'grammar',
        incorrect_part: 'I am want',
        correction: 'I want',
        explanation: "Do not use 'am' before the verb 'want'. Say 'I want'.",
      },
    ],
    corrected_sentence: 'I want a blue shirt.',
    simple_explanation: 'Use Simple Present without auxiliary am.',
    natural_expression: "I'm looking for a blue formal shirt.",
    additional_examples: ['I want to buy a formal shirt.', 'Could I see your blue shirts?'],
    encouragement: 'Good effort! Practice makes perfect.',
  };

  it('renders detailed feedback sections A to G correctly', () => {
    render(
      <FeedbackCard
        feedback={mockFeedback}
        onRepeatEvaluation={() => {}}
        onNextSituation={() => {}}
        isEvaluatingRepeat={false}
        repeatResult={null}
      />
    );

    // Section A: Original Answer
    expect(screen.getByText('"I am want a blue shirt"')).toBeInTheDocument();

    // Section B: Mistakes
    expect(screen.getByText('I am want')).toBeInTheDocument();
    expect(screen.getByText('I want')).toBeInTheDocument();

    // Section C: Corrected Sentence
    expect(screen.getByText('I want a blue shirt.')).toBeInTheDocument();

    // Section D: Explanation
    expect(screen.getByText('Use Simple Present without auxiliary am.')).toBeInTheDocument();

    // Section E: Natural Expression
    expect(screen.getByText('"I\'m looking for a blue formal shirt."')).toBeInTheDocument();

    // Section F: Examples
    expect(screen.getByText('I want to buy a formal shirt.')).toBeInTheDocument();

    // Section G: Practice Again
    expect(screen.getByText(/Practice Again – Repeat Corrected Sentence/i)).toBeInTheDocument();
  });
});
