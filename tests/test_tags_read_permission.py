"""标签字段配置：全角色可读，管理写仍限管理员。"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.main import app
from tests.auth_helpers import login_headers


def test_all_roles_can_read_tag_configs_but_only_admin_can_write():
    with TestClient(app) as client:
        admin = login_headers(client, "admin")
        leader = login_headers(client, "leader")
        operator = login_headers(client, "operator")

        for headers in (admin, leader, operator):
            res = client.get("/api/tags", headers=headers)
            assert res.status_code == 200, res.text
            assert isinstance(res.json(), list)

        create_res = client.post(
            "/api/tags",
            json={
                "object_type": "candidate",
                "field_key": "education",
                "field_label": "学历",
                "style_key": "neutral",
                "sort_order": 10,
                "enabled": True,
            },
            headers=operator,
        )
        assert create_res.status_code in (401, 403), create_res.text
