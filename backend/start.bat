@echo off
REM Startup script for AI Examination System Backend

echo ================================================
echo   AI Examination System - Backend Server
echo ================================================
echo.

REM Change to the directory where this script is located
cd /d "%~dp0"
echo Current directory: %cd%
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/Updating dependencies...
pip install -r requirements.txt --quiet
echo.

echo Starting Flask server...
echo Backend will run on: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
