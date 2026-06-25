@echo off
setlocal EnableExtensions
REM Initialize tables only (no seed data)
REM Requires Python 3 and a reachable PostgreSQL server

cd /d "%~dp0"

echo ==================================================
echo  Initializing database table structures
echo  Scope: public + recruit
echo  Note: tables/columns only, no seed data
echo ==================================================

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
)
exit /b %EXIT_CODE%
