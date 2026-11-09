import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI, profileAPI } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchProfile = async () => {
    try {
      const res = await profileAPI.get();
      setProfile(res.data);
    } catch (err) {
      console.warn('Failed to fetch profile', err);
    }
  };

  const checkAuth = async () => {
    const token = localStorage.getItem('speakmate_token');
    if (token) {
      try {
        const res = await authAPI.getMe();
        setUser(res.data);
        await fetchProfile();
      } catch (err) {
        console.warn('Token expired or invalid, logging out', err);
        localStorage.removeItem('speakmate_token');
        setUser(null);
      }
    } else {
      // Auto-login as default learner for seamless local development
      try {
        const loginRes = await authAPI.login('learner@speakmate.ai', 'password123');
        localStorage.setItem('speakmate_token', loginRes.data.access_token);
        const userRes = await authAPI.getMe();
        setUser(userRes.data);
        await fetchProfile();
      } catch (e) {
        console.warn('Auto-login demo skipped', e);
      }
    }
    setLoading(false);
  };

  useEffect(() => {
    checkAuth();
  }, []);

  const login = async (email, password) => {
    const res = await authAPI.login(email, password);
    localStorage.setItem('speakmate_token', res.data.access_token);
    const userRes = await authAPI.getMe();
    setUser(userRes.data);
    await fetchProfile();
    return userRes.data;
  };

  const register = async (formData) => {
    await authAPI.register(formData);
    return login(formData.email, formData.password);
  };

  const logout = () => {
    localStorage.removeItem('speakmate_token');
    setUser(null);
    setProfile(null);
  };

  const refreshProfile = async () => {
    await fetchProfile();
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        loading,
        login,
        register,
        logout,
        refreshProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
