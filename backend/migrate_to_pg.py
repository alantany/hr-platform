import sys
from pathlib import Path
from sqlalchemy import create_engine, text, inspect, Boolean
from sqlalchemy.orm import Session

# 将项目根目录加入 sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app.config import settings
from backend.app.models import Base

# 配置源数据库 (SQLite) 和目标数据库 (PostgreSQL)
SQLITE_URL = f"sqlite:///{(Path(__file__).resolve().parents[1] / 'Recruit' / 'jobs' / 'data' / 'app.db').as_posix()}"
PG_URL = "postgresql://localhost:5432/hr_platform"  # 使用管理员权限导入以忽略外键

def migrate():
    print("⏳ 开始数据迁移...")
    print(f"🔌 源数据库 (SQLite): {SQLITE_URL}")
    print(f"🔌 目标数据库 (PostgreSQL): {PG_URL}")

    sqlite_engine = create_engine(SQLITE_URL, future=True)
    pg_engine = create_engine(PG_URL, future=True)

    # 1. 获取所有表名
    inspector = inspect(sqlite_engine)
    tables = inspector.get_table_names()
    print(f"📋 发现 {len(tables)} 张表需要迁移。")

    # 2. 连接 PG 数据库并执行复制
    with pg_engine.begin() as pg_conn, sqlite_engine.connect() as sq_conn:
        # 禁用外键约束检查以保证平滑迁移
        pg_conn.execute(text("SET session_replication_role = 'replica';"))

        # 一次性清空所有目标表，防范先后 TRUNCATE CASCADE 造成已迁移数据被级联抹除
        print("🧹 正在清空目标数据库中的所有表...")
        truncate_targets = []
        for table in tables:
            recruit_tables = {"candidate_profiles", "resume_downloads", "employees", "job_postings", "daily_task_stats"}
            schema = "recruit" if table in recruit_tables else "public"
            truncate_targets.append(f'"{schema}"."{table}"')
        
        truncate_sql = f"TRUNCATE TABLE {', '.join(truncate_targets)} CASCADE;"
        pg_conn.execute(text(truncate_sql))

        for table in tables:
            print(f"🔄 正在迁移表: {table} ...")
            recruit_tables = {"candidate_profiles", "resume_downloads", "employees", "job_postings", "daily_task_stats"}
            schema = "recruit" if table in recruit_tables else "public"
            target_table_name = f'"{schema}"."{table}"'

            # 获取当前表的列定义，识别哪些是 BOOLEAN 类型
            boolean_columns = set()
            try:
                columns_info = inspector.get_columns(table)
                for c in columns_info:
                    if isinstance(c["type"], Boolean) or str(c["type"]).lower().startswith("boolean"):
                        boolean_columns.add(c["name"])
            except Exception as e:
                print(f"⚠️ 无法读取列类型 {table}: {e}")

            # 查询 SQLite 数据
            result = sq_conn.execute(text(f"SELECT * FROM {table}"))
            keys = result.keys()
            
            rows = []
            for row in result.fetchall():
                row_dict = dict(zip(keys, row))
                # 将 SQLite 的 1/0 转换为 PG 所需的 True/False Boolean 值
                for col in boolean_columns:
                    if col in row_dict and row_dict[col] is not None:
                        row_dict[col] = bool(row_dict[col])
                rows.append(row_dict)

            if not rows:
                print(f"ℹ️ 表 {table} 无数据，已跳过。")
                continue

            # 插入 PostgreSQL 并对列名使用标准 SQL 双引号转义（防范 'user' 等保留字语法错误）
            columns = ", ".join([f'"{k}"' for k in keys])
            placeholders = ", ".join([f":{k}" for k in keys])
            insert_sql = text(f"INSERT INTO {target_table_name} ({columns}) VALUES ({placeholders})")
            
            pg_conn.execute(insert_sql, rows)
            print(f"✅ 成功导入 {len(rows)} 条数据到 {target_table_name}。")

        # 重新启用外键检查
        pg_conn.execute(text("SET session_replication_role = 'origin';"))
        
        # 3. 修复自增序列 (Sequence) 计数
        print("🔄 正在修复自增序列计数...")
        for table in tables:
            recruit_tables = {"candidate_profiles", "resume_downloads", "employees", "job_postings", "daily_task_stats"}
            schema = "recruit" if table in recruit_tables else "public"
                
            # 检查表是否有 'id' 列
            columns = [c["name"] for c in inspector.get_columns(table)]
            if "id" in columns:
                seq_query = f"SELECT setval(pg_get_serial_sequence('{schema}.{table}', 'id'), COALESCE(MAX(id), 1)) FROM {schema}.{table};"
                try:
                    pg_conn.execute(text(seq_query))
                except Exception as e:
                    # 如果列不是 serial 类型或无关联 sequence，可忽略
                    pass

    print("🎉 所有数据已成功从 SQLite 迁移同步至 PostgreSQL 数据库！")

if __name__ == "__main__":
    migrate()
