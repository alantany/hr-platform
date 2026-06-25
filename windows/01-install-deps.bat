@echo off
setlocal EnableExtensions
REM Step 1: install Python dependencies

cd /d "%~dp0\.."

if not exist "requirements.txt" (
  echo [ERROR] requirements.txt not found
  pause
  exit /b 1
)

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python not found. Please install Python 3 and add it to PATH.
  pause
  exit /b 1
)

python -m pip install -r requirements.txt
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] Dependency installation failed with exit code %EXIT_CODE%
  pause
  exit /b %EXIT_CODE%
)
echo [OK] Dependencies installed successfully.
exit /b %EXIT_CODE%
