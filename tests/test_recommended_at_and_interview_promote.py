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
    company = client.post("/api/companies", json={"name": f"推荐口径客户-{suffix}"}, headers=headers).json()
    project = client.post(
        "/api/projects",
        json={"company_id": company["id"], "name": f"推荐口径项目-{suffix}"},
        headers=headers,
    ).json()
    position = client.post(
        "/api/positions",
        json={"project_id": project["id"], "name": f"推荐口径岗位-{suffix}"},
        headers=headers,
    ).json()
    candidate = client.post(
        "/api/candidates",
        json={"name": f"推荐口径候选人-{suffix}"},
        headers=headers,
    ).json()
    return candidate, position


def test_pending_recommendation_not_counted_until_recommended() -> None:
    headers = auth_headers()
    before = client.get("/api/dashboard/summary", headers=headers).json()["recommendation_count"]
    candidate, position = create_flow(headers)

    recommendation = client.post(
        "/api/recommendations",
        json={"candidate_id": candidate["id"], "position_id": position["id"], "recommender": "admin"},
        headers=headers,
    ).json()
    assert recommendation["status"] == "待推荐"
    assert recommendation.get("recommended_at") in (None, "")

    after_create = client.get("/api/dashboard/summary", headers=headers).json()["recommendation_count"]
    assert after_create == before

    promoted = client.put(
        f"/api/recommendations/{recommendation['id']}",
        json={"status": "已推荐"},
        headers=headers,
    ).json()
    assert promoted["status"] == "已推荐"
    assert promoted.get("recommended_at")

    after_promote = client.get("/api/dashboard/summary", headers=headers).json()["recommendation_count"]
    assert after_promote == before + 1


def test_interview_round_auto_promotes_pending_to_recommended() -> None:
    headers = auth_headers()
    candidate, position = create_flow(headers)
    recommendation = client.post(
        "/api/recommendations",
        json={"candidate_id": candidate["id"], "position_id": position["id"], "recommender": "admin"},
        headers=headers,
    ).json()
    assert recommendation["status"] == "待推荐"

    tracking = client.post(
        "/api/candidate-tracking-events",
        json={
            "candidate_id": candidate["id"],
            "event_type": "面试跟踪",
            "interview_round": "第1轮",
            "interview_date": "2026-07-12",
            "position_id": position["id"],
            "recommendation_id": recommendation["id"],
        },
        headers=headers,
    )
    assert tracking.status_code == 200

    updated = client.get(f"/api/recommendations?candidate_id={candidate['id']}", headers=headers).json()[0]
    assert updated["status"] == "已推荐"
    assert updated.get("recommended_at")


def test_screening_does_not_auto_promote() -> None:
    headers = auth_headers()
    candidate, position = create_flow(headers)
    recommendation = client.post(
        "/api/recommendations",
        json={"candidate_id": candidate["id"], "position_id": position["id"], "recommender": "admin"},
        headers=headers,
    ).json()

    tracking = client.post(
        "/api/candidate-tracking-events",
        json={
            "candidate_id": candidate["id"],
            "event_type": "面试跟踪",
            "interview_round": "初筛",
            "screening_result": "通过",
            "position_id": position["id"],
            "recommendation_id": recommendation["id"],
        },
        headers=headers,
    )
    assert tracking.status_code == 200

    updated = client.get(f"/api/recommendations?candidate_id={candidate['id']}", headers=headers).json()[0]
    assert updated["status"] == "待推荐"
    assert updated.get("recommended_at") in (None, "")
