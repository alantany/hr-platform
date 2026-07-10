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


def get_deepseek_config() -> tuple[str, str | None, str]:
    """每次调用重新读取 .env，避免改 Key 后 uvicorn 热重载仍用旧值。"""
    load_dotenv(BASE_DIR / ".env", override=True)
    base_url = os.getenv("DEEPSEEK_BASE_URL") or os.getenv(
        "OPENROUTER_BASE_URL", "https://api.deepseek.com"
    )
    api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("DEEPSEEK_MODEL") or os.getenv(
        "OPENROUTER_MODEL", "deepseek-v4-flash"
    )
    return base_url, api_key, model


# 兼容旧 import：启动时快照；LLM 调用请优先用 get_deepseek_config()
DEEPSEEK_BASE_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL = get_deepseek_config()
