from __future__ import annotations

from pathlib import Path
from uuid import uuid4
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.database import SessionLocal
from backend.app.main import app
from backend.app.models import User
from backend.app.security import hash_password
from tests.auth_helpers import login_headers

client = TestClient(app)


def test_user_can_change_own_password():
    db = SessionLocal()
    suffix = uuid4().hex[:8]
    username = f"pwd_user_{suffix}"
    old_password = "oldpass1"
    new_password = "newpass2"
    user = None

    try:
        user = User(
            username=username,
            full_name="改密测试用户",
            role="操作员",
            password_hash=hash_password(old_password),
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        headers = login_headers(client, username, old_password)

        wrong = client.post(
            "/api/me/change-password",
            headers=headers,
            json={"current_password": "wrong", "new_password": new_password},
        )
        assert wrong.status_code == 400
        assert "当前密码不正确" in wrong.text

        ok = client.post(
            "/api/me/change-password",
            headers=headers,
            json={"current_password": old_password, "new_password": new_password},
        )
        assert ok.status_code == 200
        assert ok.json()["ok"] is True

        old_login = client.post("/api/auth/login", json={"username": username, "password": old_password})
        assert old_login.status_code == 401

        new_login = client.post("/api/auth/login", json={"username": username, "password": new_password})
        assert new_login.status_code == 200
    finally:
        if user is not None and user.id:
            db_user = db.get(User, user.id)
            if db_user is not None:
                db.delete(db_user)
                db.commit()
        db.close()
