import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FileUploader from './components/FileUploader';
import PartsTable from './components/PartsTable';
import CircuitNameDialog from './components/CircuitNameDialog';
import ProgressIndicator from './components/ProgressIndicator';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [files, setFiles] = useState({
    xml: null,
    csv: null,
    yaml: null
  });
  
  const [previews, setPreviews] = useState({
    xml: [],
    csv: [],
    yaml: []
  });
  
  const [chips, setChips] = useState([]);
  const [partsData, setPartsData] = useState(null);
  const [progress, setProgress] = useState({ done: 0, total: 0, status: 'idle' });
  const [showCircuitDialog, setShowCircuitDialog] = useState(false);
  const [circuitName, setCircuitName] = useState('');
  const [loading, setLoading] = useState(false);

  // Poll for progress updates
  useEffect(() => {
    let interval;
    if (progress.status === 'processing') {
      interval = setInterval(async () => {
        try {
          const response = await axios.get(`${API_BASE_URL}/progress`);
          setProgress(response.data);
          
          // If completed, fetch parts data
          if (response.data.status === 'completed') {
            fetchPartsData();
          }
        } catch (error) {
          console.error('Error fetching progress:', error);
        }
      }, 1000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [progress.status]);

  const fetchPartsData = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/parts`);
      setPartsData(response.data);
    } catch (error) {
      console.error('Error fetching parts data:', error);
    }
  };

  const handleFileUpload = async (fileType, file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE_URL}/upload/${fileType}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setFiles(prev => ({ ...prev, [fileType]: response.data.filename }));
      setPreviews(prev => ({ ...prev, [fileType]: response.data.preview }));

      if (fileType === 'csv' && response.data.chips) {
        setChips(response.data.chips);
        setProgress({ done: 0, total: response.data.total_parts, status: 'processing' });
      }

      return response.data;
    } catch (error) {
      console.error('Upload error:', error);
      throw error;
    }
  };

  const handleShowCircuitName = () => {
    setShowCircuitDialog(true);
  };

  const handleGenerateCircuitName = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/circuit-name`, { chips });
      setCircuitName(response.data.circuit_name);
      setLoading(false);
      return response.data.circuit_name;
    } catch (error) {
      console.error('Error generating circuit name:', error);
      setLoading(false);
      throw error;
    }
  };

  const allFilesUploaded = files.xml && files.csv && files.yaml;

  return (
    <div className="app">
      <div className="card">
        <h1 className="title">WCCA Automation</h1>
        
        <div className="columns">
          <FileUploader
            title="Netlist"
            fileType="xml"
            label=".xml file"
            onUpload={handleFileUpload}
            preview={previews.xml}
            fileName={files.xml}
          />
          
          <FileUploader
            title="Bom"
            fileType="csv"
            label=".csv file"
            onUpload={handleFileUpload}
            preview={previews.csv}
            fileName={files.csv}
          />
          
          <FileUploader
            title="Conditions"
            fileType="yaml"
            label=".yaml file"
            onUpload={handleFileUpload}
            preview={previews.yaml}
            fileName={files.yaml}
          />
        </div>

        {progress.status === 'processing' && (
          <ProgressIndicator done={progress.done} total={progress.total} />
        )}

        {partsData && (
          <div className="parts-section">
            <PartsTable data={partsData} />
          </div>
        )}

        {allFilesUploaded && partsData && (
          <div className="footer">
            <button 
              className="circuit-btn"
              onClick={handleShowCircuitName}
            >
              Show Circuit Name
            </button>
          </div>
        )}

        <div className="note">
          Note: Supported file types are .xml, .csv, and .yaml.
        </div>
      </div>

      {showCircuitDialog && (
        <CircuitNameDialog
          onClose={() => setShowCircuitDialog(false)}
          onGenerate={handleGenerateCircuitName}
          circuitName={circuitName}
          loading={loading}
        />
      )}
    </div>
  );
}

export default App;
