@echo off
echo Starting WCCA Frontend Server...
echo.

cd /d "%~dp0\frontend"

if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

echo.
echo Frontend server starting on http://localhost:3000
echo Press Ctrl+C to stop the server
echo.

npm start
