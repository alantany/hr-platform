@echo off
setlocal EnableExtensions
REM Step 2: initialize database tables only (no seed data)

cd /d "%~dp0\.."

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python not found. Please install Python 3 and add it to PATH.
  pause
  exit /b 1
)

python -m backend.scripts.init_tables
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] Table initialization failed with exit code %EXIT_CODE%
  pause
  exit /b %EXIT_CODE%
)
echo [OK] Database tables initialized successfully.
exit /b %EXIT_CODE%
