from __future__ import annotations

from functools import wraps
from typing import Callable

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .config import settings
from .models import User


def get_current_user(db: Session, authorization: str | None) -> User:
    token = (authorization or "").removeprefix("Bearer ").strip()
    if token != settings.access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未授权")
    user = db.query(User).filter(User.username == "admin").first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="账号不可用")
    return user


def require_roles(*roles: str):
    def decorator(handler: Callable):
        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        return wrapper

    return decorator
