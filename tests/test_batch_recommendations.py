from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi import HTTPException
from fastapi.testclient import TestClient

from backend.app import crud
from backend.app import main as main_module
from backend.app.main import app


client = TestClient(app)


def auth_headers():
    token = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_position(headers: dict[str, str], suffix: str) -> dict:
    company = client.post(
        "/api/companies",
        json={"name": f"批量推荐客户-{suffix}"},
        headers=headers,
    ).json()
    project = client.post(
        "/api/projects",
        json={"company_id": company["id"], "name": f"批量推荐项目-{suffix}"},
        headers=headers,
    ).json()
    return client.post(
        "/api/positions",
        json={"project_id": project["id"], "name": f"批量推荐岗位-{suffix}"},
        headers=headers,
    ).json()


def create_candidate(headers: dict[str, str], suffix: str, label: str) -> dict:
    return client.post(
        "/api/candidates",
        json={"name": f"{label}-{suffix}", "source": "手工导入"},
        headers=headers,
    ).json()


def test_batch_recommendations_continue_and_summarize():
    suffix = uuid4().hex[:8]
    headers = auth_headers()
    position = create_position(headers, suffix)
    other_position = create_position(headers, suffix + "-other")
    first = create_candidate(headers, suffix, "成功候选人一")
    second = create_candidate(headers, suffix, "成功候选人二")
    locked = create_candidate(headers, suffix, "锁定候选人")
    duplicate = create_candidate(headers, suffix, "重复候选人")

    locked_recommendation = client.post(
        "/api/recommendations",
        json={"candidate_id": locked["id"], "position_id": other_position["id"], "recommender": "admin"},
        headers=headers,
    )
    assert locked_recommendation.status_code == 200
    existing = client.post(
        "/api/recommendations",
        json={"candidate_id": duplicate["id"], "position_id": position["id"], "recommender": "admin"},
        headers=headers,
    )
    assert existing.status_code == 200

    notifications_before = client.get("/api/notifications", headers=headers).json()
    response = client.post(
        "/api/recommendations/batch",
        json={
            "record_keys": [
                f"candidate:{first['id']}",
                f"candidate:{second['id']}",
                f"candidate:{locked['id']}",
                f"candidate:{duplicate['id']}",
                "candidate:999999999",
            ],
            "position_id": position["id"],
            "recommender": "admin",
            "status": "待推荐",
            "feedback": "统一推荐理由",
        },
        headers=headers,
    )

    assert response.status_code == 200
    result = response.json()
    assert result["total"] == 5
    assert result["succeeded"] == 2
    assert result["skipped"] == 2
    assert result["failed"] == 1
    assert [item["result"] for item in result["items"]] == [
        "success",
        "success",
        "skipped",
        "skipped",
        "failed",
    ]
    assert "锁定" in result["items"][2]["reason"]
    assert "已推荐" in result["items"][3]["reason"]
    assert "不存在" in result["items"][4]["reason"]

    recommendations = client.get(
        f"/api/recommendations?position_id={position['id']}",
        headers=headers,
    ).json()
    assert {item["candidate_id"] for item in recommendations} == {
        first["id"],
        second["id"],
        duplicate["id"],
    }
    assert all(item["feedback"] == "统一推荐理由" for item in recommendations if item["candidate_id"] != duplicate["id"])
    assert client.get(f"/api/candidates/{first['id']}", headers=headers).json()["locked"] is True
    assert client.get(f"/api/candidates/{first['id']}", headers=headers).json()["status"] == "锁定"
    assert client.get(f"/api/candidates/{second['id']}", headers=headers).json()["locked"] is True
    assert client.get(f"/api/candidates/{duplicate['id']}", headers=headers).json()["locked"] is True

    notifications_after = client.get("/api/notifications", headers=headers).json()
    new_notifications = [
        item for item in notifications_after
        if item["id"] not in {existing["id"] for existing in notifications_before}
    ]
    assert len(new_notifications) == 1
    assert new_notifications[0]["title"] == "批量推荐完成：2 人"


def test_batch_recommendations_pass_record_keys_to_candidate_resolution(monkeypatch):
    suffix = uuid4().hex[:8]
    headers = auth_headers()
    position = create_position(headers, suffix)
    candidate = create_candidate(headers, suffix, "外部候选人")
    original = crud.ensure_local_candidate
    seen_keys: list[str] = []

    def resolve_candidate(db, candidate_key):
        seen_keys.append(str(candidate_key))
        if str(candidate_key) == "download:987654321":
            return original(db, f"candidate:{candidate['id']}")
        return original(db, candidate_key)

    monkeypatch.setattr(crud, "ensure_local_candidate", resolve_candidate)
    response = client.post(
        "/api/recommendations/batch",
        json={
            "record_keys": ["download:987654321"],
            "position_id": position["id"],
            "recommender": "admin",
        },
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["succeeded"] == 1
    assert seen_keys == ["download:987654321"]
    locked_candidate = client.get(f"/api/candidates/{candidate['id']}", headers=headers).json()
    assert locked_candidate["locked"] is True
    assert locked_candidate["status"] == "锁定"


def test_batch_recommendations_reject_inaccessible_position(monkeypatch):
    suffix = uuid4().hex[:8]
    headers = auth_headers()
    position = create_position(headers, suffix)
    candidate = create_candidate(headers, suffix, "权限候选人")

    def deny_position_access(db, user, position_id):
        raise HTTPException(status_code=403, detail="无权访问该岗位")

    monkeypatch.setattr(main_module, "enforce_position_access", deny_position_access)
    response = client.post(
        "/api/recommendations/batch",
        json={
            "record_keys": [f"candidate:{candidate['id']}"],
            "position_id": position["id"],
            "recommender": "admin",
        },
        headers=headers,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "无权访问该岗位"
    assert client.get(
        f"/api/recommendations?position_id={position['id']}",
        headers=headers,
    ).json() == []
