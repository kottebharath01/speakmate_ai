import axios from 'axios';
import { getLocalDateString } from '../utils/dateUtils';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach JWT token to requests if present in localStorage
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('speakmate_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (data) => api.post('/auth/register', data),
  getMe: () => api.get('/auth/me'),
};

export const situationsAPI = {
  getAll: (level, category) => api.get('/situations', { params: { level, category } }),
  getById: (id) => api.get(`/situations/${id}`),
  generate: (category, level) => api.post('/situations/generate', null, { params: { category, level } }),
  submit: (data) => api.post('/situations/submit', data),
  evaluateRepeat: (data) => api.post('/situations/repeat-evaluation', data),
  // Guided Speaking Practice Sessions
  getCategoryStats: () => api.get('/situations/categories/stats'),
  startSession: (data) =>
    api.post('/situations/sessions/start', {
      ...data,
      local_date: data?.local_date || getLocalDateString(),
    }),
  getActiveSession: () => api.get('/situations/sessions/active'),
  getSession: (id) => api.get(`/situations/sessions/${id}`),
  submitSessionAnswer: (id, data) => api.post(`/situations/sessions/${id}/submit`, data),
  submitSessionRepeat: (id, data) => api.post(`/situations/sessions/${id}/repeat`, data),
  abandonSession: (id) => api.post(`/situations/sessions/${id}/abandon`),
  getSessionHistory: () => api.get('/situations/sessions/history'),
};

export const aiAPI = {
  chat: (data) => api.post('/ai/chat', data),
  correctSentence: (sentence) => api.post('/ai/correct-sentence', { sentence }),
};

export const learningAPI = {
  getLessons: (category, level) => api.get('/lessons', { params: { category, level } }),
  getLesson: (id) => api.get(`/lessons/${id}`),
  getPatterns: (level) => api.get('/patterns', { params: { level } }),
  getVocabulary: (level, search) => api.get('/vocabulary', { params: { level, search } }),
  getDailyChallenges: () => api.get('/daily-challenges'),
};

export const progressAPI = {
  getStats: (localDate) =>
    api.get('/dashboard-stats', { params: { local_date: localDate || getLocalDateString() } }),
  getStreak: (localDate) =>
    api.get('/streak', { params: { local_date: localDate || getLocalDateString() } }),
  getRecords: () => api.get('/progress'),
  getMistakes: (isResolved) => api.get('/mistakes', { params: { is_resolved: isResolved } }),
  getAssessments: () => api.get('/assessments'),
};

export const interviewAPI = {
  start: (topic, level) => api.post('/interviews/start', { topic, level }),
  answer: (data) => api.post('/interviews/answer', data),
};

export const profileAPI = {
  get: (localDate) =>
    api.get('/profile', { params: { local_date: localDate || getLocalDateString() } }),
  update: (data) => api.put('/profile', data),
};

export const wordsExpressionsAPI = {
  getItems: (params) => api.get('/words-expressions/items', { params }),
  getItem: (id) => api.get(`/words-expressions/items/${id}`),
  getCategories: (section) => api.get('/words-expressions/categories', { params: { section } }),
  getDailyFeatured: () => api.get('/words-expressions/daily-featured'),
  getRandom: (section) => api.get('/words-expressions/random', { params: { section } }),
  toggleBookmark: (id) => api.post(`/words-expressions/items/${id}/bookmark`),
  toggleLearned: (id) => api.post(`/words-expressions/items/${id}/mark-learned`),
  getProgress: () => api.get('/words-expressions/progress'),
  getExercises: (section, limit) => api.get('/words-expressions/exercises', { params: { section, limit } }),
  checkExercise: (data) => api.post('/words-expressions/check-exercise', data),
  checkSentence: (data) => api.post('/words-expressions/check-sentence', data),
  // Guided Words & Expressions Sessions
  getModesSummary: () => api.get('/words-expressions/modes/summary'),
  startSession: (data) =>
    api.post('/words-expressions/sessions/start', {
      ...data,
      local_date: data?.local_date || getLocalDateString(),
    }),
  getActiveSession: () => api.get('/words-expressions/sessions/active'),
  getSession: (id) => api.get(`/words-expressions/sessions/${id}`),
  submitSessionAnswer: (id, data) => api.post(`/words-expressions/sessions/${id}/answer`, data),
  submitSessionRepeat: (id, data) => api.post(`/words-expressions/sessions/${id}/repeat`, data),
  abandonSession: (id) => api.post(`/words-expressions/sessions/${id}/abandon`),
  getSessionHistory: () => api.get('/words-expressions/sessions/history'),
};

export default api;
