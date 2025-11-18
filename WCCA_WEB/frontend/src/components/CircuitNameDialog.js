import React, { useState, useEffect } from 'react';
import { X, Loader } from 'lucide-react';
import './CircuitNameDialog.css';

function CircuitNameDialog({ onClose, onGenerate, circuitName, loading }) {
  const [generatedName, setGeneratedName] = useState('');
  const [manualName, setManualName] = useState('');
  const [showManualInput, setShowManualInput] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    if (!circuitName && !isGenerating) {
      handleGenerate();
    }
  }, []);

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      const name = await onGenerate();
      setGeneratedName(name);
    } catch (error) {
      console.error('Error generating name:', error);
      setGeneratedName('Unknown Circuit');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleProceed = () => {
    console.log('Circuit name:', generatedName);
    onClose();
  };

  const handleManualSubmit = () => {
    if (manualName.trim()) {
      console.log('Manual circuit name:', manualName);
      onClose();
    }
  };

  if (showManualInput) {
    return (
      <div className="dialog-overlay" onClick={onClose}>
        <div className="dialog-content" onClick={(e) => e.stopPropagation()}>
          <button className="close-btn" onClick={onClose}>
            <X size={24} />
          </button>
          
          <h2 className="dialog-title">Enter Circuit Name Manually</h2>
          
          <div className="manual-input-section">
            <input
              type="text"
              className="manual-input"
              value={manualName}
              onChange={(e) => setManualName(e.target.value)}
              placeholder="Enter circuit name..."
              autoFocus
              onKeyPress={(e) => e.key === 'Enter' && handleManualSubmit()}
            />
          </div>
          
          <div className="dialog-actions">
            <button 
              className="btn btn-primary"
              onClick={handleManualSubmit}
              disabled={!manualName.trim()}
            >
              Submit
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>
          <X size={24} />
        </button>
        
        <h2 className="dialog-title">
          {isGenerating ? 'Generating Circuit Name...' : 'Detected Circuit Name'}
        </h2>
        
        <div className="circuit-name-display">
          {isGenerating ? (
            <div className="loading-state">
              <Loader className="spinner" size={40} />
              <p>Thinking...</p>
            </div>
          ) : (
            <p className="circuit-name">{generatedName || circuitName}</p>
          )}
        </div>
        
        {!isGenerating && (
          <div className="dialog-actions">
            <button 
              className="btn btn-primary"
              onClick={handleProceed}
            >
              Proceed
            </button>
            <button 
              className="btn btn-secondary"
              onClick={() => setShowManualInput(true)}
            >
              Enter Manually
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default CircuitNameDialog;
