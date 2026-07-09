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

# DeepSeek 官方 API（兼容旧 OPENROUTER_* 环境变量名）
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL") or os.getenv(
    "OPENROUTER_BASE_URL", "https://api.deepseek.com"
)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENROUTER_API_KEY")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL") or os.getenv(
    "OPENROUTER_MODEL", "deepseek-v4-flash"
)
