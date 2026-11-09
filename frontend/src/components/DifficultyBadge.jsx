import React from 'react';
import { ShieldCheck, Award, Zap } from 'lucide-react';

export function DifficultyBadge({ level = 'BEGINNER', showIcon = true }) {
  const norm = (level || 'BEGINNER').toUpperCase();

  const config = {
    BEGINNER: {
      label: 'Beginner',
      className: 'badge-level-beginner',
      icon: ShieldCheck,
      color: '#3b82f6',
    },
    INTERMEDIATE: {
      label: 'Intermediate',
      className: 'badge-level-intermediate',
      icon: Award,
      color: '#8b5cf6',
    },
    ADVANCED: {
      label: 'Advanced',
      className: 'badge-level-advanced',
      icon: Zap,
      color: '#ec4899',
    },
  }[norm] || {
    label: norm,
    className: 'badge-level-beginner',
    icon: ShieldCheck,
    color: '#3b82f6',
  };

  const IconComponent = config.icon;

  return (
    <span className={`difficulty-badge ${config.className}`}>
      {showIcon && <IconComponent size={13} className="badge-icon" />}
      <span>{config.label}</span>
    </span>
  );
}
