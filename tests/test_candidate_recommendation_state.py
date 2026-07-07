from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def auth_headers() -> dict[str, str]:
    token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_flow(headers: dict[str, str]) -> tuple[dict, dict]:
    suffix = uuid4().hex[:8]
    company = client.post("/api/companies", json={"name": f"状态联动客户-{suffix}"}, headers=headers).json()
    project = client.post(
        "/api/projects",
        json={"company_id": company["id"], "name": f"状态联动项目-{suffix}"},
        headers=headers,
    ).json()
    position = client.post(
        "/api/positions",
        json={"project_id": project["id"], "name": f"状态联动岗位-{suffix}"},
        headers=headers,
    ).json()
    candidate = client.post(
        "/api/candidates",
        json={"name": f"状态联动候选人-{suffix}"},
        headers=headers,
    ).json()
    return candidate, position


def candidate_state(headers: dict[str, str], candidate_id: int) -> tuple[bool, str, str]:
    item = client.get(f"/api/candidates/{candidate_id}", headers=headers).json()
    return item["locked"], item["status"], item["delivery_status"]


def test_recommendation_drives_candidate_lock_and_failure_releases() -> None:
    headers = auth_headers()
    candidate, position = create_flow(headers)
    assert candidate_state(headers, candidate["id"]) == (False, "未锁定", "未推荐")

    recommendation = client.post(
        "/api/recommendations",
        json={"candidate_id": candidate["id"], "position_id": position["id"], "recommender": "admin"},
        headers=headers,
    ).json()
    # Initial status is now 待推荐; must be promoted manually
    assert candidate_state(headers, candidate["id"]) == (True, "锁定", "待推荐")

    # Promote to 已推荐 manually
    client.put(f"/api/recommendations/{recommendation['id']}", json={"status": "已推荐"}, headers=headers)
    assert candidate_state(headers, candidate["id"]) == (True, "锁定", "已推荐")

    client.put(f"/api/recommendations/{recommendation['id']}", json={"status": "面试中"}, headers=headers)
    assert candidate_state(headers, candidate["id"]) == (True, "锁定", "面试中")

    terminal = client.put(
        f"/api/recommendations/{recommendation['id']}",
        json={"status": "未录用"},
        headers=headers,
    )
    assert terminal.status_code == 200
    assert candidate_state(headers, candidate["id"]) == (True, "锁定", "未录用")
    history = client.get(f"/api/recommendations?candidate_id={candidate['id']}", headers=headers).json()
    assert history[0]["status"] == "未录用"


def test_onboard_state_only_comes_from_employment_action() -> None:
    headers = auth_headers()
    candidate, position = create_flow(headers)
    recommendation = client.post(
        "/api/recommendations",
        json={"candidate_id": candidate["id"], "position_id": position["id"], "recommender": "admin"},
        headers=headers,
    ).json()
    # Promote through states manually: 待推荐 -> 已推荐 -> 面试中
    client.put(f"/api/recommendations/{recommendation['id']}", json={"status": "已推荐"}, headers=headers)
    client.put(f"/api/recommendations/{recommendation['id']}", json={"status": "面试中"}, headers=headers)
    legacy_hired = client.put(f"/api/recommendations/{recommendation['id']}", json={"status": "已录用"}, headers=headers)
    assert legacy_hired.status_code == 400
    assert candidate_state(headers, candidate["id"]) == (True, "锁定", "面试中")
    assert client.get(f"/api/employment-records?candidate_id={candidate['id']}", headers=headers).json() == []

    onboard = client.post(
        "/api/employment-records",
        json={
            "candidate_id": candidate["id"],
            "status": "已入职",
            "company_name": "状态联动客户",
            "position_name": "状态联动岗位",
        },
        headers=headers,
    )
    assert onboard.status_code == 200
    assert candidate_state(headers, candidate["id"]) == (True, "锁定", "已入职")
    onboard_candidate = client.get(f"/api/candidates/{candidate['id']}", headers=headers).json()
    assert onboard_candidate["candidate_warranty_status"] == "质保中"

    deleted = client.delete(f"/api/recommendations/{recommendation['id']}", headers=headers)
    assert deleted.status_code == 409
    assert candidate_state(headers, candidate["id"]) == (True, "锁定", "已入职")


def test_manual_lock_fields_and_endpoints_are_rejected() -> None:
    headers = auth_headers()
    candidate, _ = create_flow(headers)
    assert client.patch(
        f"/api/candidates/{candidate['id']}", json={"status": "锁定"}, headers=headers
    ).status_code == 400
    assert client.post(f"/api/candidates/{candidate['id']}/lock", headers=headers).status_code == 409
    assert client.post(f"/api/candidates/{candidate['id']}/release", headers=headers).status_code == 409
    assert candidate_state(headers, candidate["id"]) == (False, "未锁定", "未推荐")
