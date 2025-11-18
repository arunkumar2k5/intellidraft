import React from 'react';
import './ProgressIndicator.css';

function ProgressIndicator({ done, total }) {
  const percentage = total > 0 ? Math.round((done / total) * 100) : 0;

  return (
    <div className="progress-indicator">
      <div className="progress-circle">
        <svg width="96" height="96" viewBox="0 0 96 96">
          <circle
            cx="48"
            cy="48"
            r="40"
            fill="none"
            stroke="#39275c"
            strokeWidth="6"
          />
          <circle
            cx="48"
            cy="48"
            r="40"
            fill="none"
            stroke="#7c5fff"
            strokeWidth="6"
            strokeDasharray={`${2 * Math.PI * 40}`}
            strokeDashoffset={`${2 * Math.PI * 40 * (1 - percentage / 100)}`}
            strokeLinecap="round"
            transform="rotate(-90 48 48)"
            style={{ transition: 'stroke-dashoffset 0.3s ease' }}
          />
        </svg>
        <div className="progress-text">{percentage}%</div>
      </div>
      <p className="progress-label">Processing parts ({done} / {total})</p>
    </div>
  );
}

export default ProgressIndicator;
