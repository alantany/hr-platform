@echo off
setlocal EnableExtensions
REM 第 2 步：初始化数据库表结构（只建表，不导数据）

cd /d "%~dp0\.."

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] 未找到 python，请先安装 Python 3 并加入 PATH
  pause
  exit /b 1
)

python -m backend.scripts.init_tables
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] 表结构初始化失败，退出码 %EXIT_CODE%
  pause
)
exit /b %EXIT_CODE%
