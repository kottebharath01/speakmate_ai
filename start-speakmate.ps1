Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Starting SpeakMate AI - Your Personal English Tutor" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Start backend in a separate window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'D:\speakmate-ai\backend'; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

Start-Sleep -Seconds 2

# Start frontend in a separate window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'D:\speakmate-ai\frontend'; npm run dev"

Start-Sleep -Seconds 2
Start-Process "http://localhost:5173"
