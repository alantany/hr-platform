"""搜索热词：标签字典热词管理 + 简历池启用列表。"""
from pathlib import Path
import sys
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.main import app


def auth_headers(client: TestClient):
    token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_search_hotwords_crud_and_enabled_only():
    with TestClient(app) as client:
        headers = auth_headers(client)
        suffix = uuid4().hex[:6]
        keyword = f"热词{suffix}"

        created = client.post(
            "/api/search-hotwords",
            json={"keyword": keyword, "sort_order": 5, "enabled": True},
            headers=headers,
        )
        assert created.status_code == 200, created.text
        item = created.json()
        assert item["keyword"] == keyword
        assert item["enabled"] is True

        listed = client.get("/api/search-hotwords", headers=headers)
        assert listed.status_code == 200
        assert any(row["id"] == item["id"] for row in listed.json())

        enabled = client.get("/api/search-hotwords?enabled_only=true", headers=headers)
        assert enabled.status_code == 200
        assert any(row["id"] == item["id"] for row in enabled.json())

        disabled = client.patch(
            f"/api/search-hotwords/{item['id']}",
            json={"enabled": False},
            headers=headers,
        )
        assert disabled.status_code == 200
        assert disabled.json()["enabled"] is False

        enabled_after = client.get("/api/search-hotwords?enabled_only=true", headers=headers)
        assert all(row["id"] != item["id"] for row in enabled_after.json())

        deleted = client.delete(f"/api/search-hotwords/{item['id']}", headers=headers)
        assert deleted.status_code == 200
