# IntelliDraft Backend

FastAPI backend for IntelliDraft component documentation system.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Add your OpenRouter API key (get from https://openrouter.ai/keys):
     ```
     OPENROUTER_API_KEY=sk-or-v1-your-key-here
     ```

3. **Run the server**:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## API Endpoints

### POST /api/upload-template
Upload a .docx template file

### POST /api/classify-component
Classify component type from part number using OpenAI

### POST /api/fetch-parameters
Fetch component parameters from Digi-Key API

### POST /api/generate-document
Generate final document with parameters table

### GET /api/download/{filename}
Download generated document

## Directory Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── config.py              # Configuration management
├── routers/
│   └── components.py      # API routes
├── services/
│   ├── openai_service.py  # OpenAI integration
│   ├── digikey_service.py # Digi-Key integration
│   └── document_service.py # Document generation
├── uploads/               # Uploaded templates
└── outputs/               # Generated documents
```
