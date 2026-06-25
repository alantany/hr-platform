from __future__ import annotations

import hashlib
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


def hash_password(password: str) -> str:
    return "sha256:" + hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, stored_password: str) -> bool:
    if stored_password.startswith("sha256:"):
        return hash_password(password) == stored_password
    return password == stored_password


def issue_user_token(user: User) -> str:
    return f"user:{user.username}"


def get_role_code(role: str | None) -> str:
    return ROLE_CODE_MAP.get(str(role or "").strip(), str(role or "").strip().upper())


def is_admin(user: User) -> bool:
    return get_role_code(user.role) == "ADMIN"


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
    permissions = _active_permissions(db, user)
    allowed_companies = {p.scope_id for p in permissions if p.scope_type == "company"}
    allowed_projects = {p.scope_id for p in permissions if p.scope_type == "project"}
    allowed_positions = {p.scope_id for p in permissions if p.scope_type == "position"}

    if scope_type == "company":
        return scope_id in allowed_companies
    if scope_type == "project":
        if scope_id in allowed_projects:
            return True
        project = db.get(Project, int(scope_id))
        return bool(project and str(project.company_id) in allowed_companies)
    if scope_type == "position":
        if scope_id in allowed_positions:
            return True
        position = db.get(Position, int(scope_id))
        if not position:
            return False
        project = position.project
        return bool(
            str(position.project_id) in allowed_projects
            or (project and str(project.company_id) in allowed_companies)
        )
    if scope_type == "candidate":
        candidate = db.get(Candidate, int(scope_id))
        if not candidate:
            return False
        if candidate.owner_user_id == user.id:
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


def accessible_candidate_ids(db: Session, user: User) -> list[int]:
    if is_admin(user):
        return [row[0] for row in db.query(Candidate.id).all()]
    ids: set[int] = set()
    for candidate_id, owner_user_id in db.query(Candidate.id, Candidate.owner_user_id).all():
        if owner_user_id == user.id:
            ids.add(candidate_id)
    recommendation_rows = (
        db.query(Recommendation.candidate_id, Recommendation.position_id)
        .distinct()
        .all()
    )
    for candidate_id, position_id in recommendation_rows:
        if can_access_scope(db, user, "position", position_id):
            ids.add(candidate_id)
    return sorted(ids)


def get_current_user(db: Session, authorization: str | None) -> User:
    token = (authorization or "").removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="请先登录")
    if token == settings.access_token:
        user = db.query(User).filter(User.username == "admin").first()
    elif token.startswith("user:"):
        user = db.query(User).filter(User.username == token.removeprefix("user:")).first()
    else:
        user = db.query(User).filter(User.username == token).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="账号不可用")
    return user


def require_roles(*roles: str):
    def decorator(handler: Callable):
        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        return wrapper

    return decorator
