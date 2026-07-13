from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def auth_headers() -> dict[str, str]:
    token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_dashboard_candidate_count_matches_resume_pool_list() -> None:
    """首页求职者总数以简历池列表为准，两端数量一致。"""
    headers = auth_headers()
    summary = client.get("/api/dashboard/summary", headers=headers).json()
    items = client.get("/api/candidates", headers=headers).json()
    assert summary["candidate_count"] == len(items)
