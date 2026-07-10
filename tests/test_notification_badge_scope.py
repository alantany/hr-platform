"""铃铛未读数应只统计当前用户自己的未读通知。"""
from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.main import app
from tests.auth_helpers import login_headers


client = TestClient(app)


def headers(username: str, password: str | None = None) -> dict[str, str]:
    return login_headers(client, username, password)


def test_admin_unread_notifications_only_include_own_messages():
    """管理员铃铛未读数不应把其他用户的未读算进去。"""
    suffix = uuid4().hex[:8]
    admin_headers = headers("admin")

    mine = client.post(
        "/api/notifications",
        json={
            "user": "admin",
            "title": f"管理员自己的未读-{suffix}",
            "type": "铃铛测试",
            "target_path": "./notifications.html",
        },
        headers=admin_headers,
    ).json()
    others = client.post(
        "/api/notifications",
        json={
            "user": "operator",
            "title": f"操作员未读-{suffix}",
            "type": "铃铛测试",
            "target_path": "./notifications.html",
        },
        headers=admin_headers,
    ).json()

    unread = client.get("/api/notifications?read=false", headers=admin_headers).json()
    titles = {item["title"] for item in unread}

    assert f"管理员自己的未读-{suffix}" in titles
    assert f"操作员未读-{suffix}" not in titles
    assert all(item["user"] in {"admin", "系统管理员"} for item in unread if suffix in item["title"])

    # 已读自己的通知后，铃铛口径的未读里不应再出现该条
    read_back = client.post(f"/api/notifications/{mine['id']}/read", headers=admin_headers).json()
    assert read_back["read"] is True
    unread_after = client.get("/api/notifications?read=false", headers=admin_headers).json()
    assert mine["id"] not in {item["id"] for item in unread_after}
    # 他人未读仍存在于库中，但不应出现在管理员未读列表
    assert others["id"] not in {item["id"] for item in unread_after}


def test_marking_own_notification_read_decreases_personal_unread_count():
    suffix = uuid4().hex[:8]
    admin_headers = headers("admin")
    # 先塞一条别人的未读，模拟「全站未读很多」的干扰
    client.post(
        "/api/notifications",
        json={"user": "operator", "title": f"干扰未读-{suffix}", "type": "铃铛测试"},
        headers=admin_headers,
    )
    mine = client.post(
        "/api/notifications",
        json={"user": "admin", "title": f"待确认未读-{suffix}", "type": "铃铛测试"},
        headers=admin_headers,
    ).json()

    before = client.get("/api/notifications?read=false", headers=admin_headers).json()
    before_ids = {item["id"] for item in before}
    assert mine["id"] in before_ids

    client.post(f"/api/notifications/{mine['id']}/read", headers=admin_headers)
    after = client.get("/api/notifications?read=false", headers=admin_headers).json()
    after_ids = {item["id"] for item in after}

    assert mine["id"] not in after_ids
    assert len(after_ids) == len(before_ids) - 1
