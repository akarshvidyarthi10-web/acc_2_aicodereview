@echo off
REM AI Code Review Agent - Quick Start Script (Windows)

echo ============================================
echo AI Code Review Agent - Starting Services
echo ============================================

REM Check if backend/.env exists
if not exist "backend\.env" (
    echo.
    echo [ERROR] backend\.env not found!
    echo Please create backend\.env first using backend\.env.example as template
    echo.
    pause
    exit /b 1
)

echo.
echo [1] Starting MongoDB (if not running)...
echo Note: Make sure MongoDB is running on localhost:27017
echo You can start it with: docker run -d -p 27017:27017 --name mongodb mongo:latest
echo.

echo [2] Starting Backend on http://localhost:8000
start "Backend" cmd /k "cd backend && .venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 2 /nobreak

echo [3] Starting Frontend on http://localhost:4173
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================
echo Services starting...
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:4173
echo Docs:     http://localhost:8000/docs
echo Health:   http://localhost:8000/health
echo.
echo For webhooks, use ngrok: ngrok http 8000
echo ============================================
