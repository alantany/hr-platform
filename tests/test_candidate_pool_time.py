"""候选人列表入池时间：recruit 抓取用下载时间，上传/手创用 candidates.created_at。"""
from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.main import app
from tests.auth_helpers import login_headers


client = TestClient(app)


def test_candidate_list_exposes_created_at_as_pool_time():
    headers = login_headers(client, "admin")
    suffix = uuid4().hex[:8]
    created = client.post(
        "/api/candidates",
        json={"name": f"入池时间候选人-{suffix}", "phone": f"139{suffix[:8]}", "city": "长春", "source": "手工导入"},
        headers=headers,
    ).json()
    assert created.get("id")

    items = client.get("/api/candidates", headers=headers).json()
    row = next(item for item in items if item["id"] == created["id"])
    assert row.get("created_at"), "上传/手创候选人应有 created_at 作为入池时间"
    assert "expected_salary" in row  # 字段仍保留，仅列表列不再展示
