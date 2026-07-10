"""质保规则：有 page:warranty 即可读写；无权限仍 403。"""
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


def test_leader_with_page_warranty_can_crud_rules():
    suffix = uuid4().hex[:8]
    with TestClient(app) as client:
        leader = login_headers(client, "leader")
        operator = login_headers(client, "operator")

        listed = client.get("/api/warranty-rules", headers=leader)
        assert listed.status_code == 200, listed.text

        created = client.post(
            "/api/warranty-rules",
            json={"scope": f"测试范围{suffix}", "months": 3, "remind_days": 7, "auto_expire": True},
            headers=leader,
        )
        assert created.status_code == 200, created.text
        rule_id = created.json()["id"]

        updated = client.put(
            f"/api/warranty-rules/{rule_id}",
            json={"scope": f"测试范围{suffix}", "months": 6, "remind_days": 5, "auto_expire": False},
            headers=leader,
        )
        assert updated.status_code == 200, updated.text
        assert updated.json()["months"] == 6

        assert client.delete(f"/api/warranty-rules/{rule_id}", headers=leader).status_code == 200

        assert client.get("/api/warranty-rules", headers=operator).status_code == 403
        assert client.post(
            "/api/warranty-rules",
            json={"scope": f"拒{suffix}", "months": 1, "remind_days": 1, "auto_expire": True},
            headers=operator,
        ).status_code == 403


def test_operator_granted_page_warranty_can_read_then_revoke():
    created_new, previous = _set_operator_page_perm("page:warranty", True)
    try:
        with TestClient(app) as client:
            operator = login_headers(client, "operator")
            assert client.get("/api/warranty-rules", headers=operator).status_code == 200
    finally:
        _restore_operator_page_perm("page:warranty", created_new, previous)

    with TestClient(app) as client:
        operator = login_headers(client, "operator")
        assert client.get("/api/warranty-rules", headers=operator).status_code == 403
