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
