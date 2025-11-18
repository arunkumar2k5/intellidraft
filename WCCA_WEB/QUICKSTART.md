# Quick Start Guide

## 🚀 Running the Application

### Option 1: Using Batch Scripts (Windows)

1. **Start Backend Server:**
   - Double-click `start_backend.bat`
   - Wait for "Running on http://127.0.0.1:5000" message

2. **Start Frontend Server:**
   - Double-click `start_frontend.bat`
   - Browser will automatically open to http://localhost:3000

### Option 2: Manual Start

#### Terminal 1 - Backend
```bash
cd c:\Users\HP\Documents\Codes\WCCA
.\venv\Scripts\activate
cd backend
python app.py
```

#### Terminal 2 - Frontend
```bash
cd c:\Users\HP\Documents\Codes\WCCA\frontend
npm start
```

## 📋 First Time Setup

### Backend
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## 🎯 Using the Application

1. **Upload Files:**
   - Click "Browse" for each file type (XML, CSV, YAML)
   - Select appropriate files
   - Preview will appear automatically

2. **Wait for Processing:**
   - After uploading CSV, DigiKey search starts automatically
   - Progress indicator shows completion status

3. **View Parts Data:**
   - Parts table appears when processing completes
   - Switch between Capacitors, Resistors, and Others tabs

4. **Generate Circuit Name:**
   - Click "Show Circuit Name" button
   - AI generates circuit name based on ICs
   - Option to enter manually if needed

## ⚠️ Important Notes

- Backend must be running before starting frontend
- Both servers must run simultaneously
- Default ports: Backend (5000), Frontend (3000)
- Ensure API keys are configured in `digikey.py` and `gen_ai.py`

## 🔧 Troubleshooting

**Backend won't start:**
- Check if port 5000 is already in use
- Verify virtual environment is activated
- Ensure all dependencies are installed

**Frontend won't start:**
- Check if port 3000 is already in use
- Delete `node_modules` and run `npm install` again
- Clear browser cache

**API connection errors:**
- Verify backend is running
- Check browser console for CORS errors
- Ensure proxy is configured in `package.json`

## 📞 Need Help?

See `README_WEB.md` for detailed documentation.
