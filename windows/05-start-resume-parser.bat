@echo off
setlocal EnableExtensions
REM Step 5: start AI resume parser daemon worker

cd /d "%~dp0\.."

echo ==================================================
echo  Starting AI Resume Parser Worker (Daemon)
echo  Reads DEEPSEEK_* and DATABASE_URL from .env
echo  Press Ctrl+C to stop
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
  echo [WARN] .env not found. Copy .env.example to .env and fill in DEEPSEEK_* and DATABASE_URL.
)

python backend\scripts\resume_parser_worker.py
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] Resume parser worker exited with code %EXIT_CODE%
  pause
)
exit /b %EXIT_CODE%
