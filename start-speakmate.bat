@echo off
echo ========================================================
echo   Starting SpeakMate AI - Your Personal English Tutor
echo ========================================================
echo.

start "SpeakMate Backend (FastAPI)" cmd /k "cd /d D:\speakmate-ai\backend && .\venv\Scripts\activate && uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 2 /nobreak >nul

start "SpeakMate Frontend (Vite)" cmd /k "cd /d D:\speakmate-ai\frontend && npm run dev"

echo Backend started at: http://127.0.0.1:8000
echo Frontend started at: http://localhost:5173
echo.
echo Opening browser...
start http://localhost:5173
