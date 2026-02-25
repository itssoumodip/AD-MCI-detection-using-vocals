@echo off
echo Starting NeuroVoice AI - AD/MCI Detection System
echo ================================================

:: Start FastAPI backend in a new window
echo [1/2] Starting FastAPI backend on http://127.0.0.1:8000 ...
start "NeuroVoice Backend" cmd /k "cd /d %~dp0backend && uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

:: Wait a moment for the backend to begin starting
timeout /t 2 /nobreak >nul

:: Start Next.js frontend in a new window
echo [2/2] Starting Next.js frontend on http://localhost:3000 ...
start "NeuroVoice Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Both servers are starting in separate windows.
echo   Backend  -^> http://127.0.0.1:8000
echo   Frontend -^> http://localhost:3000
echo   API Docs -^> http://127.0.0.1:8000/docs
echo.
pause
