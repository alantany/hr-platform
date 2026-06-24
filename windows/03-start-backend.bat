@echo off
setlocal EnableExtensions
REM 第 3 步：启动后端服务

cd /d "%~dp0\.."

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] 未找到 python，请先安装 Python 3 并加入 PATH
  pause
  exit /b 1
)

python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] 后端启动失败，退出码 %EXIT_CODE%
  pause
)
exit /b %EXIT_CODE%
