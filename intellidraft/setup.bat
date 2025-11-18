@echo off
echo ========================================
echo IntelliDraft Setup Script
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.10 or higher.
    pause
    exit /b 1
)
echo.

echo [2/4] Checking Node.js installation...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found. Please install Node.js 18 or higher.
    pause
    exit /b 1
)
echo.

echo [3/4] Setting up Backend...
cd backend
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit backend\.env and add your OpenRouter API key!
    echo Get your key from: https://openrouter.ai/keys
    echo.
)

echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
cd ..
echo.

echo [4/4] Setting up Frontend...
cd frontend
echo Installing Node dependencies (this may take a few minutes)...
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Node dependencies
    pause
    exit /b 1
)
cd ..
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit backend\.env and add your OpenRouter API key
echo    Get from: https://openrouter.ai/keys
echo 2. Run start-backend.bat to start the backend server
echo 3. Run start-frontend.bat to start the frontend
echo.
echo See QUICKSTART.md for detailed instructions
echo.
pause
