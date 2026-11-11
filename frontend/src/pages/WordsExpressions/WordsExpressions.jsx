import React, { useState, useEffect } from 'react';
import { wordsExpressionsAPI } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { useTutor } from '../../context/TutorContext';
import { useSpeechSynthesis } from '../../hooks/useSpeechSynthesis';
import { useSpeechRecognition } from '../../hooks/useSpeechRecognition';
import { RobotTutor } from '../../components/RobotTutor';
import { DifficultyBadge } from '../../components/DifficultyBadge';
import {
  BookOpen, MessageSquare, MessagesSquare, CheckCircle2, Bookmark,
  BookmarkCheck, Volume2, Search, Sparkles, Filter, RefreshCw,
  ArrowRight, Award, Lightbulb, AlertTriangle, Layers, Shuffle,
  HelpCircle, Send, Check, X, ChevronRight, Mic, MicOff, Star
} from 'lucide-react';

const SECTIONS = [
  { id: 'words', label: 'Individual Words', icon: BookOpen, desc: '15 everyday categories with definitions, examples & mistakes' },
  { id: 'phrases', label: 'Daily Phrases & Expressions', icon: MessageSquare, desc: 'Natural conversational idioms & situational nuances' },
  { id: 'sentences', label: 'Complete Telugu-to-English Sentences', icon: Layers, desc: 'Full sentence structures, tenses & grammar formulas' },
  { id: 'situations', label: 'Situation-Based Expressions', icon: MessagesSquare, desc: 'Real-life dialogues across office, travel, daily life & interviews' },
  { id: 'practice', label: 'Interactive Quizzes & Practice', icon: Award, desc: 'Test yourself with translation, usage & sentence challenges' },
  { id: 'bookmarks', label: 'My Saved & Learned', icon: Bookmark, desc: 'Review your bookmarked items and track mastery' }
];

export function WordsExpressions() {
  const { user, profile, refreshProfile } = useAuth();
  const { setRobotState, triggerCelebration } = useTutor();
  const { speak } = useSpeechSynthesis();

  // Active section & view state
  const [activeSection, setActiveSection] = useState('words');
  const [items, setItems] = useState([]);
  const [totalItems, setTotalItems] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(false);

  // Filters
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [categories, setCategories] = useState([]);
  const [selectedLevel, setSelectedLevel] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  // Daily featured showcase & user progress
  const [dailyFeatured, setDailyFeatured] = useState(null);
  const [userStats, setUserStats] = useState(null);

  // Selected item modal / deep dive
  const [activeItem, setActiveItem] = useState(null);
  const [userSentence, setUserSentence] = useState('');
  const [checkingSentence, setCheckingSentence] = useState(false);
  const [sentenceFeedback, setSentenceFeedback] = useState(null);

  // Quizzes state
  const [exercises, setExercises] = useState([]);
  const [currentQuizIdx, setCurrentQuizIdx] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [quizResult, setQuizResult] = useState(null);
  const [submittingQuiz, setSubmittingQuiz] = useState(false);

  // Speech recognition for sentence creator
  const {
    transcript,
    setTranscript,
    isListening,
    startListening,
    stopListening,
    resetTranscript,
  } = useSpeechRecognition();

  // Sync voice transcript to sentence input
  useEffect(() => {
    if (transcript) {
      setUserSentence(transcript);
    }
  }, [transcript]);

  // Initial load: daily featured & user stats
  useEffect(() => {
    setRobotState(
      'GREETING',
      'Welcome to Words & Expressions! Learn how to convert Telugu thoughts into natural, fluent English.'
    );

    const loadMeta = async () => {
      try {
        const [featuredRes, statsRes] = await Promise.all([
          wordsExpressionsAPI.getDailyFeatured(),
          wordsExpressionsAPI.getProgress(),
        ]);
        setDailyFeatured(featuredRes.data);
        setUserStats(statsRes.data);
      } catch (err) {
        console.warn('Failed to load featured/stats:', err);
      }
    };
    loadMeta();
  }, [setRobotState]);

  // Load categories when section changes
  useEffect(() => {
    const loadCategories = async () => {
      if (['words', 'phrases', 'sentences', 'situations'].includes(activeSection)) {
        try {
          const res = await wordsExpressionsAPI.getCategories(activeSection);
          setCategories(res.data);
          setSelectedCategory('All');
          setPage(1);
        } catch (err) {
          console.warn('Failed to load categories:', err);
        }
      }
    };
    loadCategories();
  }, [activeSection]);

  // Load items or quiz exercises
  useEffect(() => {
    const fetchData = async () => {
      if (activeSection === 'practice') {
        // Load quiz exercises
        setLoading(true);
        try {
          const res = await wordsExpressionsAPI.getExercises(null, 10);
          setExercises(res.data);
          setCurrentQuizIdx(0);
          setSelectedAnswer('');
          setQuizResult(null);
        } catch (err) {
          console.warn('Failed to load exercises:', err);
        } finally {
          setLoading(false);
        }
        return;
      }

      setLoading(true);
      try {
        const params = {
          page,
          page_size: 12,
          category: selectedCategory !== 'All' ? selectedCategory : undefined,
          level: selectedLevel !== 'ALL' ? selectedLevel : undefined,
          search: searchQuery.trim() ? searchQuery.trim() : undefined,
        };

        if (activeSection === 'bookmarks') {
          params.bookmarked_only = true;
        } else {
          params.section = activeSection;
        }

        const res = await wordsExpressionsAPI.getItems(params);
        setItems(res.data.items);
        setTotalItems(res.data.total);
        setTotalPages(res.data.total_pages);
      } catch (err) {
        console.warn('Failed to load items:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [activeSection, selectedCategory, selectedLevel, searchQuery, page]);

  // Bookmark toggle
  const handleToggleBookmark = async (e, item) => {
    e.stopPropagation();
    try {
      const res = await wordsExpressionsAPI.toggleBookmark(item.id);
      setItems((prev) =>
        prev.map((i) => (i.id === item.id ? { ...i, is_bookmarked: res.data.is_bookmarked } : i))
      );
      if (activeItem && activeItem.id === item.id) {
        setActiveItem((prev) => ({ ...prev, is_bookmarked: res.data.is_bookmarked }));
      }
      // Refresh stats
      const statsRes = await wordsExpressionsAPI.getProgress();
      setUserStats(statsRes.data);
    } catch (err) {
      console.error('Bookmark error:', err);
    }
  };

  // Mark learned toggle
  const handleToggleLearned = async (e, item) => {
    e.stopPropagation();
    try {
      const res = await wordsExpressionsAPI.toggleLearned(item.id);
      setItems((prev) =>
        prev.map((i) => (i.id === item.id ? { ...i, is_learned: res.data.is_learned } : i))
      );
      if (activeItem && activeItem.id === item.id) {
        setActiveItem((prev) => ({ ...prev, is_learned: res.data.is_learned }));
      }
      if (res.data.is_learned) {
        triggerCelebration();
      }
      await refreshProfile();
      const statsRes = await wordsExpressionsAPI.getProgress();
      setUserStats(statsRes.data);
    } catch (err) {
      console.error('Mark learned error:', err);
    }
  };

  // Random learning item ("Surprise Me")
  const handleSurpriseMe = async () => {
    try {
      const sec = ['words', 'phrases', 'sentences', 'situations'].includes(activeSection)
        ? activeSection
        : undefined;
      const res = await wordsExpressionsAPI.getRandom(sec);
      openItemDetail(res.data);
      setRobotState(
        'EXPLAINING',
        `Here is a surprise expression for you: "${res.data.english_text}". Let's explore how to use it!`
      );
    } catch (err) {
      console.error('Random item error:', err);
    }
  };

  // Open detail modal and instruct robot
  const openItemDetail = (item) => {
    setActiveItem(item);
    setUserSentence('');
    setSentenceFeedback(null);
    resetTranscript();

    let robotMsg = `In Telugu, we say "${item.telugu_text}". In English, the natural expression is "${item.english_text}".`;
    if (item.when_to_use) {
      robotMsg += ` Use it: ${item.when_to_use}`;
    }
    setRobotState('TEACHING', robotMsg);
  };

  // Check student's custom sentence
  const handleCheckSentence = async () => {
    if (!userSentence.trim() || checkingSentence || !activeItem) return;
    if (isListening) stopListening();

    setCheckingSentence(true);
    setRobotState('THINKING', 'Analyzing your sentence grammar, tense, and natural phrasing...');

    try {
      const res = await wordsExpressionsAPI.checkSentence({
        item_id: activeItem.id,
        target_text: activeItem.english_text,
        user_sentence: userSentence.trim(),
      });

      setSentenceFeedback(res.data);
      if (res.data.is_correct) {
        setRobotState('SUCCESS', res.data.encouragement);
        triggerCelebration();
      } else {
        setRobotState('TEACHING', res.data.feedback);
      }
      await refreshProfile();
    } catch (err) {
      console.error('Sentence check error:', err);
      setRobotState('IDLE');
    } finally {
      setCheckingSentence(false);
    }
  };

  // Quiz submission
  const currentQuiz = exercises[currentQuizIdx];

  const handleQuizSubmit = async () => {
    if (!selectedAnswer || submittingQuiz || !currentQuiz) return;
    setSubmittingQuiz(true);

    try {
      const res = await wordsExpressionsAPI.checkExercise({
        exercise_id: currentQuiz.id,
        selected_answer: selectedAnswer,
      });

      setQuizResult(res.data);
      if (res.data.is_correct) {
        setRobotState('SUCCESS', 'Spot on! That is the natural native choice.');
        triggerCelebration();
        await refreshProfile();
      } else {
        setRobotState('TEACHING', res.data.explanation);
      }
    } catch (err) {
      console.error('Quiz submit error:', err);
    } finally {
      setSubmittingQuiz(false);
    }
  };

  const handleNextQuiz = () => {
    setSelectedAnswer('');
    setQuizResult(null);
    if (currentQuizIdx < exercises.length - 1) {
      setCurrentQuizIdx((prev) => prev + 1);
    } else {
      // Loop back
      setCurrentQuizIdx(0);
    }
  };

  return (
    <div className="words-expressions-page">
      {/* Page Header */}
      <div className="words-page-header">
        <div className="header-titles">
          <div className="module-pill">
            <Sparkles size={14} />
            <span>Telugu to Natural English</span>
          </div>
          <h2>Words & Expressions</h2>
          <p className="subtitle">
            Master how native speakers naturally express Telugu words, phrases, complete sentences, and workplace situations.
          </p>
        </div>

        <div className="header-stats-row">
          <div className="stat-capsule">
            <CheckCircle2 size={16} className="text-green" />
            <span><strong>{userStats?.learned_count || 0}</strong> Learned</span>
          </div>
          <div className="stat-capsule">
            <BookmarkCheck size={16} className="text-purple" />
            <span><strong>{userStats?.bookmarked_count || 0}</strong> Saved</span>
          </div>
          <button className="btn-surprise-me" onClick={handleSurpriseMe} title="Learn a random expression">
            <Shuffle size={15} />
            <span>Surprise Me</span>
          </button>
        </div>
      </div>

      {/* Daily Showcase (Word, Expression, Sentence of the Day) */}
      {dailyFeatured && (
        <div className="daily-showcase-grid">
          {dailyFeatured.word_of_the_day && (
            <div
              className="showcase-card word-card"
              onClick={() => openItemDetail(dailyFeatured.word_of_the_day)}
            >
              <div className="showcase-tag">
                <Star size={13} />
                <span>WORD OF THE DAY</span>
              </div>
              <h3 className="showcase-english">{dailyFeatured.word_of_the_day.english_text}</h3>
              <p className="showcase-telugu">{dailyFeatured.word_of_the_day.telugu_text}</p>
              <p className="showcase-def">{dailyFeatured.word_of_the_day.english_definition}</p>
              <div className="showcase-bottom">
                <span className="pos-text">{dailyFeatured.word_of_the_day.part_of_speech}</span>
                <span className="btn-explore-text">Explore <ArrowRight size={14} /></span>
              </div>
            </div>
          )}

          {dailyFeatured.expression_of_the_day && (
            <div
              className="showcase-card phrase-card"
              onClick={() => openItemDetail(dailyFeatured.expression_of_the_day)}
            >
              <div className="showcase-tag tag-purple">
                <Sparkles size={13} />
                <span>EXPRESSION OF THE DAY</span>
              </div>
              <h3 className="showcase-english">{dailyFeatured.expression_of_the_day.english_text}</h3>
              <p className="showcase-telugu">{dailyFeatured.expression_of_the_day.telugu_text}</p>
              <p className="showcase-def">{dailyFeatured.expression_of_the_day.when_to_use || 'Daily spoken conversation'}</p>
              <div className="showcase-bottom">
                <span className="pos-text">Conversational Phrase</span>
                <span className="btn-explore-text">Explore <ArrowRight size={14} /></span>
              </div>
            </div>
          )}

          {dailyFeatured.sentence_of_the_day && (
            <div
              className="showcase-card sentence-card"
              onClick={() => openItemDetail(dailyFeatured.sentence_of_the_day)}
            >
              <div className="showcase-tag tag-blue">
                <Layers size={13} />
                <span>SENTENCE OF THE DAY</span>
              </div>
              <h3 className="showcase-english">"{dailyFeatured.sentence_of_the_day.english_text}"</h3>
              <p className="showcase-telugu">{dailyFeatured.sentence_of_the_day.telugu_text}</p>
              <p className="showcase-def">{dailyFeatured.sentence_of_the_day.sentence_structure || 'Complete Sentence'}</p>
              <div className="showcase-bottom">
                <span className="pos-text">{dailyFeatured.sentence_of_the_day.category}</span>
                <span className="btn-explore-text">Explore <ArrowRight size={14} /></span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Main Section Navigation Tabs */}
      <div className="words-sections-tabs-bar">
        {SECTIONS.map((sec) => {
          const Icon = sec.icon;
          return (
            <button
              key={sec.id}
              className={`section-tab-btn ${activeSection === sec.id ? 'active' : ''}`}
              onClick={() => {
                setActiveSection(sec.id);
                setSearchQuery('');
                setSelectedCategory('All');
                setSelectedLevel('ALL');
                setPage(1);
              }}
            >
              <Icon size={18} />
              <span>{sec.label}</span>
            </button>
          );
        })}
      </div>

      {/* Content Area Based on Section */}
      {activeSection === 'practice' ? (
        /* QUIZ / PRACTICE SECTION */
        <div className="words-quiz-section">
          <div className="quiz-container-card">
            <div className="quiz-header">
              <div>
                <span className="quiz-badge">PRACTICE QUIZ</span>
                <h3>Test Your Telugu-to-English Mastery</h3>
              </div>
              <span className="quiz-counter">
                Question {currentQuizIdx + 1} of {exercises.length}
              </span>
            </div>

            {currentQuiz ? (
              <div className="quiz-content-body">
                <div className="quiz-question-box">
                  <h4 className="question-title">{currentQuiz.question}</h4>
                  {currentQuiz.telugu_prompt && (
                    <p className="question-telugu-hint">{currentQuiz.telugu_prompt}</p>
                  )}
                </div>

                <div className="quiz-options-list">
                  {currentQuiz.options?.map((opt, idx) => (
                    <button
                      key={idx}
                      className={`quiz-option-btn ${selectedAnswer === opt ? 'selected' : ''}`}
                      onClick={() => !quizResult && setSelectedAnswer(opt)}
                      disabled={quizResult !== null}
                    >
                      <span className="option-letter">{String.fromCharCode(65 + idx)}</span>
                      <span className="option-text">{opt}</span>
                    </button>
                  ))}
                </div>

                {!quizResult ? (
                  <div className="quiz-actions-row">
                    <button
                      className="btn-submit-quiz"
                      onClick={handleQuizSubmit}
                      disabled={!selectedAnswer || submittingQuiz}
                    >
                      <span>{submittingQuiz ? 'Checking...' : 'Submit Answer'}</span>
                      <ArrowRight size={16} />
                    </button>
                  </div>
                ) : (
                  <div className={`quiz-result-banner ${quizResult.is_correct ? 'pass' : 'fail'}`}>
                    <div className="result-top">
                      {quizResult.is_correct ? (
                        <>
                          <CheckCircle2 size={20} className="text-green" />
                          <strong>Correct! +10 Points</strong>
                        </>
                      ) : (
                        <>
                          <AlertTriangle size={20} className="text-amber" />
                          <strong>Correct Answer: {quizResult.correct_answer}</strong>
                        </>
                      )}
                    </div>
                    <p className="result-expl">{quizResult.explanation}</p>
                    <button className="btn-next-quiz" onClick={handleNextQuiz}>
                      <span>Next Question</span>
                      <ArrowRight size={16} />
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className="empty-quiz-notice">
                <CheckCircle2 size={36} className="text-green" />
                <p>Loading interactive exercises...</p>
              </div>
            )}
          </div>
        </div>
      ) : (
        /* STANDARD BROWSE / CARDS VIEW */
        <div className="words-content-layout">
          {/* Controls: Search, Category Pills, Level Filter */}
          <div className="words-filter-toolbar">
            <div className="search-box-wrap">
              <Search size={16} className="search-icon" />
              <input
                type="text"
                placeholder="Search Telugu or English words, phrases, sentences..."
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  setPage(1);
                }}
              />
            </div>

            {/* Level Selector */}
            <div className="level-filter-pills">
              {['ALL', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED'].map((lvl) => (
                <button
                  key={lvl}
                  className={`level-pill-btn ${selectedLevel === lvl ? 'active' : ''}`}
                  onClick={() => {
                    setSelectedLevel(lvl);
                    setPage(1);
                  }}
                >
                  {lvl}
                </button>
              ))}
            </div>
          </div>

          {/* Category Pills (if not in bookmarks) */}
          {activeSection !== 'bookmarks' && categories.length > 0 && (
            <div className="categories-scroll-row">
              <button
                className={`category-pill-btn ${selectedCategory === 'All' ? 'active' : ''}`}
                onClick={() => {
                  setSelectedCategory('All');
                  setPage(1);
                }}
              >
                All Categories ({totalItems})
              </button>
              {categories.map((cat) => (
                <button
                  key={cat.name}
                  className={`category-pill-btn ${selectedCategory === cat.name ? 'active' : ''}`}
                  onClick={() => {
                    setSelectedCategory(cat.name);
                    setPage(1);
                  }}
                >
                  {cat.name} ({cat.count})
                </button>
              ))}
            </div>
          )}

          {/* Cards Grid */}
          {loading ? (
            <div className="loading-grid-state">
              <RefreshCw size={32} className="spin-icon text-blue" />
              <p>Loading words and expressions...</p>
            </div>
          ) : items.length > 0 ? (
            <div className="words-items-grid">
              {items.map((item) => (
                <div
                  key={item.id}
                  className={`word-card-item ${item.is_learned ? 'card-learned' : ''}`}
                  onClick={() => openItemDetail(item)}
                >
                  <div className="card-top-bar">
                    <span className="card-cat-badge">{item.category}</span>
                    <div className="card-actions-group">
                      <button
                        className={`btn-action-icon ${item.is_bookmarked ? 'bookmarked' : ''}`}
                        onClick={(e) => handleToggleBookmark(e, item)}
                        title={item.is_bookmarked ? 'Remove bookmark' : 'Bookmark this item'}
                      >
                        <Bookmark size={16} fill={item.is_bookmarked ? '#8b5cf6' : 'none'} />
                      </button>
                      <button
                        className={`btn-action-icon ${item.is_learned ? 'learned' : ''}`}
                        onClick={(e) => handleToggleLearned(e, item)}
                        title={item.is_learned ? 'Marked as learned' : 'Mark as learned'}
                      >
                        <CheckCircle2 size={16} className={item.is_learned ? 'text-green' : ''} />
                      </button>
                    </div>
                  </div>

                  <div className="card-main-content">
                    {/* Telugu Source Text */}
                    <div className="telugu-block">
                      <span className="telugu-main-text">{item.telugu_text}</span>
                      {item.telugu_transliteration && (
                        <span className="telugu-phonetic">({item.telugu_transliteration})</span>
                      )}
                    </div>

                    <ArrowRight size={16} className="arrow-convert-icon" />

                    {/* English Natural Translation */}
                    <div className="english-block">
                      <div className="english-header-row">
                        <h4 className="english-main-text">{item.english_text}</h4>
                        <button
                          type="button"
                          className="btn-tiny-speak"
                          onClick={(e) => {
                            e.stopPropagation();
                            speak(item.english_text);
                          }}
                          title="Listen to native pronunciation"
                        >
                          <Volume2 size={15} />
                        </button>
                      </div>

                      {item.english_definition && (
                        <p className="english-def-snippet">{item.english_definition}</p>
                      )}
                    </div>
                  </div>

                  {/* Contextual Nuance / Examples Snippet */}
                  {item.when_to_use && (
                    <div className="when-to-use-snippet">
                      <Lightbulb size={13} className="text-amber" />
                      <span>{item.when_to_use}</span>
                    </div>
                  )}

                  {/* Card Footer */}
                  <div className="card-footer-bar">
                    <DifficultyBadge level={item.level} showIcon={false} />
                    <span className="deep-dive-link">
                      <span>Practice with AI Tutor</span>
                      <ChevronRight size={14} />
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-results-box">
              <BookOpen size={40} className="text-muted" />
              <h3>No items found</h3>
              <p>Try clearing your search query or selecting a different category filter.</p>
            </div>
          )}

          {/* Pagination Bar */}
          {totalPages > 1 && (
            <div className="pagination-bar">
              <button
                className="btn-page-nav"
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
              >
                Previous
              </button>
              <span className="page-indicator">
                Page {page} of {totalPages}
              </span>
              <button
                className="btn-page-nav"
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
              >
                Next
              </button>
            </div>
          )}
        </div>
      )}

      {/* DETAIL MODAL / DEEP-DIVE PRACTICE DRAWER */}
      {activeItem && (
        <div className="item-detail-modal-overlay" onClick={() => setActiveItem(null)}>
          <div className="item-detail-modal" onClick={(e) => e.stopPropagation()}>
            {/* Modal Header */}
            <div className="modal-header-bar">
              <div className="modal-title-group">
                <span className="modal-cat-tag">{activeItem.category}</span>
                <DifficultyBadge level={activeItem.level} />
              </div>
              <button className="btn-close-modal" onClick={() => setActiveItem(null)}>
                <X size={20} />
              </button>
            </div>

            <div className="modal-body-scroll">
              {/* Tutor Introduction Box */}
              <div className="modal-tutor-banner">
                <RobotTutor size="small" showMessage={true} />
              </div>

              {/* Main Bilingual Expression Display */}
              <div className="modal-main-expression-card">
                <div className="telugu-large-view">
                  <span className="script-label">తెలుగు వ్యక్తీకరణ:</span>
                  <h3 className="telugu-large-text">{activeItem.telugu_text}</h3>
                  {activeItem.telugu_transliteration && (
                    <span className="telugu-romanized">({activeItem.telugu_transliteration})</span>
                  )}
                </div>

                <div className="english-large-view">
                  <span className="script-label">Natural English:</span>
                  <div className="english-title-line">
                    <h2 className="english-large-text">"{activeItem.english_text}"</h2>
                    <button
                      className="btn-large-audio"
                      onClick={() => speak(activeItem.english_text)}
                      title="Listen to native pronunciation"
                    >
                      <Volume2 size={18} />
                      <span>Listen</span>
                    </button>
                  </div>
                  {activeItem.pronunciation && (
                    <span className="phonetic-text">{activeItem.pronunciation}</span>
                  )}
                  {activeItem.english_definition && (
                    <p className="english-meaning-text">{activeItem.english_definition}</p>
                  )}
                </div>
              </div>

              {/* When & Where to Use It */}
              {activeItem.when_to_use && (
                <div className="modal-section-box when-box">
                  <div className="section-title-line">
                    <Lightbulb size={16} className="text-amber" />
                    <h4>When and Where to Use It</h4>
                  </div>
                  <p>{activeItem.when_to_use}</p>
                </div>
              )}

              {/* Contextual Alternatives (Crucial for phrases with multiple meanings) */}
              {activeItem.contextual_alternatives_json?.length > 0 && (
                <div className="modal-section-box context-box">
                  <div className="section-title-line">
                    <Sparkles size={16} className="text-purple" />
                    <h4>Contextual Alternatives & Differences</h4>
                  </div>
                  <div className="context-alternatives-list">
                    {activeItem.contextual_alternatives_json.map((alt, idx) => (
                      <div key={idx} className="context-alt-card">
                        <div className="alt-top">
                          <strong>"{alt.english}"</strong>
                          <button
                            className="btn-tiny-speak"
                            onClick={() => speak(alt.english)}
                          >
                            <Volume2 size={13} />
                          </button>
                        </div>
                        <p className="alt-desc">{alt.context}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Word-by-Word Meaning Breakdown (Especially for Sentences) */}
              {activeItem.word_by_word_json?.length > 0 && (
                <div className="modal-section-box word-by-word-box">
                  <div className="section-title-line">
                    <Layers size={16} className="text-blue" />
                    <h4>Word-by-Word Breakdown</h4>
                  </div>
                  <div className="word-by-word-table">
                    {activeItem.word_by_word_json.map((w, idx) => (
                      <div key={idx} className="wbw-pair">
                        <span className="wbw-telugu">{w.telugu}</span>
                        <span className="wbw-arrow">↓</span>
                        <span className="wbw-english">{w.english}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Sentence Structure & Grammar Pattern */}
              {activeItem.sentence_structure && (
                <div className="modal-section-box structure-box">
                  <div className="section-title-line">
                    <BookOpen size={16} className="text-blue" />
                    <h4>Sentence Structure & Grammar Pattern</h4>
                  </div>
                  <p>{activeItem.sentence_structure}</p>
                </div>
              )}

              {/* Practical Examples */}
              {activeItem.examples_json?.length > 0 && (
                <div className="modal-section-box examples-box">
                  <div className="section-title-line">
                    <CheckCircle2 size={16} className="text-green" />
                    <h4>Practical Daily Examples</h4>
                  </div>
                  <div className="modal-examples-list">
                    {activeItem.examples_json.map((ex, idx) => (
                      <div key={idx} className="example-row-card">
                        <div className="example-eng-line">
                          <span>"{ex.english}"</span>
                          <button
                            className="btn-tiny-speak"
                            onClick={() => speak(ex.english)}
                          >
                            <Volume2 size={13} />
                          </button>
                        </div>
                        <span className="example-tel-line">{ex.telugu}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Practical Conversation / Dialogue (for Situations) */}
              {activeItem.dialogue_json?.length > 0 && (
                <div className="modal-section-box dialogue-box">
                  <div className="section-title-line">
                    <MessagesSquare size={16} className="text-blue" />
                    <h4>Real-Life Conversation Dialogue</h4>
                  </div>
                  <div className="dialogue-chat-list">
                    {activeItem.dialogue_json.map((turn, idx) => (
                      <div key={idx} className="dialogue-turn-bubble">
                        <span className="speaker-tag">{turn.speaker}:</span>
                        <span className="speaker-text">"{turn.text}"</span>
                        <button
                          className="btn-tiny-speak"
                          onClick={() => speak(turn.text)}
                        >
                          <Volume2 size={12} />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Common Mistakes (Literal Translation Traps) */}
              {activeItem.common_mistakes_json?.length > 0 && (
                <div className="modal-section-box mistakes-box">
                  <div className="section-title-line">
                    <AlertTriangle size={16} className="text-amber" />
                    <h4>Common Mistakes (Literal Translation Pitfalls)</h4>
                  </div>
                  <div className="mistakes-list">
                    {activeItem.common_mistakes_json.map((m, idx) => (
                      <div key={idx} className="mistake-item">
                        <div className="compare-line">
                          <span className="text-red strike">❌ {m.incorrect}</span>
                          <span className="text-green bold">✔️ {m.correct}</span>
                        </div>
                        <p className="mistake-reason">{m.reason}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Synonyms / Related terms */}
              {activeItem.synonyms_json?.length > 0 && (
                <div className="modal-section-box synonyms-box">
                  <span className="box-mini-label">Synonyms & Related Expressions:</span>
                  <div className="synonyms-tags-wrap">
                    {activeItem.synonyms_json.map((syn, idx) => (
                      <span key={idx} className="synonym-tag">{syn}</span>
                    ))}
                  </div>
                </div>
              )}

              {/* INTERACTIVE PRACTICE: CREATE YOUR OWN SENTENCE */}
              <div className="sentence-creator-card">
                <div className="creator-header">
                  <Sparkles size={18} className="text-blue" />
                  <h4>Practice with Tutor: Create Your Own Sentence</h4>
                </div>
                <p className="creator-instructions">
                  Create a natural sentence using <strong>"{activeItem.english_text}"</strong>. Speak using your microphone or type it below to get instant AI tutor feedback!
                </p>

                <div className="creator-input-bar">
                  <button
                    type="button"
                    className={`btn-creator-mic ${isListening ? 'listening' : ''}`}
                    onClick={isListening ? stopListening : startListening}
                    disabled={checkingSentence}
                  >
                    {isListening ? <MicOff size={16} /> : <Mic size={16} />}
                    <span>{isListening ? 'Stop' : 'Speak'}</span>
                  </button>

                  <input
                    type="text"
                    className="creator-text-input"
                    value={userSentence}
                    onChange={(e) => setUserSentence(e.target.value)}
                    placeholder={`e.g. Try making a sentence with ${activeItem.english_text}...`}
                    disabled={checkingSentence}
                  />

                  <button
                    type="button"
                    className="btn-creator-submit"
                    onClick={handleCheckSentence}
                    disabled={checkingSentence || !userSentence.trim()}
                  >
                    <Send size={15} />
                    <span>{checkingSentence ? 'Checking...' : 'Check'}</span>
                  </button>
                </div>

                {sentenceFeedback && (
                  <div className={`creator-feedback-box ${sentenceFeedback.is_correct ? 'pass' : 'review'}`}>
                    <div className="feedback-top">
                      {sentenceFeedback.is_correct ? (
                        <>
                          <CheckCircle2 size={18} className="text-green" />
                          <strong>Excellent! Score: {Math.round(sentenceFeedback.score)}%</strong>
                        </>
                      ) : (
                        <>
                          <AlertTriangle size={18} className="text-amber" />
                          <strong>Correction Suggested:</strong>
                        </>
                      )}
                    </div>
                    <p className="feedback-corrected">"{sentenceFeedback.corrected_sentence}"</p>
                    <p className="feedback-text">{sentenceFeedback.feedback}</p>
                    <p className="feedback-encouragement">{sentenceFeedback.encouragement}</p>
                  </div>
                )}
              </div>
            </div>

            {/* Modal Bottom Action Bar */}
            <div className="modal-bottom-actions">
              <button
                className={`btn-modal-action ${activeItem.is_bookmarked ? 'active' : ''}`}
                onClick={(e) => handleToggleBookmark(e, activeItem)}
              >
                <Bookmark size={16} />
                <span>{activeItem.is_bookmarked ? 'Bookmarked' : 'Bookmark'}</span>
              </button>

              <button
                className={`btn-modal-action primary ${activeItem.is_learned ? 'active' : ''}`}
                onClick={(e) => handleToggleLearned(e, activeItem)}
              >
                <CheckCircle2 size={16} />
                <span>{activeItem.is_learned ? 'Marked as Learned' : 'Mark as Learned'}</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
