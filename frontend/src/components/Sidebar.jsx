import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard, MessageSquareText, MessagesSquare, BookOpen,
  Boxes, BookMarked, Briefcase, CalendarCheck, AlertOctagon,
  TrendingUp, Settings
} from 'lucide-react';

const NAV_ITEMS = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/situations', label: 'Situation Practice', icon: MessageSquareText, highlight: true },
  { to: '/conversation', label: 'AI Conversation Room', icon: MessagesSquare },
  { to: '/grammar', label: 'Grammar Academy', icon: BookOpen },
  { to: '/patterns', label: 'Sentence Patterns', icon: Boxes },
  { to: '/vocabulary', label: 'Vocabulary Trainer', icon: BookMarked },
  { to: '/interview', label: 'Interview Preparation', icon: Briefcase },
  { to: '/challenges', label: 'Daily Challenges', icon: CalendarCheck },
  { to: '/mistakes', label: 'Mistake Journal', icon: AlertOctagon },
  { to: '/progress', label: 'Progress Centre', icon: TrendingUp },
  { to: '/settings', label: 'Profile & Settings', icon: Settings },
];

export function Sidebar({ isOpen, onClose }) {
  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && <div className="sidebar-backdrop" onClick={onClose} />}

      <aside className={`main-sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-section-title">LEARNING MODULES</div>
        <nav className="sidebar-nav">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                onClick={onClose}
                className={({ isActive }) =>
                  `sidebar-link ${isActive ? 'active' : ''} ${item.highlight ? 'featured' : ''}`
                }
                end={item.to === '/'}
              >
                <Icon size={19} className="nav-icon" />
                <span className="nav-text">{item.label}</span>
                {item.highlight && <span className="core-badge">CORE</span>}
              </NavLink>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <div className="tutor-mini-status">
            <span className="status-dot online" />
            <span className="status-text">AI Tutor Active & Ready</span>
          </div>
        </div>
      </aside>
    </>
  );
}
