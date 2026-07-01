import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text

def load_env():
    """手动从 .env 文件读取环境变量"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def add_columns_safely():
    print("=== 开始同步表结构（跳过Alembic历史，直接检查并添加字段） ===")
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("错误：未能在 .env 中找到 DATABASE_URL")
        sys.exit(1)
        
    print(f"使用的数据库连接: {db_url}")
    
    try:
        engine = create_engine(db_url)
        with engine.begin() as conn:
            print("正在检查并添加 delivery_status 字段...")
            conn.execute(text("ALTER TABLE candidates ADD COLUMN IF NOT EXISTS delivery_status VARCHAR(32) NOT NULL DEFAULT '未推荐';"))
            
            print("正在检查并添加 candidate_warranty_status 字段...")
            conn.execute(text("ALTER TABLE candidates ADD COLUMN IF NOT EXISTS candidate_warranty_status VARCHAR(32) NOT NULL DEFAULT '';"))
            
        print("\n表结构同步完成！两个新字段已成功添加（如果已存在则自动跳过）。")
    except Exception as e:
        print(f"\n表结构同步失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    load_env()
    add_columns_safely()
