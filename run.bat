@echo off
title NexusForge AI Launcher
echo ==========================================
echo    INITIALIZING NEXUSFORGE AI SYSTEM
echo ==========================================

:: 1. Kontrola Dockeru
echo [1/3] Checking Docker status...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running! 
    echo Please start Docker Desktop and try again.
    pause
    exit
)
echo OK: Docker is active.

:: 2. Spuštění Backend (FastAPI) v novém okně
echo [2/3] Launching Backend Engine (FastAPI)...
start "Nexus-Backend" cmd /k "cd backend && uvicorn main:app --reload --port 8000"

:: Krátká pauza pro nastartování serveru
timeout /t 3 >nul

:: 3. Spuštění Frontend (Electron) v novém okně
echo [3/3] Launching Frontend Interface (Electron)...
start "Nexus-Frontend" cmd /k "npm start"

echo ==========================================
echo    SYSTEM DEPLOYED SUCCESSFULLY
echo ==========================================
echo Close the individual windows to stop the services.
pause