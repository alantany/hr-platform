"""Safely add missing columns on positions table (idempotent, no data loss)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

POSITION_PATCHES = {
    "owner_user_id": "ALTER TABLE positions ADD COLUMN owner_user_id INTEGER",
    "age_requirement": "ALTER TABLE positions ADD COLUMN age_requirement TEXT NOT NULL DEFAULT ''",
    "education_requirement": "ALTER TABLE positions ADD COLUMN education_requirement TEXT NOT NULL DEFAULT ''",
    "experience_requirement": "ALTER TABLE positions ADD COLUMN experience_requirement TEXT NOT NULL DEFAULT ''",
    "requirement_tags": "ALTER TABLE positions ADD COLUMN requirement_tags JSON",
    "target_resume_count": "ALTER TABLE positions ADD COLUMN target_resume_count INTEGER NOT NULL DEFAULT 10",
    "description": "ALTER TABLE positions ADD COLUMN description TEXT NOT NULL DEFAULT ''",
}


def main() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise SystemExit("[ERROR] DATABASE_URL is missing. Please set it in .env")

    engine = create_engine(database_url)
    inspector = inspect(engine)
    existing = {col["name"] for col in inspector.get_columns("positions")}

    added = 0
    skipped = 0
    with engine.begin() as conn:
        for column, ddl in POSITION_PATCHES.items():
            if column in existing:
                print(f"[SKIP] positions.{column} already exists")
                skipped += 1
                continue
            conn.execute(text(ddl))
            print(f"[OK]   added positions.{column}")
            added += 1

    print(f"Done. added={added}, skipped={skipped}")


if __name__ == "__main__":
    main()
