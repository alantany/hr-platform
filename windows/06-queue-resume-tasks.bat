@echo off
setlocal EnableExtensions
REM Step 6: one-time batch queue of resume parse tasks

cd /d "%~dp0\.."

echo ==================================================
echo  Queue resume parse tasks (one-time batch)
echo  Reads DATABASE_URL from .env in project root
echo ==================================================

if exist ".venv\Scripts\activate.bat" (
  call ".venv\Scripts\activate.bat"
) else if exist "venv\Scripts\activate.bat" (
  call "venv\Scripts\activate.bat"
)

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python not found. Please install Python 3 and add it to PATH.
  pause
  exit /b 1
)

if not exist ".env" (
  echo [WARN] .env not found. Copy .env.example to .env and fill in DATABASE_URL.
)

python backend\scripts\queue_resume_tasks.py
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] Queue script failed with exit code %EXIT_CODE%
  pause
)
exit /b %EXIT_CODE%
