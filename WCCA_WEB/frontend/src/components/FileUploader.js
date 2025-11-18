import React, { useRef, useState } from 'react';
import { Upload } from 'lucide-react';
import './FileUploader.css';

function FileUploader({ title, fileType, label, onUpload, preview, fileName }) {
  const fileInputRef = useRef(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const handleBrowse = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setError('');

    try {
      await onUpload(fileType, file);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const getAcceptedExtensions = () => {
    const extensions = {
      xml: '.xml',
      csv: '.csv',
      yaml: '.yml,.yaml'
    };
    return extensions[fileType] || '';
  };

  return (
    <div className="file-uploader">
      <h3 className="uploader-title">{title}</h3>
      
      <div className="upload-row">
        <label className="file-label">{label}</label>
        <input
          type="text"
          className="file-input"
          value={fileName || ''}
          readOnly
          placeholder="No file selected"
        />
        <button 
          className="browse-btn"
          onClick={handleBrowse}
          disabled={uploading}
        >
          {uploading ? 'Uploading...' : 'Browse'}
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept={getAcceptedExtensions()}
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="preview-section">
        <h4 className="preview-title">Preview</h4>
        <div className="preview-box">
          {preview && preview.length > 0 ? (
            <pre className="preview-content">
              {preview.join('\n')}
            </pre>
          ) : (
            <div className="preview-placeholder">
              <Upload size={32} color="#bcb4d5" />
              <p>No file uploaded</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default FileUploader;
