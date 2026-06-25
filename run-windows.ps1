Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

Write-Host "=================================================="
Write-Host " 正在启动 AI招聘管理平台 后端服务"
Write-Host " 共享数据库: PostgreSQL hr_platform"
Write-Host " API 服务地址: http://127.0.0.1:8000"
Write-Host "=================================================="

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  throw "未找到 python，请先安装 Python 3 并加入 PATH"
}

python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
