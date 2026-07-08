@echo off
setlocal EnableExtensions
REM Safely patch missing columns on positions table (no seed, no drop)

cd /d "%~dp0\.."

echo ==================================================
echo  Patch positions missing columns (safe)
echo  Reads DATABASE_URL from .env in project root
echo ==================================================

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python not found. Please install Python 3 and add it to PATH.
  pause
  exit /b 1
)

python -m backend.scripts.patch_positions_columns
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] Patch failed with exit code %EXIT_CODE%
  pause
)
exit /b %EXIT_CODE%
