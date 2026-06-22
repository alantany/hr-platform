from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    app_name: str = "hr-platform"
    api_prefix: str = "/api"
    database_url: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{(BASE_DIR / 'Recruit' / 'jobs' / 'data' / 'app.db').as_posix()}",
    )
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key")
    access_token: str = os.getenv("ACCESS_TOKEN", "dev-token")
    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "*")

    def __post_init__(self):
        if self.database_url.startswith("postgres://"):
            object.__setattr__(self, "database_url", self.database_url.replace("postgres://", "postgresql://", 1))


settings = Settings()
