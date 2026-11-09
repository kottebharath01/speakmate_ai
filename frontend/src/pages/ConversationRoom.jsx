import React, { useState, useEffect, useRef } from 'react';
import { aiAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useTutor } from '../context/TutorContext';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';
import { RobotTutor } from '../components/RobotTutor';
import {
  Send, Mic, MicOff, Volume2, Sparkles, MessageSquare,
  AlertCircle, Lightbulb, RefreshCw
} from 'lucide-react';

const TOPICS = [
  'Daily Routine',
  'Family & Friends',
  'Hobbies & Interests',
  'Travel Experiences',
  'Workplace & Career',
  'Technology & Software',
  'Weekend Plans',
];

export function ConversationRoom() {
  const { profile } = useAuth();
  const { setRobotState, speak } = useTutor();

  const [currentTopic, setCurrentTopic] = useState('Daily Routine');
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [textInput, setTextInput] = useState('');
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef(null);

  const {
    transcript,
    setTranscript,
    isListening,
    startListening,
    stopListening,
    resetTranscript,
  } = useSpeechRecognition();

  // Initialize conversation when topic changes
  useEffect(() => {
    setMessages([
      {
        sender: 'ai',
        text: `Hello! I'm SpeakMate AI. Let's chat about ${currentTopic}. How has your day been so far?`,
      },
    ]);
    setConversationId(null);
    setRobotState('GREETING', `Let's have a friendly English chat about ${currentTopic}!`);
  }, [currentTopic, setRobotState]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Sync speech transcript into textInput
  useEffect(() => {
    if (transcript) {
      setTextInput(transcript);
    }
  }, [transcript]);

  const handleSendMessage = async () => {
    const textToSend = textInput.trim();
    if (!textToSend || sending) return;

    if (isListening) stopListening();
    resetTranscript();
    setTextInput('');

    // Append user message
    const updatedMessages = [...messages, { sender: 'user', text: textToSend }];
    setMessages(updatedMessages);

    setSending(true);
    setRobotState('THINKING');

    try {
      const res = await aiAPI.chat({
        message: textToSend,
        topic: currentTopic,
        conversation_id: conversationId,
      });

      setConversationId(res.data.conversation_id);
      setMessages((prev) => [
        ...prev,
        {
          sender: 'ai',
          text: res.data.reply,
          gentle_tip: res.data.gentle_tip,
          suggested_ideas: res.data.suggested_reply_ideas,
        },
      ]);

      setRobotState('TEACHING');
      speak(res.data.reply);
    } catch (err) {
      console.error('Chat error:', err);
      setRobotState('IDLE');
    } finally {
      setSending(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="conversation-room-page">
      {/* Header and Topic Selector */}
      <div className="room-header-bar">
        <div>
          <h2>AI English Conversation Room</h2>
          <p className="subtitle">Practice free-form casual conversations with gentle grammar coaching.</p>
        </div>

        {/* Topic Pills */}
        <div className="topics-scroll-row">
          {TOPICS.map((t) => (
            <button
              key={t}
              className={`topic-pill ${currentTopic === t ? 'active' : ''}`}
              onClick={() => setCurrentTopic(t)}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      <div className="conversation-layout">
        {/* Tutor Character Card */}
        <div className="tutor-side-widget">
          <RobotTutor size="medium" showMessage={true} />
        </div>

        {/* Chat History & Input */}
        <div className="chat-main-widget">
          <div className="chat-messages-scroll">
            {messages.map((msg, idx) => (
              <div key={idx} className={`chat-bubble-row ${msg.sender === 'user' ? 'user' : 'ai'}`}>
                <div className="chat-bubble">
                  <p className="message-text">{msg.text}</p>

                  {/* Audio button for AI reply */}
                  {msg.sender === 'ai' && (
                    <button
                      className="btn-bubble-audio"
                      onClick={() => speak(msg.text)}
                      title="Listen to response"
                    >
                      <Volume2 size={14} />
                    </button>
                  )}

                  {/* Gentle Coaching Tip */}
                  {msg.gentle_tip && (
                    <div className="gentle-tip-card">
                      <Lightbulb size={14} className="text-amber" />
                      <span>{msg.gentle_tip}</span>
                    </div>
                  )}

                  {/* Suggested Quick Reply Ideas */}
                  {msg.suggested_ideas && msg.suggested_ideas.length > 0 && (
                    <div className="suggested-ideas-row">
                      <span className="ideas-label">Suggested replies:</span>
                      {msg.suggested_ideas.map((idea, i) => (
                        <button
                          key={i}
                          className="btn-idea-pill"
                          onClick={() => setTextInput(idea)}
                        >
                          "{idea}"
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {sending && (
              <div className="chat-bubble-row ai">
                <div className="chat-bubble thinking-bubble">
                  <RefreshCw size={16} className="spin-icon" />
                  <span>SpeakMate is thinking...</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Interactive Chat Input Bar */}
          <div className="chat-input-bar">
            <button
              type="button"
              className={`btn-chat-mic ${isListening ? 'listening' : ''}`}
              onClick={isListening ? stopListening : startListening}
              title={isListening ? 'Stop listening' : 'Tap to speak'}
            >
              {isListening ? <MicOff size={18} /> : <Mic size={18} />}
            </button>

            <input
              type="text"
              className="chat-text-input"
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={isListening ? 'Listening to your voice...' : 'Type or speak your reply in English...'}
              disabled={sending}
            />

            <button
              type="button"
              className="btn-chat-send"
              onClick={handleSendMessage}
              disabled={sending || !textInput.trim()}
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
