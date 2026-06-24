@echo off
setlocal EnableExtensions
REM 第 1 步：安装 Python 依赖

cd /d "%~dp0\.."

if not exist "requirements.txt" (
  echo [ERROR] 找不到 requirements.txt
  pause
  exit /b 1
)

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] 未找到 python，请先安装 Python 3 并加入 PATH
  pause
  exit /b 1
)

python -m pip install -r requirements.txt
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] 依赖安装失败，退出码 %EXIT_CODE%
  pause
)
exit /b %EXIT_CODE%
