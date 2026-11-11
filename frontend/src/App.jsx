import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { TutorProvider } from './context/TutorContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';

import { Dashboard } from './pages/Dashboard';
import { SituationPractice } from './pages/SituationPractice';
import { ConversationRoom } from './pages/ConversationRoom';
import { GrammarAcademy } from './pages/GrammarAcademy';
import { SentencePatterns } from './pages/SentencePatterns';
import { VocabularyTrainer } from './pages/VocabularyTrainer';
import { WordsExpressions } from './pages/WordsExpressions/WordsExpressions';
import { InterviewPrep } from './pages/InterviewPrep';
import { DailyChallenges } from './pages/DailyChallenges';
import { MistakeJournal } from './pages/MistakeJournal';
import { ProgressCentre } from './pages/ProgressCentre';
import { ProfileSettings } from './pages/ProfileSettings';
import { Login } from './pages/Login';
import { Register } from './pages/Register';

import './App.css';

function MainLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="auth-loading-screen">
        <div className="loading-spinner-box">Loading SpeakMate AI...</div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="app-shell">
      <Navbar onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
      <div className="app-body">
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        <main className="main-content-area">{children}</main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <TutorProvider>
          <Routes>
            {/* Public Auth Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Core Application Routes with Shell Layout */}
            <Route
              path="/"
              element={
                <MainLayout>
                  <Dashboard />
                </MainLayout>
              }
            />
            <Route
              path="/situations"
              element={
                <MainLayout>
                  <SituationPractice />
                </MainLayout>
              }
            />
            <Route
              path="/words-expressions"
              element={
                <MainLayout>
                  <WordsExpressions />
                </MainLayout>
              }
            />
            <Route
              path="/conversation"
              element={
                <MainLayout>
                  <ConversationRoom />
                </MainLayout>
              }
            />
            <Route
              path="/grammar"
              element={
                <MainLayout>
                  <GrammarAcademy />
                </MainLayout>
              }
            />
            <Route
              path="/patterns"
              element={
                <MainLayout>
                  <SentencePatterns />
                </MainLayout>
              }
            />
            <Route
              path="/vocabulary"
              element={
                <MainLayout>
                  <VocabularyTrainer />
                </MainLayout>
              }
            />
            <Route
              path="/interview"
              element={
                <MainLayout>
                  <InterviewPrep />
                </MainLayout>
              }
            />
            <Route
              path="/challenges"
              element={
                <MainLayout>
                  <DailyChallenges />
                </MainLayout>
              }
            />
            <Route
              path="/mistakes"
              element={
                <MainLayout>
                  <MistakeJournal />
                </MainLayout>
              }
            />
            <Route
              path="/progress"
              element={
                <MainLayout>
                  <ProgressCentre />
                </MainLayout>
              }
            />
            <Route
              path="/settings"
              element={
                <MainLayout>
                  <ProfileSettings />
                </MainLayout>
              }
            />

            {/* Catch-all redirect */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </TutorProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
