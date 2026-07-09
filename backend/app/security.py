from __future__ import annotations

import hashlib
import re
import secrets
from functools import wraps
from typing import Callable

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .config import settings
from .models import Candidate, Company, DataPermission, Position, Project, Recommendation, User


ROLE_CODE_MAP = {
    "超级管理员": "ADMIN",
    "ADMIN": "ADMIN",
    "组长": "LEADER",
    "LEADER": "LEADER",
    "操作员": "OPERATOR",
    "OPERATOR": "OPERATOR",
}


def normalize_candidate_name(name: str | None) -> str:
    """折叠姓名字符串中的连续重复字符，修复 wkhtmltopdf 等 PDF 逐字双写问题。"""
    text = str(name or "").strip()
    if not text:
        return text
    return re.sub(r"(.)\1+", r"\1", text)


def hash_password(password: str) -> str:
    return "sha256:" + hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, stored_password: str) -> bool:
    if stored_password.startswith("sha256:"):
        return hash_password(password) == stored_password
    return password == stored_password


SESSION_KICKED_MESSAGE = "您的账号已在其他设备登录，请重新登录"
SESSION_EXPIRED_MESSAGE = "登录已失效，请重新登录"


def rotate_user_session(user: User) -> str:
    user.session_token = secrets.token_urlsafe(32)
    return f"user:{user.username}:{user.session_token}"


def clear_user_session(user: User) -> None:
    user.session_token = None


def issue_user_token(user: User) -> str:
    if not user.session_token:
        return rotate_user_session(user)
    return f"user:{user.username}:{user.session_token}"


def parse_user_token(token: str) -> tuple[str | None, str | None]:
    if not token.startswith("user:"):
        return token, None
    payload = token.removeprefix("user:")
    if ":" not in payload:
        return payload, None
    username, session_token = payload.split(":", 1)
    return username, session_token or None


def get_role_code(role: str | None) -> str:
    return ROLE_CODE_MAP.get(str(role or "").strip(), str(role or "").strip().upper())


def is_admin(user: User) -> bool:
    return get_role_code(user.role) == "ADMIN"


def is_leader(user: User) -> bool:
    return get_role_code(user.role) == "LEADER"


def subordinate_user_ids(db: Session, user: User) -> set[int]:
    if not user.id:
        return set()
    from sqlalchemy import text
    sql = text("""
        WITH RECURSIVE sub_users AS (
            SELECT id FROM users WHERE manager_user_id = :user_id AND is_active = true
            UNION ALL
            SELECT u.id FROM users u
            INNER JOIN sub_users su ON u.manager_user_id = su.id
            WHERE u.is_active = true
        )
        SELECT id FROM sub_users
    """)
    rows = db.execute(sql, {"user_id": user.id}).fetchall()
    return {row[0] for row in rows}


def visible_owner_user_ids(db: Session, user: User) -> set[int]:
    ids = {user.id}
    if is_leader(user):
        ids.update(subordinate_user_ids(db, user))
    return ids


def _owner_visible(db: Session, user: User, owner_user_id: int | None) -> bool:
    return owner_user_id is not None and owner_user_id in visible_owner_user_ids(db, user)


def require_admin(user: User) -> User:
    if not is_admin(user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="仅超级管理员可执行该操作")
    return user


def require_super_admin(user: User) -> User:
    return require_admin(user)


def _active_permissions(db: Session, user: User) -> list[DataPermission]:
    return (
        db.query(DataPermission)
        .filter(DataPermission.user_id == user.id, DataPermission.active.is_(True))
        .order_by(DataPermission.scope_type.asc(), DataPermission.scope_id.asc())
        .all()
    )


def can_access_scope(db: Session, user: User, scope_type: str, scope_id: int | str | None) -> bool:
    if is_admin(user):
        return True
    if scope_id in (None, ""):
        return False
    scope_id = str(scope_id)
    if scope_type in {"company", "project", "position"}:
        return True
    permissions = _active_permissions(db, user)
    allowed_companies = {p.scope_id for p in permissions if p.scope_type == "company"}
    allowed_projects = {p.scope_id for p in permissions if p.scope_type == "project"}
    allowed_positions = {p.scope_id for p in permissions if p.scope_type == "position"}

    if scope_type == "company":
        company = db.get(Company, int(scope_id))
        if company and _owner_visible(db, user, company.owner_user_id):
            return True
        return scope_id in allowed_companies
    if scope_type == "project":
        if scope_id in allowed_projects:
            return True
        project = db.get(Project, int(scope_id))
        if project and _owner_visible(db, user, project.owner_user_id):
            return True
        return bool(project and (str(project.company_id) in allowed_companies or can_access_scope(db, user, "company", project.company_id)))
    if scope_type == "position":
        if scope_id in allowed_positions:
            return True
        position = db.get(Position, int(scope_id))
        if not position:
            return False
        if _owner_visible(db, user, position.owner_user_id):
            return True
        project = position.project
        return bool(
            str(position.project_id) in allowed_projects
            or (project and (str(project.company_id) in allowed_companies or can_access_scope(db, user, "project", project.id)))
        )
    if scope_type == "candidate":
        candidate = db.get(Candidate, int(scope_id))
        if not candidate:
            return False
        if _owner_visible(db, user, candidate.owner_user_id):
            return True
        candidate_positions = [
            row[0]
            for row in db.query(Recommendation.position_id)
            .filter(Recommendation.candidate_id == candidate.id)
            .all()
        ]
        for position_id in candidate_positions:
            if can_access_scope(db, user, "position", position_id):
                return True
        return False
    return False


def user_has_position_assignment(db: Session, user: User, position_id: int) -> bool:
    if is_admin(user):
        return True
    pos = db.get(Position, position_id)
    if not pos:
        return False
    allowed_ids = visible_owner_user_ids(db, user)
    if pos.owner_user_id in allowed_ids:
        return True
    has_perm = db.query(DataPermission).filter(
        DataPermission.user_id == user.id,
        DataPermission.scope_type == "position",
        DataPermission.scope_id == str(position_id),
        DataPermission.active.is_(True)
    ).first() is not None
    return has_perm


def accessible_candidate_ids(db: Session, user: User) -> list[int]:
    if is_admin(user):
        return [row[0] for row in db.query(Candidate.id).all()]
    ids: set[int] = set()
    visible_owner_ids = visible_owner_user_ids(db, user)
    for candidate_id, owner_user_id in db.query(Candidate.id, Candidate.owner_user_id).all():
        if owner_user_id in visible_owner_ids:
            ids.add(candidate_id)
    recommendation_rows = (
        db.query(Recommendation.candidate_id, Recommendation.position_id)
        .distinct()
        .all()
    )
    for candidate_id, position_id in recommendation_rows:
        if user_has_position_assignment(db, user, position_id):
            ids.add(candidate_id)
    return sorted(ids)


def get_current_user(db: Session, authorization: str | None) -> User:
    token = (authorization or "").removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="请先登录")
    if token == settings.access_token:
        user = db.query(User).filter(User.username == "admin").first()
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="账号不可用")
        return user

    username, session_token = parse_user_token(token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=SESSION_EXPIRED_MESSAGE)
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="账号不可用")
    if not session_token or not user.session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=SESSION_EXPIRED_MESSAGE)
    if session_token != user.session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=SESSION_KICKED_MESSAGE)
    return user


def require_roles(*roles: str):
    def decorator(handler: Callable):
        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        return wrapper

    return decorator
