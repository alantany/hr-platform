Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

Write-Host "=================================================="
Write-Host " 正在启动 AI 简历解析守护进程"
Write-Host " 配置来源: 项目根目录 .env (DEEPSEEK_* / DATABASE_URL)"
Write-Host " 按 Ctrl+C 可停止"
Write-Host "=================================================="

$venvActivate = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"
if (-not (Test-Path $venvActivate)) {
  $venvActivate = Join-Path $PSScriptRoot "venv\Scripts\Activate.ps1"
}
if (Test-Path $venvActivate) {
  . $venvActivate
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  throw "未找到 python，请先安装 Python 3 并加入 PATH"
}

if (-not (Test-Path (Join-Path $PSScriptRoot ".env"))) {
  Write-Warning ".env 不存在，请从 .env.example 复制并填写 DEEPSEEK_* 与 DATABASE_URL"
}

python backend\scripts\resume_parser_worker.py
