@echo off
setlocal EnableExtensions
REM Connect to project PostgreSQL via psql (use 127.0.0.1 to avoid IPv6 ::1 issues)

cd /d "%~dp0"

where psql >nul 2>nul
if errorlevel 1 (
  echo [ERROR] psql not found. Install PostgreSQL and add its bin folder to PATH.
  echo Example: C:\Program Files\PostgreSQL\17\bin
  pause
  exit /b 1
)

echo Connecting to hr_platform as user_delivery ...
psql "postgresql://user_delivery:delivery_pass@127.0.0.1:5432/hr_platform"
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] psql exited with code %EXIT_CODE%
  pause
)
exit /b %EXIT_CODE%
