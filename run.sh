#!/bin/bash
# 启动招聘管理系统后端服务

echo "=================================================="
echo "🚀 正在启动 招聘管理系统 (HR Platform) 后端服务..."
echo "📂 共享数据库: PostgreSQL hr_platform"
echo "🌐 API 服务地址: http://127.0.0.1:8000"
echo "=================================================="

# 默认使用 PostgreSQL 双 Schema 权限隔离连接（可由外部环境变量覆盖）
export DATABASE_URL="${DATABASE_URL:-postgresql://user_delivery:delivery_pass@localhost:5432/hr_platform}"

# 运行 uvicorn 服务器（开启自动重载）
# 优先使用 uv 按 requirements.txt 创建隔离运行环境，避免系统 Python 缺少 uvicorn。
if command -v uv >/dev/null 2>&1; then
  uv run --with-requirements requirements.txt uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
else
  python3 -m pip install -r requirements.txt
  python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
fi
