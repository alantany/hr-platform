Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

Write-Host "=================================================="
Write-Host " 正在初始化数据库表结构"
Write-Host " 范围: public + recruit"
Write-Host " 说明: 仅建表/补列，不写入种子数据"
Write-Host "=================================================="

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  throw "未找到 python，请先安装 Python 3 并加入 PATH"
}

python -m backend.scripts.init_tables
