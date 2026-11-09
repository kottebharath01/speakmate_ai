import axios from 'axios';

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
  getStats: () => api.get('/dashboard-stats'),
  getRecords: () => api.get('/progress'),
  getMistakes: (isResolved) => api.get('/mistakes', { params: { is_resolved: isResolved } }),
  getAssessments: () => api.get('/assessments'),
};

export const interviewAPI = {
  start: (topic, level) => api.post('/interviews/start', { topic, level }),
  answer: (data) => api.post('/interviews/answer', data),
};

export const profileAPI = {
  get: () => api.get('/profile'),
  update: (data) => api.put('/profile', data),
};

export default api;
