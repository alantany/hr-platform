from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = "hr-platform"
    api_prefix: str = "/api"
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user_delivery:delivery_pass@localhost:5432/hr_platform",
    )
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key")
    access_token: str = os.getenv("ACCESS_TOKEN", "dev-token")
    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "*")


settings = Settings()
