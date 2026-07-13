@echo off
echo Starting BhagvadGPT Servers...
echo ========================================

echo [1/3] Starting Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
:: Giving Docker 15 seconds to fully initialize its engine before running containers
timeout /t 15 /nobreak >nul

echo [2/3] Starting Backend (Uvicorn)...
:: Launching the backend in a separate terminal window so it stays active
start "BhagvadGPT Backend" cmd /c "cd /d C:\Users\himan\OneDrive\Desktop\projects\bgvdgpt\BhagavadGPT\bhagvadgpt-backend && venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
echo [3/3] Starting Frontend (Docker Compose)...
:: Navigating to the frontend folder and launching Docker in the background
cd /d C:\Users\himan\OneDrive\Desktop\projects\bgvdgpt\BhagavadGPT\BhagvadGPT-frontend
docker-compose up -d

echo ========================================
echo  All servers have been successfully triggered! 
echo Radhe Radhe! 
pause