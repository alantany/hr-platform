from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def auth_headers():
    token = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_company_and_project_values_are_derived_from_projects_and_positions():
    suffix = uuid4().hex[:8]
    headers = auth_headers()

    company = client.post(
        "/api/companies",
        json={"name": f"聚合规则客户-{suffix}"},
        headers=headers,
    ).json()
    assert company["status"] == "未招聘"
    assert company["project_count"] == 0
    assert company["position_count"] == 0

    project = client.post(
        "/api/projects",
        json={
            "company_id": company["id"],
            "name": f"聚合规则项目-{suffix}",
            "status": "招聘中",
            "level": "高",
        },
        headers=headers,
    ).json()
    assert project["level"] == "高"
    assert project["hiring_count"] == 0
    assert project["position_count"] == 0

    first_position = client.post(
        "/api/positions",
        json={
            "project_id": project["id"],
            "name": f"聚合岗位一-{suffix}",
            "urgency": "高",
            "hiring_count": 2,
            "status": "已关闭",
        },
        headers=headers,
    ).json()
    second_position = client.post(
        "/api/positions",
        json={
            "project_id": project["id"],
            "name": f"聚合岗位二-{suffix}",
            "urgency": "低",
            "hiring_count": 3,
        },
        headers=headers,
    ).json()
    assert "status" not in first_position
    assert "status" not in second_position

    project = next(
        item
        for item in client.get("/api/projects", headers=headers).json()
        if item["id"] == project["id"]
    )
    company = next(
        item
        for item in client.get("/api/companies", headers=headers).json()
        if item["id"] == company["id"]
    )
    assert project["hiring_count"] == 5
    assert project["position_count"] == 2
    assert company["project_count"] == 1
    assert company["position_count"] == 2
    assert company["status"] == "招聘中"

    client.patch(
        f"/api/projects/{project['id']}",
        json={"status": "招聘完毕", "level": "中"},
        headers=headers,
    )
    company = next(
        item
        for item in client.get("/api/companies", headers=headers).json()
        if item["id"] == company["id"]
    )
    assert company["status"] == "未招聘"
