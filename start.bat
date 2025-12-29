@echo off
REM Quick Setup Script for DataBridge AI (Windows)

echo ============================================================
echo DataBridge AI - Quick Setup
echo ============================================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo [OK] Docker is running

REM Check if .env exists
if not exist .env (
    echo.
    echo [SETUP] Creating .env file from template...
    copy .env.example .env
    echo [WARNING] Please edit .env and add your OPENAI_API_KEY
    echo.
    notepad .env
)

echo.
echo [INFO] Starting Docker containers...
echo This may take a few minutes on first run...
echo.

docker-compose up --build -d

if errorlevel 1 (
    echo [ERROR] Failed to start containers
    pause
    exit /b 1
)

echo.
echo [INFO] Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo.
echo [INFO] Initializing database...
docker-compose exec -T backend python init_db.py

if errorlevel 1 (
    echo [WARNING] Database initialization failed. Retrying in 5 seconds...
    timeout /t 5 /nobreak >nul
    docker-compose exec -T backend python init_db.py
)

echo.
echo ============================================================
echo DataBridge AI is ready!
echo ============================================================
echo.
echo Access the application:
echo   - Frontend UI:  http://localhost:8501
echo   - Backend API:  http://localhost:8000
echo   - API Docs:     http://localhost:8000/docs
echo.
echo To view logs:      docker-compose logs -f
echo To stop:           docker-compose down
echo To restart:        docker-compose restart
echo.
echo See QUICKSTART.md for more information.
echo.
pause
