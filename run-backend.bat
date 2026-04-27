@echo off
REM Convenience launcher for backend server
cd /d "%~dp0\backend"

echo.
echo  Starting AI Examination System...
echo  The app will open at: http://localhost:5000
echo.

REM Open browser after 3-second delay (runs in background)
start /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

call start.bat
