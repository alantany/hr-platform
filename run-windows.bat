@echo off
setlocal EnableExtensions
REM Windows startup entry: backend FastAPI only
REM Requires Python 3 and a reachable PostgreSQL server

cd /d "%~dp0"

echo ==================================================
echo  Starting AI Recruitment Platform backend
echo  Shared database: PostgreSQL hr_platform
echo  API address: http://127.0.0.1:8000
echo ==================================================

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python not found. Please install Python 3 and add it to PATH.
  pause
  exit /b 1
)

python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] Service start failed with exit code %EXIT_CODE%
  pause
)
exit /b %EXIT_CODE%
