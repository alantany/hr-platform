@echo off
setlocal EnableExtensions
REM Step 3: start backend service

cd /d "%~dp0\.."

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python not found. Please install Python 3 and add it to PATH.
  pause
  exit /b 1
)

python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] Backend start failed with exit code %EXIT_CODE%
  pause
)
exit /b %EXIT_CODE%
