"""标签字段配置：全角色可读；写操作按 page:dictionary 放行。"""
from pathlib import Path
import sys
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.database import SessionLocal
from backend.app.models import RolePermission
from tests.auth_helpers import login_headers


def _set_operator_page_perm(permission_key: str, enabled: bool) -> tuple[bool, bool | None]:
    """返回 (created_new_row, previous_enabled_or_None)。"""
    db = SessionLocal()
    try:
        row = (
            db.query(RolePermission)
            .filter(
                RolePermission.role_code == "OPERATOR",
                RolePermission.permission_key == permission_key,
            )
            .first()
        )
        if row:
            previous = bool(row.enabled)
            row.enabled = enabled
            db.commit()
            return False, previous
        if enabled:
            db.add(
                RolePermission(
                    role_code="OPERATOR",
                    permission_key=permission_key,
                    permission_type="menu",
                    module="系统设置",
                    enabled=True,
                )
            )
            db.commit()
            return True, None
        return False, None
    finally:
        db.close()


def _restore_operator_page_perm(permission_key: str, created_new: bool, previous_enabled: bool | None) -> None:
    db = SessionLocal()
    try:
        if created_new:
            db.query(RolePermission).filter(
                RolePermission.role_code == "OPERATOR",
                RolePermission.permission_key == permission_key,
            ).delete(synchronize_session=False)
        elif previous_enabled is not None:
            row = (
                db.query(RolePermission)
                .filter(
                    RolePermission.role_code == "OPERATOR",
                    RolePermission.permission_key == permission_key,
                )
                .first()
            )
            if row:
                row.enabled = previous_enabled
        db.commit()
    finally:
        db.close()


def test_all_roles_can_read_tag_configs_but_write_needs_page_dictionary():
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


def test_leader_with_page_dictionary_can_write_tags_and_hotwords():
    suffix = uuid4().hex[:8]
    with TestClient(app) as client:
        leader = login_headers(client, "leader")
        operator = login_headers(client, "operator")

        tag_payload = {
            "object_type": "candidate",
            "field_key": f"custom_{suffix}",
            "field_label": f"标签{suffix}",
            "style_key": "neutral",
            "sort_order": 99,
            "enabled": True,
        }
        created = client.post("/api/tags", json=tag_payload, headers=leader)
        assert created.status_code == 200, created.text
        tag_id = created.json()["id"]

        patched = client.patch(f"/api/tags/{tag_id}", json={"enabled": False}, headers=leader)
        assert patched.status_code == 200, patched.text
        assert patched.json()["enabled"] is False

        hotword = client.post(
            "/api/search-hotwords",
            json={"keyword": f"热词{suffix}", "sort_order": 1, "enabled": True},
            headers=leader,
        )
        assert hotword.status_code == 200, hotword.text
        hotword_id = hotword.json()["id"]

        listed = client.get("/api/search-hotwords", headers=leader)
        assert listed.status_code == 200, listed.text

        assert client.delete(f"/api/search-hotwords/{hotword_id}", headers=leader).status_code == 200
        assert client.delete(f"/api/tags/{tag_id}", headers=leader).status_code == 200

        assert client.get("/api/search-hotwords", headers=operator).status_code == 403
        assert client.post(
            "/api/search-hotwords",
            json={"keyword": f"拒{suffix}", "sort_order": 1, "enabled": True},
            headers=operator,
        ).status_code == 403


def test_operator_granted_page_dictionary_can_write_then_revoke():
    suffix = uuid4().hex[:8]
    created_new, previous = _set_operator_page_perm("page:dictionary", True)
    try:
        with TestClient(app) as client:
            operator = login_headers(client, "operator")
            created = client.post(
                "/api/tags",
                json={
                    "object_type": "candidate",
                    "field_key": f"op_{suffix}",
                    "field_label": f"操作员标签{suffix}",
                    "style_key": "neutral",
                    "sort_order": 1,
                    "enabled": True,
                },
                headers=operator,
            )
            assert created.status_code == 200, created.text
            tag_id = created.json()["id"]
            assert client.delete(f"/api/tags/{tag_id}", headers=operator).status_code == 200
    finally:
        _restore_operator_page_perm("page:dictionary", created_new, previous)

    with TestClient(app) as client:
        operator = login_headers(client, "operator")
        denied = client.post(
            "/api/tags",
            json={
                "object_type": "candidate",
                "field_key": f"op_denied_{suffix}",
                "field_label": "应拒绝",
                "style_key": "neutral",
                "sort_order": 1,
                "enabled": True,
            },
            headers=operator,
        )
        assert denied.status_code == 403, denied.text
