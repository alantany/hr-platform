from pathlib import Path
import sys
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def auth_headers():
    token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_salary_tracking_links_position_and_derives_company():
    suffix = uuid4().hex[:8]
    headers = auth_headers()

    company_a = client.post(
        "/api/companies",
        json={"name": f"薪资联动公司A-{suffix}", "contact_name": "负责人A", "contact_phone": "13800001111"},
        headers=headers,
    ).json()
    project_a = client.post(
        "/api/projects",
        json={"company_id": company_a["id"], "name": f"薪资联动项目A-{suffix}", "work_location": "上海"},
        headers=headers,
    ).json()
    position_a = client.post(
        "/api/positions",
        json={"project_id": project_a["id"], "name": f"薪资联动岗位A-{suffix}", "urgency": "高"},
        headers=headers,
    ).json()

    company_b = client.post(
        "/api/companies",
        json={"name": f"薪资联动公司B-{suffix}", "contact_name": "负责人B", "contact_phone": "13800002222"},
        headers=headers,
    ).json()
    project_b = client.post(
        "/api/projects",
        json={"company_id": company_b["id"], "name": f"薪资联动项目B-{suffix}", "work_location": "北京"},
        headers=headers,
    ).json()
    position_b = client.post(
        "/api/positions",
        json={"project_id": project_b["id"], "name": f"薪资联动岗位B-{suffix}", "urgency": "中"},
        headers=headers,
    ).json()

    candidate = client.post(
        "/api/candidates",
        json={"name": f"薪资测试候选人-{suffix}", "phone": f"1399999{suffix[:4]}", "city": "上海"},
        headers=headers,
    ).json()
    candidate_id = candidate["id"]

    payload_create = {
        "candidate_id": candidate_id,
        "position_id": position_a["id"],
        "interview_round": "第1轮",
        "agreed_salary": "35K/月",
        "welfare_desc": "六险一金，16薪",
        "onboard_cond": "携带离职证明及体检报告",
        "candidate_accepted": "接受",
        "operator": "李四",
    }

    res_create = client.post("/api/salary-records", json=payload_create, headers=headers)
    assert res_create.status_code == 200
    record = res_create.json()
    assert record["id"] is not None
    assert record["position_id"] == position_a["id"]
    assert record["position_name"] == position_a["name"]
    assert record["company_name"] == company_a["name"]
    assert record["agreed_salary"] == "35K/月"
    assert record["candidate_accepted"] == "接受"
    assert record["operator"] == "李四"

    res_list = client.get(f"/api/salary-records?candidate_id={candidate_id}", headers=headers)
    assert res_list.status_code == 200
    records = res_list.json()
    assert len(records) >= 1
    target_rec = [r for r in records if r["id"] == record["id"]][0]
    assert target_rec["position_id"] == position_a["id"]
    assert target_rec["position_name"] == position_a["name"]
    assert target_rec["company_name"] == company_a["name"]

    payload_update = {
        "candidate_id": candidate_id,
        "position_id": position_b["id"],
        "interview_round": "第2轮",
        "agreed_salary": "40K/月",
        "welfare_desc": "六险一金，16薪，全额公积金",
        "onboard_cond": "携带离职证明及体检报告",
        "candidate_accepted": "接受",
        "operator": "李四",
    }

    res_update = client.patch(f"/api/salary-records/{record['id']}", json=payload_update, headers=headers)
    assert res_update.status_code == 200
    updated_record = res_update.json()
    assert updated_record["position_id"] == position_b["id"]
    assert updated_record["position_name"] == position_b["name"]
    assert updated_record["company_name"] == company_b["name"]
    assert updated_record["agreed_salary"] == "40K/月"
    assert updated_record["interview_round"] == "第1轮"

    res_list_after = client.get(f"/api/salary-records?candidate_id={candidate_id}", headers=headers).json()
    assert len(res_list_after) == 1
    assert res_list_after[0]["position_id"] == position_b["id"]
    assert res_list_after[0]["position_name"] == position_b["name"]
    assert res_list_after[0]["company_name"] == company_b["name"]
