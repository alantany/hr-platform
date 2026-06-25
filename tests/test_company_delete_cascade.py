from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def auth_headers():
    token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_delete_company_removes_descendant_records():
    suffix = uuid4().hex[:8]
    headers = auth_headers()

    company = client.post(
        "/api/companies",
        json={"name": f"删除级联客户-{suffix}", "contact_name": "负责人", "contact_phone": "13800002222"},
        headers=headers,
    ).json()
    project = client.post(
        "/api/projects",
        json={"company_id": company["id"], "name": f"删除级联项目-{suffix}", "work_location": "深圳"},
        headers=headers,
    ).json()
    position = client.post(
        "/api/positions",
        json={"project_id": project["id"], "name": f"删除级联岗位-{suffix}", "urgency": "高"},
        headers=headers,
    ).json()
    candidate = client.post(
        "/api/candidates",
        json={"name": f"删除级联合同候选人-{suffix}", "phone": f"138{suffix[:8]}", "city": "深圳"},
        headers=headers,
    ).json()
    recommendation = client.post(
        "/api/recommendations",
        json={"candidate_id": candidate["id"], "position_id": position["id"], "recommender": "admin"},
        headers=headers,
    ).json()
    tracking_event = client.post(
        "/api/candidate-tracking-events",
        json={
            "candidate_id": candidate["id"],
            "event_type": "面试",
            "status": "已完成",
            "summary": "删除级联测试",
            "position_id": position["id"],
            "recommendation_id": recommendation["id"],
            "interview_round": "初筛",
            "screening_result": "通过",
            "interview_date": "2026-06-24",
            "interviewer": "测试官",
            "interview_location": "线上",
            "interview_requirements": "无",
            "interview_contact": "13800000000",
            "interview_result": "-",
            "note": "用于验证删除级联",
            "employment_status": "待设置",
            "operator": "admin",
        },
        headers=headers,
    ).json()
    feedback = client.post(
        "/api/recommendation-feedbacks",
        json={
            "recommendation_id": recommendation["id"],
            "status": "客户已收",
            "feedback": "已收到",
            "customer_comment": "等待后续",
            "operator": "admin",
        },
        headers=headers,
    ).json()
    delivery = client.post(
        "/api/deliveries",
        json={"recommendation_id": recommendation["id"], "delivered_by": "admin"},
        headers=headers,
    ).json()

    delete_resp = client.delete(f"/api/companies/{company['id']}", headers=headers)
    assert delete_resp.status_code == 200
    assert delete_resp.json() == {"ok": True}

    assert all(item["id"] != company["id"] for item in client.get("/api/companies", headers=headers).json())
    assert client.get(f"/api/projects?company_id={company['id']}", headers=headers).json() == []
    assert client.get(f"/api/positions?project_id={project['id']}", headers=headers).json() == []
    assert client.get(f"/api/recommendations?position_id={position['id']}", headers=headers).json() == []
    assert client.get(f"/api/recommendation-feedbacks?recommendation_id={recommendation['id']}", headers=headers).json() == []
    assert client.get(f"/api/deliveries?recommendation_id={recommendation['id']}", headers=headers).json() == []
    assert client.get(f"/api/candidate-tracking-events?candidate_id={candidate['id']}", headers=headers).json() == []

    # 这些对象本身用于制造级联链路，保留变量避免静态分析误判为未使用。
    assert tracking_event["id"] > 0
    assert feedback["id"] > 0
    assert delivery["id"] > 0
