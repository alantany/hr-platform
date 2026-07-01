import os
import sys
from pathlib import Path
import alembic.config

def load_env():
    """手动从 .env 文件读取环境变量，避免依赖外部库"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def run_migrations():
    print("=== 开始同步数据库表结构（执行 Alembic 迁移） ===")
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("错误：未能在 .env 中找到 DATABASE_URL")
        sys.exit(1)
        
    print(f"使用的数据库连接: {db_url}")
    
    alembicArgs = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    try:
        alembic.config.main(argv=alembicArgs)
        print("表结构迁移完成！")
    except Exception as e:
        print(f"表结构迁移失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 1. 加载 .env 里的配置
    load_env()
    
    # 2. 为了让 Alembic 能找到应用模块，确保当前目录在 sys.path 中
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # 3. 运行表结构同步
    run_migrations()
