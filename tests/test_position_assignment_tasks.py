from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.main import app
from tests.auth_helpers import login_headers


client = TestClient(app)


def headers(username: str, password: str | None = None) -> dict[str, str]:
    return login_headers(client, username, password)


def test_position_assignment_requires_operator_confirmation_and_notifies_leader():
    suffix = uuid4().hex[:8]
    admin_headers = headers("admin")
    leader_headers = headers("leader")
    leader_id = client.get("/api/me", headers=leader_headers).json()["id"]
    operator_username = f"temp_assignment_{suffix}"
    operator = client.post(
        "/api/users",
        json={
            "username": operator_username,
            "full_name": "岗位确认操作员",
            "password_hash": "operator123",
            "role": "操作员",
            "manager_user_id": leader_id,
        },
        headers=admin_headers,
    ).json()
    operator_headers = headers(operator_username, "operator123")
    company = client.post("/api/companies", json={"name": f"岗位待办客户-{suffix}"}, headers=leader_headers).json()
    project = client.post(
        "/api/projects",
        json={"company_id": company["id"], "name": f"岗位待办项目-{suffix}"},
        headers=leader_headers,
    ).json()
    position = client.post(
        "/api/positions",
        json={"project_id": project["id"], "name": f"岗位待办岗位-{suffix}"},
        headers=leader_headers,
    ).json()

    assigned = client.post(
        f"/api/positions/{position['id']}/assign",
        json={"user_ids": [operator["id"]]},
        headers=leader_headers,
    )
    assert assigned.status_code == 200
    assert assigned.json()["pending_count"] == 1

    permission = next(
        item for item in client.get(f"/api/data-permissions?user_id={operator['id']}", headers=admin_headers).json()
        if item["scope_type"] == "position" and item["scope_id"] == str(position["id"])
    )
    assert permission["active"] is False
    assert len(client.get("/api/dashboard/todos", headers=operator_headers).json()) == 1

    tasks = client.get("/api/position-assignment-tasks", headers=operator_headers).json()
    assert len(tasks) == 1
    assert tasks[0]["status"] == "pending"
    assign_notices_before = client.get("/api/notifications?type=岗位分配&read=false", headers=operator_headers).json()
    assert any(position["name"] in item["title"] for item in assign_notices_before)
    accepted = client.post(
        f"/api/position-assignment-tasks/{tasks[0]['id']}/respond",
        json={"action": "accept"},
        headers=operator_headers,
    )
    assert accepted.status_code == 200
    assert accepted.json()["status"] == "accepted"
    assert client.get("/api/dashboard/todos", headers=operator_headers).json() == []
    assign_notices_after = client.get("/api/notifications?type=岗位分配&read=false", headers=operator_headers).json()
    assert not any(position["name"] in item["title"] for item in assign_notices_after)

    permission = next(
        item for item in client.get(f"/api/data-permissions?user_id={operator['id']}", headers=admin_headers).json()
        if item["scope_type"] == "position" and item["scope_id"] == str(position["id"])
    )
    assert permission["active"] is True
    leader_notices = client.get("/api/notifications?type=岗位分配回执", headers=leader_headers).json()
    assert any("已接受岗位" in item["title"] and position["name"] in item["title"] for item in leader_notices)


def test_rejected_position_assignment_does_not_enable_permission():
    suffix = uuid4().hex[:8]
    admin_headers = headers("admin")
    leader_headers = headers("leader")
    leader_id = client.get("/api/me", headers=leader_headers).json()["id"]
    operator_username = f"temp_assignment_reject_{suffix}"
    operator = client.post(
        "/api/users",
        json={
            "username": operator_username,
            "full_name": "拒绝岗位操作员",
            "password_hash": "operator123",
            "role": "操作员",
            "manager_user_id": leader_id,
        },
        headers=admin_headers,
    ).json()
    company = client.post("/api/companies", json={"name": f"拒绝岗位客户-{suffix}"}, headers=leader_headers).json()
    project = client.post("/api/projects", json={"company_id": company["id"], "name": f"拒绝岗位项目-{suffix}"}, headers=leader_headers).json()
    position = client.post("/api/positions", json={"project_id": project["id"], "name": f"拒绝岗位-{suffix}"}, headers=leader_headers).json()
    client.post(f"/api/positions/{position['id']}/assign", json={"user_ids": [operator["id"]]}, headers=leader_headers)
    operator_headers = headers(operator_username, "operator123")
    task = client.get("/api/position-assignment-tasks", headers=operator_headers).json()[0]
    assert any(
        position["name"] in item["title"]
        for item in client.get("/api/notifications?type=岗位分配&read=false", headers=operator_headers).json()
    )

    rejected = client.post(
        f"/api/position-assignment-tasks/{task['id']}/respond",
        json={"action": "reject", "note": "当前任务已满"},
        headers=operator_headers,
    )
    assert rejected.status_code == 200
    assert rejected.json()["status"] == "rejected"
    assert not any(
        position["name"] in item["title"]
        for item in client.get("/api/notifications?type=岗位分配&read=false", headers=operator_headers).json()
    )
    permission = next(
        item for item in client.get(f"/api/data-permissions?user_id={operator['id']}", headers=admin_headers).json()
        if item["scope_type"] == "position" and item["scope_id"] == str(position["id"])
    )
    assert permission["active"] is False
    leader_notices = client.get("/api/notifications?type=岗位分配回执", headers=leader_headers).json()
    assert any("已拒绝岗位" in item["title"] and "当前任务已满" in item["title"] for item in leader_notices)
