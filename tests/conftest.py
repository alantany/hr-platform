from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from sqlalchemy import inspect

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app.database import SessionLocal
from backend.app.models import (
    AiTask,
    AuditLog,
    Candidate,
    CandidateFollowUpRecord,
    CandidateMailRecord,
    CandidateNote,
    CandidateTrackingEvent,
    Company,
    DataPermission,
    Delivery,
    EmailConfig,
    EmploymentRecord,
    Evaluation,
    EvaluationLevel,
    ExportRecord,
    ImportRecord,
    InterviewRecord,
    Notification,
    Position,
    Project,
    Recommendation,
    RecommendationFeedback,
    Role,
    RolePermission,
    SalaryRecord,
    SearchPreset,
    SystemConfig,
    TagDictionary,
    User,
    WarrantyRule,
)
from backend.app.main import ROOT_DIR


BASELINE_KEYS: dict[str, set] = {}


def _snapshot_primary_keys(db):
    snapshot: dict[str, set] = {}
    for model in _cleanup_order():
        pk_col = inspect(model).primary_key[0]
        snapshot[model.__tablename__] = {value for (value,) in db.query(pk_col).all()}
    return snapshot


def _delete_rows_not_in_baseline(db, model, baseline_values: set):
    pk_col = inspect(model).primary_key[0]
    query = db.query(model)
    if baseline_values:
        query = query.filter(~pk_col.in_(baseline_values))
    query.delete(synchronize_session=False)


def _fetch_new_file_paths(db, model, baseline_values: set) -> set[str]:
    pk_col = inspect(model).primary_key[0]
    query = db.query(model.file_path)
    if baseline_values:
        query = query.filter(~pk_col.in_(baseline_values))
    return {path for (path,) in query.all() if path}


def _cleanup_order():
    return [
        CandidateTrackingEvent,
        InterviewRecord,
        SalaryRecord,
        EmploymentRecord,
        CandidateFollowUpRecord,
        CandidateMailRecord,
        CandidateNote,
        Evaluation,
        RecommendationFeedback,
        Delivery,
        Recommendation,
        ExportRecord,
        ImportRecord,
        Notification,
        AiTask,
        AuditLog,
        SearchPreset,
        DataPermission,
        RolePermission,
        TagDictionary,
        EvaluationLevel,
        WarrantyRule,
        SystemConfig,
        EmailConfig,
        Candidate,
        Position,
        Project,
        Company,
        Role,
        User,
    ]


def _reset_seed_rows(db):
    admin = db.query(User).filter(User.username == "admin").first()
    if admin is None:
        db.add(User(username="admin", full_name="系统管理员", password_hash="dev", role="超级管理员", is_active=True))
    else:
        admin.full_name = "系统管理员"
        admin.password_hash = "dev"
        admin.role = "超级管理员"
        admin.is_active = True

    db.query(WarrantyRule).delete(synchronize_session=False)
    db.add_all([
        WarrantyRule(scope="简历", months=3, remind_days=10, auto_expire=True),
        WarrantyRule(scope="客户", months=6, remind_days=7, auto_expire=True),
        WarrantyRule(scope="项目", months=6, remind_days=7, auto_expire=True),
        WarrantyRule(scope="岗位", months=3, remind_days=5, auto_expire=True),
        WarrantyRule(scope="入职质保期", months=2, remind_days=5, auto_expire=True),
    ])

    db.query(SystemConfig).delete(synchronize_session=False)
    db.add_all([
        SystemConfig(key="site_name", value="招聘管理平台", description="系统名称"),
        SystemConfig(key="watermark", value="招聘管理系统", description="水印模板"),
        SystemConfig(key="log_retention_days", value="90", description="日志保留天数"),
        SystemConfig(key="responsive_breakpoint", value="1280", description="响应式断点"),
    ])

    db.query(EmailConfig).delete(synchronize_session=False)
    db.add(EmailConfig(host="smtp.example.com", port=25, sender="noreply@example.com", username="", password="", use_tls=False, enabled=False))


def _cleanup_obvious_test_artifacts(db):
    db.query(RolePermission).filter(RolePermission.permission_key == "page:permissions:smoke").delete(synchronize_session=False)
    db.query(DataPermission).filter(DataPermission.scope_id == "team-smoke").delete(synchronize_session=False)
    db.query(Notification).filter(Notification.title == "新通知").delete(synchronize_session=False)
    db.query(AiTask).filter(
        (AiTask.task_type == "jd_generate") & (AiTask.input_text == "Java Lead")
    ).delete(synchronize_session=False)
    db.query(AiTask).filter(
        (AiTask.task_type == "resume_parse") & (AiTask.input_text == "张三 简历")
    ).delete(synchronize_session=False)
    db.query(EvaluationLevel).filter(EvaluationLevel.name == "超级优秀").delete(synchronize_session=False)
    db.query(User).filter(User.username.like("temp_%")).delete(synchronize_session=False)
    db.query(Role).filter(Role.code.like("TEMP_%")).delete(synchronize_session=False)
    db.query(Role).filter(Role.code.like("DEL_%")).delete(synchronize_session=False)


def _delete_generated_files(paths: set[str]):
    for raw_path in paths:
        if not raw_path:
            continue
        candidates = [
            ROOT_DIR / raw_path.lstrip("/"),
            ROOT_DIR / raw_path,
            ROOT_DIR / "Recruit" / raw_path,
        ]
        for candidate in candidates:
            try:
                if candidate.exists():
                    candidate.unlink()
                    break
            except OSError:
                continue


def _cleanup_new_rows_and_files():
    db = SessionLocal()
    try:
        file_paths: set[str] = set()
        for model in _cleanup_order():
            baseline_values = BASELINE_KEYS.get(model.__tablename__, set())
            if model in {ExportRecord, Candidate}:
                file_paths.update(_fetch_new_file_paths(db, model, baseline_values))

            _delete_rows_not_in_baseline(db, model, baseline_values)

        _reset_seed_rows(db)
        db.commit()
        _delete_generated_files(file_paths)
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def _prepare_database():
    db = SessionLocal()
    try:
        _reset_seed_rows(db)
        _cleanup_obvious_test_artifacts(db)
        db.commit()
        global BASELINE_KEYS
        BASELINE_KEYS = _snapshot_primary_keys(db)
    finally:
        db.close()

    yield

    _cleanup_new_rows_and_files()


@pytest.fixture(autouse=True)
def _cleanup_test_data_after_each_test():
    yield
    _cleanup_new_rows_and_files()
