import React, { useState, useEffect } from 'react';
import { learningAPI } from '../services/api';
import { useTutor } from '../context/TutorContext';
import { DifficultyBadge } from '../components/DifficultyBadge';
import {
  BookMarked, Volume2, Search, Sparkles, Filter, Check, Eye
} from 'lucide-react';

export function VocabularyTrainer() {
  const { setRobotState, speak } = useTutor();
  const [vocabList, setVocabList] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedLevel, setSelectedLevel] = useState('ALL');
  const [cardFlipMap, setCardFlipMap] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setRobotState(
      'TEACHING',
      'Learn high-impact English words with their Telugu meanings and spoken context.'
    );

    const loadVocab = async () => {
      try {
        const res = await learningAPI.getVocabulary();
        setVocabList(res.data);
      } catch (err) {
        console.warn('Failed to fetch vocabulary:', err);
      } finally {
        setLoading(false);
      }
    };

    loadVocab();
  }, [setRobotState]);

  const toggleFlip = (id) => {
    setCardFlipMap((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const filteredVocab = vocabList.filter((item) => {
    const matchesSearch =
      item.word.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.telugu_meaning.includes(searchQuery) ||
      item.english_definition.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesLevel = selectedLevel === 'ALL' || item.level === selectedLevel;
    return matchesSearch && matchesLevel;
  });

  return (
    <div className="vocabulary-trainer-page">
      <div className="page-header-row">
        <div>
          <h2>Practical Vocabulary Trainer</h2>
          <p className="subtitle">High-frequency words for daily communication and workplace success.</p>
        </div>

        {/* Filter Bar */}
        <div className="vocab-filters-row">
          <div className="search-input-wrapper">
            <Search size={16} className="search-icon" />
            <input
              type="text"
              placeholder="Search words, meanings..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="level-select-pills">
            {['ALL', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED'].map((lvl) => (
              <button
                key={lvl}
                className={`filter-pill ${selectedLevel === lvl ? 'active' : ''}`}
                onClick={() => setSelectedLevel(lvl)}
              >
                {lvl}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Vocabulary Cards Grid */}
      <div className="vocab-cards-grid">
        {filteredVocab.map((item) => {
          const isFlipped = cardFlipMap[item.id];
          return (
            <div
              key={item.id}
              className={`vocab-card ${isFlipped ? 'flipped' : ''}`}
              onClick={() => toggleFlip(item.id)}
            >
              <div className="vocab-card-header">
                <span className="pos-badge">{item.part_of_speech}</span>
                <DifficultyBadge level={item.level} showIcon={false} />
              </div>

              <div className="vocab-word-row">
                <h3 className="vocab-word">{item.word}</h3>
                <button
                  type="button"
                  className="btn-audio-circle"
                  onClick={(e) => {
                    e.stopPropagation();
                    speak(item.word);
                  }}
                  title="Listen to pronunciation"
                >
                  <Volume2 size={16} />
                </button>
              </div>

              {/* Front Side: Meaning & Definition */}
              <div className="vocab-card-body">
                <div className="telugu-meaning-pill">
                  <span className="telugu-label">తెలుగు అర్థం:</span>
                  <span className="telugu-word">{item.telugu_meaning}</span>
                </div>

                <p className="english-def">{item.english_definition}</p>

                <div className="vocab-example-box">
                  <span className="example-tag">Example:</span>
                  <p className="example-text">"{item.example_sentence}"</p>
                  <button
                    type="button"
                    className="btn-example-speak"
                    onClick={(e) => {
                      e.stopPropagation();
                      speak(item.example_sentence);
                    }}
                    title="Listen to sentence"
                  >
                    <Volume2 size={13} />
                  </button>
                </div>

                {item.usage_notes && (
                  <div className="usage-note-banner">
                    <Sparkles size={13} className="text-blue" />
                    <span>{item.usage_notes}</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
