#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections.abc import Iterable
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app.database import SessionLocal
from backend.test_cleanup import cleanup_models, full_reset_database, table_exists


def _count_rows(db, models: Iterable[type]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for model in models:
        if not table_exists(db, model):
            continue
        counts[model.__tablename__] = db.query(model).count()
    return counts


def dry_run() -> None:
    db = SessionLocal()
    try:
        counts = _count_rows(db, cleanup_models())
        total = sum(counts.values())
        print(f"tables={len(counts)} rows={total}")
        for name, count in sorted(counts.items(), key=lambda item: item[0]):
            print(f"{name}: {count}")
    finally:
        db.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean test data and reset seed rows for the recruitment platform.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be cleaned without modifying the database.")
    args = parser.parse_args()

    if args.dry_run:
        dry_run()
        return 0

    full_reset_database()
    print("test data cleaned and seed rows restored")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
