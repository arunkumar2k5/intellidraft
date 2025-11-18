# IntelliDraft

AI-powered component documentation system for electronic components.

## Overview

IntelliDraft automates the process of creating technical documentation for electronic components by:
1. Using OpenRouter AI to classify component types
2. Fetching detailed parameters from Digi-Key API
3. Generating professional documentation with editable parameter tables

## Phase 1 Features

- ✅ Template-based document generation (.docx)
- ✅ OpenRouter AI-powered component classification
- ✅ Digi-Key API integration for parameter extraction
- ✅ Editable parameter tables
- ✅ Automatic Functional Description section updates
- ✅ Single component processing
- 🔄 Batch processing (Phase 2)

## Technology Stack

### Backend
- **Python 3.10+**
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **OpenRouter API** - Component classification (supports multiple LLM models)
- **python-docx** - Document manipulation
- **Digi-Key API** - Parameter extraction

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Axios** - HTTP client

## Project Structure

```
intellidraft/
├── backend/                    # FastAPI backend
│   ├── main.py                # Entry point
│   ├── config.py              # Configuration
│   ├── routers/               # API routes
│   ├── services/              # Business logic
│   ├── uploads/               # Uploaded templates
│   ├── outputs/               # Generated documents
│   └── requirements.txt       # Python dependencies
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API client
│   │   └── App.jsx           # Main app
│   └── package.json          # Node dependencies
└── Library/                   # Shared resources
    ├── digikey.py            # Digi-Key integration
    └── parameters.json       # Component parameter definitions
```

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- OpenRouter API key (get from https://openrouter.ai/keys)
- Digi-Key API credentials

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   ```
   Get your key from: https://openrouter.ai/keys

5. Run the backend server:
   ```bash
   python main.py
   ```
   
   Backend will be available at: http://localhost:8000
   API docs: http://localhost:8000/docs

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```
   
   Frontend will be available at: http://localhost:3000

## Usage

### Single Component Processing

1. **Upload Template**
   - Click "Upload Template" and select your .docx file
   - Template must have a "2. Functional Description" section

2. **Search Component**
   - Enter the component part number (e.g., GCM1885C1H180JA16D)
   - Click "Search" button

3. **Review & Edit Parameters**
   - AI will classify the component type
   - Parameters will be fetched from Digi-Key
   - Edit any values in the parameter table

4. **Generate Document**
   - Click "Generate Document"
   - Document will be created with updated Functional Description
   - File will be named after the part number

## API Endpoints

### POST /api/upload-template
Upload a .docx template file

### POST /api/classify-component
Classify component type using OpenRouter AI
```json
{
  "part_number": "GCM1885C1H180JA16D"
}
```

### POST /api/fetch-parameters
Fetch parameters from Digi-Key
```json
{
  "part_number": "GCM1885C1H180JA16D",
  "component_type": "capacitor"
}
```

### POST /api/generate-document
Generate final document
```json
{
  "template_path": "path/to/template.docx",
  "part_number": "GCM1885C1H180JA16D",
  "component_type": "capacitor",
  "parameters": { ... }
}
```

### GET /api/download/{filename}
Download generated document

## Component Types Supported

- **Resistor** - resistance, tolerance, power rating, etc.
- **Capacitor** - capacitance, voltage rating, dielectric, etc.
- **Inductor** - inductance, current rating, DCR, etc.
- **Diode** - voltage, current, forward voltage, etc.
- **Transistor** - Vce, Ic, hFE, power dissipation, etc.

More types can be added by updating `Library/parameters.json`

## Development

### Adding New Component Types

Edit `Library/parameters.json`:
```json
{
  "new_component_type": {
    "description": "Component description",
    "key_parameters": [
      "parameter1",
      "parameter2"
    ]
  }
}
```

### Customizing Document Generation

Edit `backend/services/document_service.py` to modify how the Functional Description section is formatted.

## Troubleshooting

### Backend Issues
- Ensure Python 3.10+ is installed
- Check `.env` file has valid OpenRouter API key
- Verify Digi-Key credentials in `Library/digikey.py`

### Frontend Issues
- Clear browser cache
- Check backend is running on port 8000
- Verify CORS settings in `backend/main.py`

### Document Generation Issues
- Ensure template has "2. Functional Description" section
- Check template is valid .docx format
- Verify write permissions in `backend/outputs/` directory

## Future Enhancements (Phase 2+)

- [ ] Batch processing with CSV upload
- [ ] Support for more component types
- [ ] Custom parameter mapping
- [ ] Document templates library
- [ ] User authentication
- [ ] Processing history
- [ ] Export to multiple formats (PDF, HTML)

## License

Proprietary - Internal Use Only

## Support

For issues or questions, contact the development team.
