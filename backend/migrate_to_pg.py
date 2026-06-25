from __future__ import annotations

import os
import sys
from pathlib import Path

from sqlalchemy import create_engine, inspect, text

# 将项目根目录加入 sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app.config import settings


SOURCE_DATABASE_URL = os.getenv("SOURCE_DATABASE_URL")
TARGET_DATABASE_URL = os.getenv("TARGET_DATABASE_URL", settings.database_url)
RECRUIT_SCHEMAS = ("public", "recruit")


def _list_tables(engine):
    inspector = inspect(engine)
    tables: list[tuple[str, str]] = []
    for schema in RECRUIT_SCHEMAS:
        try:
            names = inspector.get_table_names(schema=schema)
        except Exception:
            continue
        for table in names:
            if table != "alembic_version":
                tables.append((schema, table))
    return tables


def sync():
    if not SOURCE_DATABASE_URL:
        raise SystemExit("请先设置 SOURCE_DATABASE_URL")
    if not TARGET_DATABASE_URL:
        raise SystemExit("请先设置 TARGET_DATABASE_URL")
    if SOURCE_DATABASE_URL == TARGET_DATABASE_URL:
        raise SystemExit("SOURCE_DATABASE_URL 与 TARGET_DATABASE_URL 不能相同")

    print("⏳ 开始 PostgreSQL 数据同步...")
    print(f"🔌 源数据库 (PostgreSQL): {SOURCE_DATABASE_URL}")
    print(f"🔌 目标数据库 (PostgreSQL): {TARGET_DATABASE_URL}")

    source_engine = create_engine(SOURCE_DATABASE_URL, future=True)
    target_engine = create_engine(TARGET_DATABASE_URL, future=True)

    tables = _list_tables(source_engine)
    print(f"📋 发现 {len(tables)} 张表需要同步。")

    with target_engine.begin() as target_conn, source_engine.connect() as source_conn:
        if any(schema == "recruit" for schema, _ in tables):
            target_conn.execute(text("CREATE SCHEMA IF NOT EXISTS recruit"))

        print("🧹 正在清空目标数据库中的相关表...")
        if tables:
            truncate_targets = [f'"{schema}"."{table}"' for schema, table in tables]
            target_conn.execute(text(f"TRUNCATE TABLE {', '.join(truncate_targets)} RESTART IDENTITY CASCADE;"))

        inspector = inspect(source_engine)
        for schema, table in tables:
            print(f"🔄 正在同步表: {schema}.{table} ...")
            columns_info = inspector.get_columns(table, schema=schema)
            columns = [col["name"] for col in columns_info]
            if not columns:
                print(f"ℹ️ 表 {schema}.{table} 无列信息，已跳过。")
                continue

            quoted_columns = ", ".join([f'"{c}"' for c in columns])
            select_sql = text(f'SELECT {quoted_columns} FROM "{schema}"."{table}"')
            rows = source_conn.execute(select_sql).mappings().all()
            if not rows:
                print(f"ℹ️ 表 {schema}.{table} 无数据，已跳过。")
                continue

            placeholders = ", ".join([f":{c}" for c in columns])
            insert_sql = text(
                f'INSERT INTO "{schema}"."{table}" '
                f"({quoted_columns}) "
                f"VALUES ({placeholders})"
            )
            target_conn.execute(insert_sql, rows)
            print(f"✅ 成功同步 {len(rows)} 条数据到 {schema}.{table}。")

        print("🔄 正在修复自增序列计数...")
        for schema, table in tables:
            columns = [c["name"] for c in inspector.get_columns(table, schema=schema)]
            if "id" not in columns:
                continue
            seq_query = text(
                f"SELECT setval(pg_get_serial_sequence('{schema}.{table}', 'id'), COALESCE(MAX(id), 1)) "
                f"FROM \"{schema}\".\"{table}\";"
            )
            try:
                target_conn.execute(seq_query)
            except Exception:
                pass

    print("🎉 所有数据已成功在 PostgreSQL 数据库之间同步完成！")


if __name__ == "__main__":
    sync()
