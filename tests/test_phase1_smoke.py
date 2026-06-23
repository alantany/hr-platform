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


def test_phase1_chain_smoke():
    suffix = uuid4().hex[:8]
    headers = auth_headers()
    company = client.post("/api/companies", json={"name": f"测试客户B-{suffix}", "contact_name": "负责人", "contact_phone": "13800002222"}, headers=headers).json()
    updated_company = client.patch(f"/api/companies/{company['id']}", json={"contact_name": "负责人-改"}, headers=headers).json()
    toggled_company = client.post(f"/api/companies/{company['id']}/toggle", headers=headers).json()
    project = client.post("/api/projects", json={"company_id": company["id"], "name": f"测试项目B-{suffix}", "work_location": "深圳"}, headers=headers).json()
    updated_project = client.patch(f"/api/projects/{project['id']}", json={"status": "招聘完毕"}, headers=headers).json()
    toggled_project = client.post(f"/api/projects/{project['id']}/toggle", headers=headers).json()
    position = client.post("/api/positions", json={"project_id": project["id"], "name": f"后端工程师B-{suffix}", "urgency": "高"}, headers=headers).json()
    updated_position = client.patch(f"/api/positions/{position['id']}", json={"status": "暂停招聘", "salary_min": 20, "salary_max": 35, "location": "广州"}, headers=headers).json()
    positions = client.get(f"/api/positions?project_id={project['id']}", headers=headers).json()
    candidate = client.post("/api/candidates", json={"name": f"候选人B-{suffix}", "phone": f"1381111{suffix[:4]}", "city": "深圳"}, headers=headers).json()
    updated_candidate = client.patch(f"/api/candidates/{candidate['id']}", json={"phone": f"1392222{suffix[:4]}", "city": "广州", "status": "激活", "source": "页面编辑"}, headers=headers).json()
    mailed_candidate = client.patch(f"/api/candidates/{candidate['id']}", json={"email": f"{suffix}@example.com", "current_title": "高级工程师"}, headers=headers).json()
    mail_record = client.post("/api/candidate-mail-records", json={"candidate_id": candidate["id"], "recipient_email": f"{suffix}@example.com", "mail_subject": f"候选人B-{suffix}-高级工程师", "mail_body": "候选人信息预览", "attachment_name": f"候选人B-{suffix}-高级工程师.pdf", "sent_by": "admin", "status": "已发送"}, headers=headers).json()
    mail_records = client.get(f"/api/candidate-mail-records?candidate_id={candidate['id']}", headers=headers).json()
    salary_record = client.post("/api/salary-records", json={"candidate_id": candidate["id"], "expected_salary": "20k-30k", "offered_salary": "25k", "service_status": "已完成", "note": "薪资跟踪验证"}, headers=headers).json()
    employment_record = client.post("/api/employment-records", json={"candidate_id": candidate["id"], "status": "已入职", "company_name": "测试公司", "position_name": "高级工程师", "note": "入职验证"}, headers=headers).json()
    promoted_candidate = client.patch(f"/api/candidates/{candidate['id']}", json={"status": "已录用"}, headers=headers).json()
    followup_record = client.post("/api/candidate-follow-up-records", json={"candidate_id": candidate["id"], "status": "已录用", "follow_up_time": "2026-06-16T10:00:00", "content": "候选人已入职后随访", "operator": "admin"}, headers=headers).json()
    followup_records = client.get(f"/api/candidate-follow-up-records?candidate_id={candidate['id']}", headers=headers).json()
    note_record = client.post("/api/candidate-notes", json={"candidate_id": candidate["id"], "content": "测试候选人备注记录", "operator": "admin"}, headers=headers).json()
    note_records = client.get(f"/api/candidate-notes?candidate_id={candidate['id']}", headers=headers).json()
    
    # 测试候选人跟踪面试记录
    tracking_record = client.post("/api/candidate-tracking-events", json={
        "candidate_id": candidate["id"],
        "event_type": "面试",
        "status": "已完成",
        "interview_round": "初筛",
        "screening_result": "通过",
        "interview_date": "2026-05-23",
        "interviewer": "张三",
        "interview_location": "北京市海淀区",
        "interview_requirements": "带身份证",
        "interview_contact": "138-0000-0001",
        "interview_result": "-",
        "note": "符合要求",
        "employment_status": "待设置",
        "operator": "admin"
    }, headers=headers).json()
    tracking_records = client.get(f"/api/candidate-tracking-events?candidate_id={candidate['id']}", headers=headers).json()

    # 测试修改跟踪面试记录
    updated_tracking = client.put(f"/api/candidate-tracking-events/{tracking_record['id']}", json={
        "candidate_id": candidate["id"],
        "event_type": "面试",
        "status": "已完成",
        "interview_round": "初筛",
        "screening_result": "通过",
        "interview_date": "2026-05-23",
        "interviewer": "李四",
        "interview_location": "北京市海淀区中关村",
        "interview_requirements": "带身份证、学历证",
        "interview_contact": "138-0000-0001",
        "interview_result": "-",
        "note": "非常合适",
        "employment_status": "待设置",
        "operator": "admin"
    }, headers=headers).json()
    
    # 测试删除面试记录
    deleted_resp = client.delete(f"/api/candidate-tracking-events/{tracking_record['id']}", headers=headers).json()

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
            "file_name": f"{candidate['name']}-{position['name']}.pdf",
            "file_path": f"/exports/{candidate['name']}.pdf",
        },
        headers=headers,
    ).json()
    export_records = client.get(f"/api/export-records?candidate_id={candidate['id']}", headers=headers).json()
    locked_by_update = client.patch(f"/api/candidates/{candidate['id']}", json={"locked": True}, headers=headers).json()
    locked = client.post(f"/api/candidates/{candidate['id']}/lock", headers=headers).json()
    # 获取 admin 用户的动态 ID
    users_list = client.get("/api/users", headers=headers).json()
    admin_id = next(u["id"] for u in users_list if u["username"] == "admin")
    reset_user = client.post(f"/api/users/{admin_id}/reset-password", json={"password_hash": f"dev-{suffix}"}, headers=headers).json()
    edited_user = client.patch(f"/api/users/{admin_id}", json={"full_name": f"管理员-{suffix}", "role": "组长"}, headers=headers).json()
    temp_role = client.post("/api/roles", json={"code": f"TEMP_{suffix}", "name": f"临时角色-{suffix}", "description": "临时测试角色"}, headers=headers).json()
    temp_user = client.post("/api/users", json={"username": f"temp_{suffix}", "full_name": "临时用户", "role": temp_role["name"], "password_hash": "dev"}, headers=headers).json()
    role_delete_blocked = client.delete(f"/api/roles/{temp_role['id']}", headers=headers)
    removable_role = client.post("/api/roles", json={"code": f"DEL_{suffix}", "name": f"可删角色-{suffix}", "description": "临时删除角色"}, headers=headers).json()
    role_delete_ok = client.delete(f"/api/roles/{removable_role['id']}", headers=headers).json()
    preset = client.post("/api/search-presets", json={"name": f"快捷-{suffix}", "keyword": "Java", "city": "深圳", "status": "激活", "created_by": "admin"}, headers=headers).json()
    presets = client.get("/api/search-presets", headers=headers).json()
    recommendation_blocked = client.post("/api/recommendations", json={"candidate_id": candidate["id"], "position_id": position["id"], "recommender": "admin"}, headers=headers)
    released = client.post(f"/api/candidates/{candidate['id']}/release", headers=headers).json()
    recommendation = client.post("/api/recommendations", json={"candidate_id": candidate["id"], "position_id": position["id"], "recommender": "admin"}, headers=headers).json()
    rec = client.post("/api/recommendations", json={"candidate_id": candidate["id"], "position_id": position["id"], "recommender": "admin"}, headers=headers).json()
    feedback_record = client.post("/api/recommendation-feedbacks", json={"recommendation_id": rec["id"], "status": "客户已收", "feedback": "客户同意推进", "customer_comment": "安排下一步面试", "operator": "admin"}, headers=headers).json()
    feedback_records = client.get(f"/api/recommendation-feedbacks?recommendation_id={rec['id']}", headers=headers).json()
    delivery = client.post("/api/deliveries", json={"recommendation_id": rec["id"], "delivered_by": "admin"}, headers=headers).json()
    client.put(f"/api/recommendations/{rec['id']}", json={"status": "已推荐"}, headers=headers)
    rec_status = client.put(f"/api/recommendations/{rec['id']}", json={"status": "客户已收", "feedback": "浏览器验收推进", "customer_comment": "客户确认接收"}, headers=headers).json()
    rec_list = client.get(f"/api/recommendations?candidate_id={candidate['id']}", headers=headers).json()
    delivery_list = client.get(f"/api/deliveries?recommendation_id={rec['id']}", headers=headers).json()
    logs = client.get("/api/audit-logs", headers=headers).json()

    assert company["name"] == f"测试客户B-{suffix}"
    assert updated_company["contact_name"] == "负责人-改"
    assert toggled_company["status"] in {"招聘中", "空闲", "失效"}
    assert project["company_id"] == company["id"]
    assert updated_project["status"] == "招聘完毕"
    assert toggled_project["status"] in {"招聘中", "招聘完毕", "招聘中止"}
    assert position["project_id"] == project["id"]
    assert updated_position["status"] == "暂停招聘"
    assert updated_position["salary_min"] == 20
    assert updated_position["salary_max"] == 35
    assert updated_position["location"] == "广州"
    assert any(item["id"] == position["id"] for item in positions)
    assert updated_candidate["phone"] == f"1392222{suffix[:4]}"
    assert updated_candidate["city"] == "广州"
    assert updated_candidate["source"] == "页面编辑"
    assert mailed_candidate["email"] == f"{suffix}@example.com"
    assert mail_record["mail_subject"] == f"候选人B-{suffix}-高级工程师"
    assert any(item["candidate_id"] == candidate["id"] for item in mail_records)
    assert salary_record["expected_salary"] == "20k-30k"
    assert employment_record["status"] == "已入职"
    assert promoted_candidate["status"] == "已录用"
    assert followup_record["content"] == "候选人已入职后随访"
    assert any(item["candidate_id"] == candidate["id"] for item in followup_records)
    assert note_record["content"] == "测试候选人备注记录"
    assert any(item["candidate_id"] == candidate["id"] for item in note_records)
    
    # 验证候选人跟踪记录字段
    assert tracking_record["interview_round"] == "初筛"
    assert tracking_record["screening_result"] == "通过"
    assert any(item["candidate_id"] == candidate["id"] for item in tracking_records)
    assert updated_tracking["interviewer"] == "李四"
    assert updated_tracking["interview_location"] == "北京市海淀区中关村"
    assert deleted_resp["success"] is True

    assert export_record["candidate_id"] == candidate["id"]
    assert export_record["file_name"] == f"{candidate['name']}-简历报告.pdf"
    assert any(item["candidate_id"] == candidate["id"] for item in export_records)
    assert locked_by_update["locked"] is True
    assert locked["locked"] is True
    assert reset_user["password_hash"] == f"dev-{suffix}"
    assert edited_user["full_name"] == f"管理员-{suffix}"
    assert edited_user["role"] == "组长"
    assert role_delete_blocked.status_code == 400
    assert role_delete_ok["ok"] is True
    assert recommendation_blocked.status_code == 400
    assert released["locked"] is False
    assert recommendation["candidate_id"] == candidate["id"]
    assert preset["name"] == f"快捷-{suffix}"
    assert any(item["name"] == f"快捷-{suffix}" for item in presets)
    assert rec["candidate_id"] == candidate["id"]
    assert feedback_record["status"] == "客户已收"
    assert any(item["recommendation_id"] == rec["id"] for item in feedback_records)
    assert delivery["recommendation_id"] == rec["id"]
    assert rec_status["status"] == "客户已收"
    assert any(item["status"] == "客户已收" for item in rec_list)
    assert any(log["action"] == "锁定候选人" for log in logs)

    # Test database resource explorer endpoints
    tables_list = client.get("/api/db-tables", headers=headers).json()
    assert isinstance(tables_list, list)
    assert "users" in tables_list
    assert "candidate_notes" in tables_list

    # Query table with model mapping
    users_data = client.get("/api/db-tables?table_name=users", headers=headers).json()
    assert users_data["table_name"] == "users"
    assert "id" in users_data["columns"]
    assert len(users_data["records"]) > 0
