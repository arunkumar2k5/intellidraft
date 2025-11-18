import React, { useState } from 'react';
import './PartsTable.css';

function PartsTable({ data }) {
  const [activeTab, setActiveTab] = useState('capacitors');

  const renderTable = (items, columns) => {
    if (!items || items.length === 0) {
      return <div className="empty-state">No data available</div>;
    }

    return (
      <div className="table-container">
        <table className="parts-table">
          <thead>
            <tr>
              {columns.map(col => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {items.map((item, idx) => (
              <tr key={idx}>
                {columns.map(col => (
                  <td key={col}>{item[col] || '-'}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  const capacitorColumns = [
    'Part Number',
    'Mfr',
    'Capacitance',
    'Tolerance',
    'Temperature Coefficient',
    'Operating Temperature'
  ];

  const resistorColumns = [
    'Part Number',
    'Mfr',
    'Resistance',
    'Tolerance',
    'Temperature Coefficient',
    'Operating Temperature'
  ];

  const otherColumns = [
    'Part Number',
    'Mfr',
    'Part Status'
  ];

  return (
    <div className="parts-table-wrapper">
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'capacitors' ? 'active' : ''}`}
          onClick={() => setActiveTab('capacitors')}
        >
          Capacitors ({data.capacitors?.length || 0})
        </button>
        <button
          className={`tab ${activeTab === 'resistors' ? 'active' : ''}`}
          onClick={() => setActiveTab('resistors')}
        >
          Resistors ({data.resistors?.length || 0})
        </button>
        <button
          className={`tab ${activeTab === 'others' ? 'active' : ''}`}
          onClick={() => setActiveTab('others')}
        >
          Others ({data.others?.length || 0})
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'capacitors' && renderTable(data.capacitors, capacitorColumns)}
        {activeTab === 'resistors' && renderTable(data.resistors, resistorColumns)}
        {activeTab === 'others' && renderTable(data.others, otherColumns)}
      </div>
    </div>
  );
}

export default PartsTable;
