import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { DifficultyBadge } from './DifficultyBadge';
import {
  Flame, Award, User, LogOut, Menu, Sparkles
} from 'lucide-react';

export function Navbar({ onToggleSidebar }) {
  const { user, profile, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="main-navbar">
      <div className="navbar-left">
        <button
          className="sidebar-toggle-btn"
          onClick={onToggleSidebar}
          aria-label="Toggle Sidebar"
        >
          <Menu size={22} />
        </button>
        <Link to="/" className="brand-logo-link">
          <div className="brand-icon-wrapper">
            <Sparkles size={20} className="sparkle-svg" />
          </div>
          <div className="brand-text">
            <span className="brand-title">SpeakMate <span className="ai-tag">AI</span></span>
            <span className="brand-subtitle">Your Personal English Tutor</span>
          </div>
        </Link>
      </div>

      <div className="navbar-right">
        {/* Streak and Points Display */}
        {profile && (
          <div className="stats-badges-group">
            <div className="nav-stat-pill streak-pill" title="Current Daily Practice Streak">
              <Flame size={16} className="flame-icon" />
              <span>{profile.streak_count || 1} Day Streak</span>
            </div>
            <div className="nav-stat-pill points-pill" title="Total Practice Points">
              <Award size={16} className="star-icon" />
              <span>{profile.total_points || 0} pts</span>
            </div>
            <DifficultyBadge level={profile.current_level} />
          </div>
        )}

        {/* User Account / Profile dropdown */}
        {user ? (
          <div className="user-profile-menu">
            <Link to="/settings" className="user-avatar-btn" title="View Profile & Settings">
              <div className="avatar-circle">
                {user.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
              </div>
              <span className="user-display-name">{user.full_name || user.username}</span>
            </Link>
            <button
              onClick={handleLogout}
              className="btn-logout"
              title="Log out"
              aria-label="Log out"
            >
              <LogOut size={16} />
            </button>
          </div>
        ) : (
          <div className="auth-buttons">
            <Link to="/login" className="btn-nav-login">Login</Link>
            <Link to="/register" className="btn-nav-register">Get Started</Link>
          </div>
        )}
      </div>
    </header>
  );
}
