from pathlib import Path
import sys
from uuid import uuid4
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def auth_headers():
    token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_employment_onboarding_and_warranty():
    suffix = uuid4().hex[:8]
    headers = auth_headers()
    
    # 1. 验证 WarrantyRule 中有“入职质保期”种子配置
    res_rules = client.get("/api/warranty-rules", headers=headers)
    assert res_rules.status_code == 200
    rules = res_rules.json()
    rule_scope_list = [r["scope"] for r in rules]
    assert "入职质保期" in rule_scope_list
    target_rule = [r for r in rules if r["scope"] == "入职质保期"][0]
    assert target_rule["months"] == 2 # 默认为 2 个月 (60天)
    
    # 2. 创建候选人
    candidate = client.post("/api/candidates", json={
        "name": f"入职测试候选人-{suffix}",
        "phone": f"1377777{suffix[:4]}",
        "city": "杭州"
    }, headers=headers).json()
    candidate_id = candidate["id"]
    
    # 3. 为候选人创建一条面试记录 (CandidateTrackingEvent)
    tracking = client.post("/api/candidate-tracking-events", json={
        "candidate_id": candidate_id,
        "event_type": "面试",
        "status": "已完成",
        "interview_round": "第1轮",
        "screening_result": "通过",
        "interview_date": "2026-06-20",
        "interviewer": "老王",
        "interview_location": "视频面试",
        "interview_requirements": "无需",
        "interview_contact": "13700000000",
        "interview_result": "-",
        "note": "初筛通过",
        "employment_status": "待设置"
    }, headers=headers).json()
    
    # 4. 创建一条约定薪资记录 (SalaryRecord)
    client.post("/api/salary-records", json={
        "candidate_id": candidate_id,
        "interview_round": "第1轮",
        "position_name": "Go开发工程师",
        "company_name": "阿里云",
        "agreed_salary": "32K",
        "welfare_desc": "大厂福利",
        "onboard_cond": "无",
        "candidate_accepted": "接受",
        "operator": "admin"
    }, headers=headers).json()
    
    # 5. 模拟“已入职”数据保存
    onboard_payload = {
        "candidate_id": candidate_id,
        "status": "已入职",
        "company_name": "阿里云",
        "position_name": "Go开发工程师",
        "onboard_date": datetime.utcnow().isoformat() + "Z",
        "note": "确认入职"
    }
    
    res_onboard = client.post("/api/employment-records", json=onboard_payload, headers=headers)
    assert res_onboard.status_code == 200
    
    # 6. 验证已入职联动更新：
    # a. 面试记录 (CandidateTrackingEvent) 的 employment_status 应变更为 "已入职"
    res_tracking_list = client.get(f"/api/candidate-tracking-events?candidate_id={candidate_id}", headers=headers).json()
    assert len(res_tracking_list) == 1
    assert res_tracking_list[0]["employment_status"] == "已入职"
    
    # b. 根据新业务规则：候选人入职后 locked=True，status="锁定"（入职状态存储在 EmploymentRecord 里）
    res_cand_detail = client.get("/api/candidates", headers=headers).json()
    updated_cand = [c for c in res_cand_detail if c["id"] == candidate_id][0]
    assert updated_cand["locked"] is True
    assert updated_cand["status"] == "锁定"

    # c. 验证获取入职记录列表包含 candidate_name 和 candidate_phone 字段
    res_emp_records = client.get("/api/employment-records", headers=headers).json()
    my_record = [r for r in res_emp_records if r["candidate_id"] == candidate_id][0]
    assert my_record["candidate_name"] == f"入职测试候选人-{suffix}"
    assert my_record["candidate_phone"] == f"1377777{suffix[:4]}"
    # d. 入职记录的 warranty_status 应被动态返回为"质保中"（刚入职，未超 180 天）
    assert my_record["warranty_status"] == "质保中"

    # 7. 模拟"未入职"数据保存（修改状态为未入职，例如候选人爽约）
    not_onboard_payload = {
        "candidate_id": candidate_id,
        "status": "未入职",
        "company_name": "",
        "position_name": "",
        "onboard_date": None,
        "note": "候选人临时爽约"
    }
    
    res_not_onboard = client.post("/api/employment-records", json=not_onboard_payload, headers=headers)
    assert res_not_onboard.status_code == 200
    
    # 8. 验证未入职联动更新：
    # a. 面试记录 (CandidateTrackingEvent) 的 employment_status 应变更为 "未入职"
    res_tracking_list_2 = client.get(f"/api/candidate-tracking-events?candidate_id={candidate_id}", headers=headers).json()
    assert res_tracking_list_2[0]["employment_status"] == "未入职"
    
    # b. 根据新的业务规则：候选人一旦被推荐锁定后，锁定状态持久保持，不因入职状态变化而解锁
    #    未入职不代表候选人重新"未锁定"；解锁需要人工通过 /release 接口手动执行
    res_cand_detail_2 = client.get("/api/candidates", headers=headers).json()
    updated_cand_2 = [c for c in res_cand_detail_2 if c["id"] == candidate_id][0]
    # 候选人自身 status 维持 "锁定"（锁定持久化规则），locked 字段为 True
    assert updated_cand_2["locked"] is True
    assert updated_cand_2["status"] == "锁定"
