#!/bin/bash
# 启动招聘管理系统后端服务

echo "=================================================="
echo "🚀 正在启动 招聘管理系统 (HR Platform) 后端服务..."
echo "📂 共享数据库路径: Recruit/jobs/data/app.db"
echo "🌐 API 服务地址: http://127.0.0.1:8000"
echo "=================================================="

# 默认使用 PostgreSQL 双 Schema 权限隔离连接（可由外部环境变量覆盖）
export DATABASE_URL="${DATABASE_URL:-postgresql://user_delivery:delivery_pass@localhost:5432/hr_platform}"

# 运行 uvicorn 服务器（开启自动重载）
python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
