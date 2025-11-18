# WCCA Automation - Web Application

A web-based version of the WCCA (Worst Case Circuit Analysis) Automation tool, built with React frontend and Flask backend.

## 🏗️ Architecture

- **Frontend**: React with modern UI components
- **Backend**: Flask REST API
- **Integration**: Easy to integrate with other applications

## 📁 Project Structure

```
WCCA/
├── backend/
│   ├── app.py              # Flask API server
│   ├── __init__.py
│   └── .env.example
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── FileUploader.js
│   │   │   ├── PartsTable.js
│   │   │   ├── CircuitNameDialog.js
│   │   │   └── ProgressIndicator.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── .env.example
├── digikey.py              # DigiKey API integration
├── gen_ai.py               # Google GenAI integration
├── excel_to_json.py        # Excel conversion utility
├── json_table.py           # (Legacy - not used in web version)
├── main.py                 # (Legacy Tkinter version)
└── requirements.txt        # Python dependencies
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to the project root:**
   ```bash
   cd c:\Users\HP\Documents\Codes\WCCA
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional):**
   ```bash
   cd backend
   copy .env.example .env
   # Edit .env with your configuration
   ```

5. **Start the Flask server:**
   ```bash
   cd backend
   python app.py
   ```
   
   The backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables (optional):**
   ```bash
   copy .env.example .env
   # Edit .env if you need to change API URL
   ```

4. **Start the React development server:**
   ```bash
   npm start
   ```
   
   The frontend will run on `http://localhost:3000`

## 🎯 Features

### File Upload & Processing
- **Netlist (.xml)**: Upload circuit netlist files
- **BOM (.csv)**: Upload Bill of Materials with automatic part number extraction
- **Conditions (.yaml)**: Upload constraint/condition files
- Real-time file preview for all uploaded files

### DigiKey Integration
- Automatic part lookup via DigiKey API
- Real-time progress tracking with visual indicator
- Categorized parts display (Capacitors, Resistors, Others)

### AI-Powered Circuit Identification
- Uses Google GenAI to identify circuit type based on IC components
- Manual circuit name entry option
- Smart chip detection from BOM reference designators

### Modern UI
- Dark theme matching original Tkinter design
- Responsive layout
- Tabbed parts table view
- Modal dialogs for circuit name

## 🔌 API Endpoints

### Health Check
```
GET /api/health
```

### File Upload
```
POST /api/upload/<file_type>
Content-Type: multipart/form-data

Parameters:
- file_type: xml, csv, or yaml
- file: The file to upload
```

### Progress Tracking
```
GET /api/progress

Response:
{
  "done": 10,
  "total": 50,
  "status": "processing"
}
```

### Parts Data
```
GET /api/parts

Response:
{
  "capacitors": [...],
  "resistors": [...],
  "others": [...],
  "total": 50
}
```

### Circuit Name Generation
```
POST /api/circuit-name
Content-Type: application/json

Body:
{
  "chips": ["IC1", "IC2", ...]
}

Response:
{
  "circuit_name": "Power Supply Circuit"
}
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env`:
```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
UPLOAD_FOLDER=~/WCCA_Uploads
MAX_FILE_SIZE=26214400
CORS_ORIGINS=http://localhost:3000
```

### Frontend Configuration

Edit `frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:5000/api
```

## 🔐 API Keys

The application requires API keys for:

1. **DigiKey API**: Update credentials in `digikey.py`
   ```python
   client_id = "your_client_id"
   client_secret = "your_client_secret"
   ```

2. **Google GenAI**: Update API key in `gen_ai.py`
   ```python
   api_key = "your_google_genai_key"
   ```

## 🚢 Production Deployment

### Backend Deployment

1. Use a production WSGI server (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
   ```

2. Configure environment variables for production
3. Set up reverse proxy (nginx/Apache)
4. Enable HTTPS

### Frontend Deployment

1. Build the React app:
   ```bash
   cd frontend
   npm run build
   ```

2. Serve the `build` folder using:
   - Static hosting (Netlify, Vercel, GitHub Pages)
   - Web server (nginx, Apache)
   - CDN

3. Update `REACT_APP_API_URL` to point to production backend

## 🔄 Integration with Other Applications

The Flask backend is designed for easy integration:

1. **RESTful API**: All endpoints follow REST conventions
2. **CORS Enabled**: Cross-origin requests are supported
3. **JSON Responses**: All data returned in JSON format
4. **Modular Design**: Import and use backend functions in other Python apps

### Example Integration

```python
from backend.app import app
from flask import Flask

# Your existing Flask app
my_app = Flask(__name__)

# Register WCCA routes with a prefix
my_app.register_blueprint(app, url_prefix='/wcca')
```

## 📝 Notes

- The original Tkinter version (`main.py`) is preserved for reference
- File uploads are stored in `~/WCCA_Uploads` by default
- Maximum file size is 25MB
- DigiKey API has rate limits - adjust accordingly
- Google GenAI requires valid API key

## 🐛 Troubleshooting

### Backend Issues

- **Port already in use**: Change port in `app.py` or kill existing process
- **Module not found**: Ensure virtual environment is activated and dependencies installed
- **CORS errors**: Check CORS configuration in `app.py`

### Frontend Issues

- **API connection failed**: Verify backend is running and URL is correct
- **Build errors**: Delete `node_modules` and run `npm install` again
- **Proxy not working**: Restart React dev server after changing proxy settings

## 📄 License

Same as original WCCA project.
