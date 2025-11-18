@echo off
echo Starting WCCA Backend Server...
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

echo.
echo Backend server starting on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

cd backend
python app.py
