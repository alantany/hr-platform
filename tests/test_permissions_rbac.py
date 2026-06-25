from pathlib import Path
import sys
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def admin_headers():
    token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def user_headers(username: str):
    return {"Authorization": f"Bearer user:{username}"}


def test_non_admin_cannot_manage_permission_system():
    headers = user_headers("operator")

    assert client.get("/api/users", headers=headers).status_code == 403
    assert client.get("/api/roles", headers=headers).status_code == 403
    assert client.get("/api/role-permissions", headers=headers).status_code == 403
    assert client.get("/api/data-permissions", headers=headers).status_code == 403
    assert client.get("/api/audit-logs", headers=headers).status_code == 403


def test_login_uses_real_user_identity_and_logout_is_audited():
    assert client.get("/api/users").status_code == 401

    leader_login = client.post("/api/auth/login", json={"username": "leader", "password": "leader123"})
    operator_login = client.post("/api/auth/login", json={"username": "operator", "password": "operator123"})
    assert leader_login.status_code == 200
    assert operator_login.status_code == 200

    leader_headers = {"Authorization": f"Bearer {leader_login.json()['access_token']}"}
    operator_headers = {"Authorization": f"Bearer {operator_login.json()['access_token']}"}
    assert client.get("/api/me", headers=leader_headers).json()["role"] == "组长"
    assert client.get("/api/me", headers=operator_headers).json()["role"] == "操作员"
    assert client.post("/api/auth/login", json={"username": "operator", "password": "wrong"}).status_code == 401
    assert client.post("/api/auth/logout", headers=operator_headers).json()["ok"] is True

    logs = client.get("/api/audit-logs", headers=admin_headers()).json()
    assert any(log["module"] == "认证登录" and log["action"] == "用户退出" for log in logs)


def test_admin_cannot_demote_current_admin_account():
    headers = admin_headers()
    users = client.get("/api/users", headers=headers).json()
    admin_id = next(item["id"] for item in users if item["username"] == "admin")

    res = client.patch(f"/api/users/{admin_id}", json={"role": "组长"}, headers=headers)

    assert res.status_code == 400
    assert "降权" in res.text


def test_operator_only_sees_candidates_for_authorized_position():
    suffix = uuid4().hex[:8]
    headers = admin_headers()

    users = client.get("/api/users", headers=headers).json()
    operator_id = next(item["id"] for item in users if item["username"] == "operator")

    company = client.post("/api/companies", json={"name": f"权限客户-{suffix}"}, headers=headers).json()
    project = client.post("/api/projects", json={"company_id": company["id"], "name": f"权限项目-{suffix}"}, headers=headers).json()
    position = client.post("/api/positions", json={"project_id": project["id"], "name": f"权限岗位-{suffix}"}, headers=headers).json()
    allowed = client.post("/api/candidates", json={"name": f"授权候选人-{suffix}"}, headers=headers).json()
    blocked = client.post("/api/candidates", json={"name": f"未授权候选人-{suffix}"}, headers=headers).json()

    client.post(
        "/api/recommendations",
        json={"candidate_id": allowed["id"], "position_id": position["id"], "recommender": "admin"},
        headers=headers,
    )
    client.post(
        "/api/data-permissions",
        json={
            "user_id": operator_id,
            "scope_type": "position",
            "scope_id": str(position["id"]),
            "scope_name": position["name"],
            "granted_by": "admin",
            "active": True,
        },
        headers=headers,
    )

    operator_candidates = client.get("/api/candidates", headers=user_headers("operator")).json()
    names = {item["name"] for item in operator_candidates}

    assert allowed["name"] in names
    assert blocked["name"] not in names
    assert client.get(f"/api/candidates/{allowed['id']}", headers=user_headers("operator")).status_code == 200
    assert client.get(f"/api/candidates/{blocked['id']}", headers=user_headers("operator")).status_code == 403


def test_data_scope_applies_to_recommendation_export_notification_analytics_and_ai():
    suffix = uuid4().hex[:8]
    headers = admin_headers()
    operator_headers = user_headers("operator")

    users = client.get("/api/users", headers=headers).json()
    operator_id = next(item["id"] for item in users if item["username"] == "operator")

    company = client.post("/api/companies", json={"name": f"横切权限客户-{suffix}"}, headers=headers).json()
    project = client.post("/api/projects", json={"company_id": company["id"], "name": f"横切权限项目-{suffix}"}, headers=headers).json()
    position = client.post("/api/positions", json={"project_id": project["id"], "name": f"横切权限岗位-{suffix}"}, headers=headers).json()
    candidate = client.post("/api/candidates", json={"name": f"横切权限候选人-{suffix}"}, headers=headers).json()
    recommendation = client.post(
        "/api/recommendations",
        json={"candidate_id": candidate["id"], "position_id": position["id"], "recommender": "admin"},
        headers=headers,
    ).json()
    delivery = client.post("/api/deliveries", json={"recommendation_id": recommendation["id"], "delivered_by": "admin"}, headers=headers).json()
    export_record = client.post(
        "/api/export-records",
        json={
            "candidate_id": candidate["id"],
            "candidate_name": candidate["name"],
            "company_name": company["name"],
            "project_name": project["name"],
            "position_name": position["name"],
            "format": "PDF",
            "watermarked": True,
            "exported_by": "admin",
        },
        headers=headers,
    ).json()
    client.post(
        "/api/notifications",
        json={"user": "operator", "title": f"操作员通知-{suffix}", "type": "权限测试", "content": "仅操作员可见"},
        headers=headers,
    )
    client.post(
        "/api/notifications",
        json={"user": "admin", "title": f"管理员通知-{suffix}", "type": "权限测试", "content": "仅管理员可见"},
        headers=headers,
    )
    admin_ai = client.post("/api/ai/tasks", json={"task_type": "resume_parse", "input_text": f"admin-{suffix}"}, headers=headers).json()
    operator_ai = client.post("/api/ai/tasks", json={"task_type": "resume_parse", "input_text": f"operator-{suffix}"}, headers=operator_headers).json()

    assert recommendation["id"] not in {item["id"] for item in client.get("/api/recommendations", headers=operator_headers).json()}
    assert delivery["id"] not in {item["id"] for item in client.get("/api/deliveries", headers=operator_headers).json()}
    assert export_record["id"] not in {item["id"] for item in client.get("/api/export-records", headers=operator_headers).json()}

    client.post(
        "/api/data-permissions",
        json={
            "user_id": operator_id,
            "scope_type": "position",
            "scope_id": str(position["id"]),
            "scope_name": position["name"],
            "granted_by": "admin",
            "active": True,
        },
        headers=headers,
    )

    assert recommendation["id"] in {item["id"] for item in client.get("/api/recommendations", headers=operator_headers).json()}
    assert delivery["id"] in {item["id"] for item in client.get("/api/deliveries", headers=operator_headers).json()}
    assert export_record["id"] in {item["id"] for item in client.get("/api/export-records", headers=operator_headers).json()}
    analytics = client.get("/api/analytics/summary", headers=operator_headers).json()
    assert analytics["candidate_count"] >= 1
    assert analytics["recommendation_count"] >= 1

    notifications = client.get("/api/notifications", headers=operator_headers).json()
    titles = {item["title"] for item in notifications}
    assert f"操作员通知-{suffix}" in titles
    assert f"管理员通知-{suffix}" not in titles

    ai_tasks = client.get("/api/ai/tasks", headers=operator_headers).json()
    ai_inputs = {item["input_text"] for item in ai_tasks}
    assert operator_ai["input_text"] in ai_inputs
    assert admin_ai["input_text"] not in ai_inputs


def test_candidate_ownership_transfer_requires_admin_approval():
    suffix = uuid4().hex[:8]
    headers = admin_headers()

    users = client.get("/api/users", headers=headers).json()
    operator_id = next(item["id"] for item in users if item["username"] == "operator")
    candidate = client.post("/api/candidates", json={"name": f"转派候选人-{suffix}", "owner_user_id": 1}, headers=headers).json()

    transfer = client.post(
        "/api/candidate-ownership-transfers",
        json={"candidate_id": candidate["id"], "to_user_id": operator_id, "reason": "岗位重新分配"},
        headers=headers,
    ).json()
    assert transfer["status"] == "待审批"

    assert client.post(
        f"/api/candidate-ownership-transfers/{transfer['id']}/approve",
        json={},
        headers=user_headers("operator"),
    ).status_code == 403

    approved = client.post(
        f"/api/candidate-ownership-transfers/{transfer['id']}/approve",
        json={},
        headers=headers,
    ).json()
    updated_candidate = client.get(f"/api/candidates/{candidate['id']}", headers=headers).json()

    assert approved["status"] == "已审批"
    assert updated_candidate["owner_user_id"] == operator_id
    assert updated_candidate["locked"] is True
