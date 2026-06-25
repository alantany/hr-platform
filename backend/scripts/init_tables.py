from __future__ import annotations

from backend.app.main import ensure_schema


def main() -> None:
    ensure_schema()
    print("Database tables initialized (public + recruit)")


if __name__ == "__main__":
    main()
