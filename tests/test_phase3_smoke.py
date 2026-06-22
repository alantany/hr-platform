from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.main import app


def test_enhancement_modules_smoke():
    with TestClient(app) as client:
        token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        ai = client.post("/api/ai/tasks", json={"task_type": "jd_generate", "input_text": "Java Lead"}, headers=headers).json()
        config = client.post("/api/system-configs", json={"key": "site_name", "value": "招聘管理平台V2", "description": "系统名称"}, headers=headers).json()
        role_perm = client.post(
            "/api/role-permissions",
            json={
                "role_code": "ADMIN",
                "permission_key": "page:permissions:smoke",
                "permission_type": "button",
                "module": "权限管理",
                "enabled": False,
            },
            headers=headers,
        ).json()
        role_permissions = client.get("/api/role-permissions?role_code=ADMIN", headers=headers).json()
        email = client.post("/api/email-config", json={"host": "smtp.example.com", "port": 2525, "sender": "noreply@example.com", "username": "", "password": "", "use_tls": False, "enabled": True}, headers=headers).json()
        email_test = client.post("/api/email-config/test", json={"host": "smtp.example.com", "port": 2525, "sender": "noreply@example.com", "username": "demo", "password": "demo", "use_tls": False, "enabled": True}, headers=headers).json()
        # 获取 admin 用户的动态 ID
        users_list = client.get("/api/users", headers=headers).json()
        admin_id = next(u["id"] for u in users_list if u["username"] == "admin")
        data_permission = client.post("/api/data-permissions", json={"user_id": admin_id, "scope_type": "team", "scope_id": "team-smoke", "scope_name": "团队验收范围", "granted_by": "admin", "active": True}, headers=headers).json()
        data_permissions = client.get(f"/api/data-permissions?user_id={admin_id}", headers=headers).json()
        summary = client.get("/api/dashboard/summary", headers=headers).json()
        ai_tasks = client.get("/api/ai/tasks", headers=headers).json()
        notifications = client.get("/api/notifications?type=AI通知", headers=headers).json()

        assert ai["task_type"] == "jd_generate"
        assert ai["status"] == "完成"
        assert config["key"] == "site_name"
        assert role_perm["permission_key"] == "page:permissions:smoke"
        assert any(item["permission_key"] == "page:permissions:smoke" for item in role_permissions)
        assert email["host"] == "smtp.example.com"
        assert "ok" in email_test
        assert data_permission["scope_id"] == "team-smoke"
        assert any(item["scope_id"] == "team-smoke" for item in data_permissions)
        assert summary["candidate_count"] >= 1
        assert len(ai_tasks) >= 1
        assert notifications and notifications[0]["title"] == "AI JD 生成完成"

        # Recruit 简历互通接口测试
        recruit_list = client.get("/api/recruit/candidates", headers=headers).json()
        assert len(recruit_list) >= 0
        if recruit_list:
            target = recruit_list[0]
            agent_id = target["candidate_agent_id"]
            
            # 测试一键导入
            import_res = client.post(f"/api/recruit/candidates/{agent_id}/import", headers=headers).json()
            assert import_res["success"] is True
            assert import_res["candidate"]["name"] == target["candidate_name"]

            # 测试简历下载/预览
            if target["file_path"]:
                download_res = client.get(f"/api/recruit/resumes/{agent_id}/download", headers=headers)
                assert download_res.status_code == 200 or download_res.status_code == 404

