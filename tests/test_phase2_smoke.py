from io import BytesIO
from pathlib import Path
import sys
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.main import app


def test_support_modules_smoke():
    with TestClient(app) as client:
        token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        level = client.post("/api/evaluation-levels", json={"name": "超级优秀", "score": 95, "description": "高分等级", "color": "green", "sort_order": 1, "enabled": True}, headers=headers).json()
        levels = client.get("/api/evaluation-levels", headers=headers).json()
        # 获取候选人的动态 ID
        candidates = client.get("/api/candidates", headers=headers).json()
        cand_id = candidates[0]["id"] if candidates else 1
        # 获取职位的动态 ID
        positions = client.get("/api/positions", headers=headers).json()
        pos_id = positions[0]["id"] if positions else 1
        evaluation = client.post("/api/evaluations", json={"candidate_id": cand_id, "position_id": pos_id, "evaluator": "admin", "round_name": "第2轮", "grade": "良好", "score": 4, "content": "阶段性通过"}, headers=headers).json()
        recommendation_stats = client.get("/api/recommendation-stats?operator=admin", headers=headers).json()
        tag = client.post("/api/tags", json={"category": "求职者标签", "name": "Python", "enabled": True}, headers=headers).json()
        tag2 = client.patch(f"/api/tags/{tag['id']}", json={"enabled": False}, headers=headers).json()
        delete_resp = client.delete(f"/api/tags/{tag['id']}", headers=headers).json()
        notification = client.post("/api/notifications", json={"user": "admin", "title": "新通知", "type": "测试通知", "target_path": "/src/pages/logs.html"}, headers=headers).json()
        read_back = client.post(f"/api/notifications/{notification['id']}/read", headers=headers).json()
        notifications = client.get("/api/notifications?keyword=新通知", headers=headers).json()
        warranty = client.post("/api/warranty-rules", json={"scope": "岗位", "months": 6, "remind_days": 5, "auto_expire": True}, headers=headers).json()
        warranty_rules = client.get("/api/warranty-rules", headers=headers).json()
        audit_logs = client.get("/api/audit-logs?keyword=通知", headers=headers).json()
        summary = client.get("/api/analytics/summary", headers=headers).json()

        assert level["name"] == "超级优秀"
        assert any(item["name"] == "超级优秀" for item in levels)
        assert evaluation["candidate_id"] == cand_id
        assert tag["name"] == "Python"
        assert tag2["enabled"] is False
        assert delete_resp["ok"] is True
        assert read_back["read"] is True
        assert any(item["title"] == "新通知" for item in notifications)
        assert len(audit_logs) >= 1
        assert "total" in recommendation_stats
        assert warranty["scope"] == "岗位"
        assert {item["scope"] for item in warranty_rules} >= {"简历", "客户", "项目", "岗位"}
        assert summary["evaluation_count"] >= 1
        assert summary["notification_count"] >= 1
        assert summary["tag_count"] >= 1
        assert summary["warranty_rule_count"] >= 1
        assert isinstance(summary["team_rankings"], list)
        assert isinstance(summary["customer_rankings"], list)


from unittest.mock import patch
from backend.app.models import Candidate

@patch("backend.app.main.parse_and_create_candidate")
def test_batch_import_smoke(mock_parse):
    def side_effect(db, full_path, save_name, username, owner_user_id):
        stem = Path(full_path).stem
        if "_" in stem:
            stem = stem.split("_", 1)[1]
        c = Candidate(
            name=stem,
            phone="13800000000",
            email="test@test.com",
            city="深圳",
            status="未锁定",
            source="AI解析"
        )
        db.add(c)
        db.flush()
        return {"status": "success", "candidate": c}
    mock_parse.side_effect = side_effect

    with TestClient(app) as client:
        token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        suffix = uuid4().hex[:8]
        files = [
            ("files", (f"batch-a-{suffix}.pdf", BytesIO(b"resume-a"), "application/pdf")),
            ("files", (f"batch-b-{suffix}.pdf", BytesIO(b"resume-b"), "application/pdf")),
        ]
        response = client.post("/api/imports/batch", files=files, headers=headers)
        assert response.status_code == 200
        payload = response.json()
        assert payload["imported"] == 2
        assert len(payload["import_records"]) == 2
        candidates = client.get("/api/candidates", headers=headers).json()
        assert any(item["name"] == f"batch-a-{suffix}" for item in candidates)
        assert any(item["name"] == f"batch-b-{suffix}" for item in candidates)
