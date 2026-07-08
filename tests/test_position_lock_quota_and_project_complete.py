from __future__ import annotations

from pathlib import Path
from uuid import uuid4
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def auth_headers():
    token = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_position_lock_quota_is_limited_to_ten_and_release_allows_readd():
    suffix = uuid4().hex[:8]
    headers = auth_headers()
    company = client.post("/api/companies", headers=headers, json={"name": f"锁定上限客户-{suffix}"}).json()
    project = client.post(
        "/api/projects",
        headers=headers,
        json={"company_id": company["id"], "name": f"锁定上限项目-{suffix}", "status": "招聘中", "level": "中"},
    ).json()
    position = client.post(
        "/api/positions",
        headers=headers,
        json={
            "project_id": project["id"],
            "name": f"锁定上限岗位-{suffix}",
            "hiring_count": 2,
            "target_resume_count": 99,
            "requirement_tags": {"keyword": "Java"},
        },
    ).json()
    assert position["target_resume_count"] == 10

    for idx in range(10):
        candidate = client.post(
            "/api/candidates",
            headers=headers,
            json={"name": f"锁定候选人{idx}-{suffix}", "phone": f"138{suffix[:4]}{idx:04d}", "status": "未锁定"},
        ).json()
        rec = client.post(
            "/api/recommendations",
            headers=headers,
            json={"candidate_id": candidate["id"], "position_id": position["id"], "status": "待推荐"},
        )
        assert rec.status_code == 200, rec.text

    overflow = client.post(
        "/api/candidates",
        headers=headers,
        json={"name": f"溢出候选人-{suffix}", "phone": f"139{suffix}", "status": "未锁定"},
    ).json()
    blocked = client.post(
        "/api/recommendations",
        headers=headers,
        json={"candidate_id": overflow["id"], "position_id": position["id"], "status": "待推荐"},
    )
    assert blocked.status_code == 400
    assert "锁定名额已满" in blocked.json()["detail"]

    existing = client.get(f"/api/recommendations?position_id={position['id']}", headers=headers).json()
    assert len(existing) == 10
    deleted = client.delete(f"/api/recommendations/{existing[0]['id']}", headers=headers)
    assert deleted.status_code == 200, deleted.text
    readd = client.post(
        "/api/recommendations",
        headers=headers,
        json={"candidate_id": overflow["id"], "position_id": position["id"], "status": "待推荐"},
    )
    assert readd.status_code == 200, readd.text


def test_project_completes_when_every_position_is_filled():
    suffix = uuid4().hex[:8]
    headers = auth_headers()
    company = client.post("/api/companies", headers=headers, json={"name": f"项目完成客户-{suffix}"}).json()
    project = client.post(
        "/api/projects",
        headers=headers,
        json={"company_id": company["id"], "name": f"项目完成项目-{suffix}", "status": "招聘中", "level": "中"},
    ).json()
    pos_a = client.post(
        "/api/positions",
        headers=headers,
        json={"project_id": project["id"], "name": f"岗位A-{suffix}", "hiring_count": 1},
    ).json()
    pos_b = client.post(
        "/api/positions",
        headers=headers,
        json={"project_id": project["id"], "name": f"岗位B-{suffix}", "hiring_count": 1},
    ).json()

    cand_a = client.post(
        "/api/candidates",
        headers=headers,
        json={"name": f"完成A-{suffix}", "phone": f"137{suffix}1", "status": "未锁定"},
    ).json()
    cand_b = client.post(
        "/api/candidates",
        headers=headers,
        json={"name": f"完成B-{suffix}", "phone": f"137{suffix}2", "status": "未锁定"},
    ).json()
    assert client.post(
        "/api/recommendations",
        headers=headers,
        json={"candidate_id": cand_a["id"], "position_id": pos_a["id"]},
    ).status_code == 200
    assert client.post(
        "/api/recommendations",
        headers=headers,
        json={"candidate_id": cand_b["id"], "position_id": pos_b["id"]},
    ).status_code == 200

    emp_a = client.post(
        "/api/employment-records",
        headers=headers,
        json={
            "candidate_id": cand_a["id"],
            "status": "已入职",
            "company_name": company["name"],
            "position_name": pos_a["name"],
        },
    )
    assert emp_a.status_code == 200, emp_a.text
    mid = client.get("/api/projects", headers=headers).json()
    target = next(item for item in mid if item["id"] == project["id"])
    assert target["status"] == "招聘中"

    emp_b = client.post(
        "/api/employment-records",
        headers=headers,
        json={
            "candidate_id": cand_b["id"],
            "status": "已入职",
            "company_name": company["name"],
            "position_name": pos_b["name"],
        },
    )
    assert emp_b.status_code == 200, emp_b.text
    done = client.get("/api/projects", headers=headers).json()
    target = next(item for item in done if item["id"] == project["id"])
    assert target["status"] == "招聘完毕"


def test_candidates_expose_has_interview_round_for_never_interviewed_filter():
    suffix = uuid4().hex[:8]
    headers = auth_headers()
    candidate = client.post(
        "/api/candidates",
        headers=headers,
        json={"name": f"未面试候选人-{suffix}", "phone": f"136{suffix}", "status": "未锁定"},
    ).json()
    listed = client.get("/api/candidates", headers=headers).json()
    row = next(
        item
        for item in listed
        if str(item.get("id")) == str(candidate["id"])
        or str(item.get("record_key")) == f"candidate:{candidate['id']}"
    )
    assert row.get("has_interview_round") is False
