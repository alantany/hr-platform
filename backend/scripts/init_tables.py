from __future__ import annotations

from backend.app.main import ensure_schema


def main() -> None:
    ensure_schema()
    print("数据库表结构初始化完成（public + recruit）")


if __name__ == "__main__":
    main()
