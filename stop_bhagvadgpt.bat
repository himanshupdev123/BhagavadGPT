@echo off
echo  Shutting Down BhagvadGPT Servers...
echo ========================================

echo [1/2] Stopping Frontend (Docker Compose Down)...
:: Navigating to frontend and cleanly stopping the containers
cd /d C:\Users\himan\OneDrive\Desktop\projects\bgvdgpt\BhagavadGPT\BhagvadGPT-frontend
docker-compose down

echo.
echo [2/2] Stopping Backend (Uvicorn)...
:: Finding the process running on port 8000 (your backend) and terminating it
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /f /pid %%a >nul 2>&1
)
echo Backend window closed.

echo ========================================
echo  All servers have been gracefully shut down.
echo Radhe Radhe! See you next time! 
pause