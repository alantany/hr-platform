from __future__ import annotations

from pathlib import Path

from sqlalchemy import inspect
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app.main import ROOT_DIR
from backend.app.security import hash_password
from backend.app.models import (
    AiTask,
    AuditLog,
    Candidate,
    CandidateFollowUpRecord,
    CandidateMailRecord,
    CandidateNote,
    CandidateOwnershipTransfer,
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
    ResumeParseTask,
    Role,
    RolePermission,
    SalaryRecord,
    SearchPreset,
    SystemConfig,
    TagDictionary,
    User,
    WarrantyRule,
)


def cleanup_models() -> list[type]:
    return [
        CandidateTrackingEvent,
        CandidateOwnershipTransfer,
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
        ResumeParseTask,
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


def table_exists(db: Session, model: type) -> bool:
    table = model.__table__
    return inspect(db.bind).has_table(table.name, schema=table.schema)


def snapshot_primary_keys(db: Session) -> dict[str, set]:
    snapshot: dict[str, set] = {}
    for model in cleanup_models():
        if not table_exists(db, model):
            continue
        pk_col = inspect(model).primary_key[0]
        snapshot[model.__tablename__] = {value for (value,) in db.query(pk_col).all()}
    return snapshot


def delete_rows_not_in_baseline(db: Session, model: type, baseline_values: set) -> None:
    if not table_exists(db, model):
        return
    pk_col = inspect(model).primary_key[0]
    query = db.query(model)
    if baseline_values:
        query = query.filter(~pk_col.in_(baseline_values))
    query.delete(synchronize_session=False)


def delete_all_rows(db: Session, model: type) -> None:
    if not table_exists(db, model):
        return
    db.query(model).delete(synchronize_session=False)


def fetch_new_file_paths(db: Session, model: type, baseline_values: set) -> set[str]:
    if not table_exists(db, model):
        return set()
    pk_col = inspect(model).primary_key[0]
    query = db.query(model.file_path)
    if baseline_values:
        query = query.filter(~pk_col.in_(baseline_values))
    return {path for (path,) in query.all() if path}


def delete_generated_files(paths: set[str]) -> None:
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


def reset_seed_rows(db: Session) -> None:
    admin = db.query(User).filter(User.username == "admin").first()
    if admin is None:
        db.add(User(username="admin", full_name="系统管理员", password_hash=hash_password("admin123"), role="超级管理员", is_active=True))
    else:
        admin.full_name = "系统管理员"
        admin.password_hash = hash_password("admin123")
        admin.role = "超级管理员"
        admin.is_active = True
    leader = db.query(User).filter(User.username == "leader").first()
    if leader is None:
        db.add(User(username="leader", full_name="团队组长", password_hash=hash_password("leader123"), role="组长", is_active=True))
    else:
        leader.full_name = "团队组长"
        leader.password_hash = hash_password("leader123")
        leader.role = "组长"
        leader.is_active = True
    operator = db.query(User).filter(User.username == "operator").first()
    if operator is None:
        db.add(User(username="operator", full_name="一线操作员", password_hash=hash_password("operator123"), role="操作员", is_active=True))
    else:
        operator.full_name = "一线操作员"
        operator.password_hash = hash_password("operator123")
        operator.role = "操作员"
        operator.is_active = True

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
        SystemConfig(key="site_name", value="AI招聘管理平台", description="系统名称"),
        SystemConfig(key="watermark", value="招聘管理系统", description="水印模板"),
        SystemConfig(key="log_retention_days", value="90", description="日志保留天数"),
        SystemConfig(key="responsive_breakpoint", value="1280", description="响应式断点"),
    ])

    db.query(EmailConfig).delete(synchronize_session=False)
    db.add(EmailConfig(host="smtp.example.com", port=25, sender="noreply@example.com", username="", password="", use_tls=False, enabled=False))


def cleanup_obvious_test_artifacts(db: Session) -> None:
    db.query(ResumeParseTask).delete(synchronize_session=False)
    db.query(RolePermission).filter(RolePermission.permission_key == "page:permissions:smoke").delete(synchronize_session=False)
    db.query(DataPermission).filter(DataPermission.scope_id == "team-smoke").delete(synchronize_session=False)
    db.query(DataPermission).filter(DataPermission.scope_id == "position-smoke").delete(synchronize_session=False)
    db.query(Notification).filter(Notification.title == "新通知").delete(synchronize_session=False)
    db.query(AiTask).filter((AiTask.task_type == "jd_generate") & (AiTask.input_text == "Java Lead")).delete(synchronize_session=False)
    db.query(AiTask).filter((AiTask.task_type == "resume_parse") & (AiTask.input_text == "张三 简历")).delete(synchronize_session=False)
    db.query(EvaluationLevel).filter(EvaluationLevel.name == "超级优秀").delete(synchronize_session=False)
    db.query(User).filter(User.username.like("temp_%")).delete(synchronize_session=False)
    db.query(Role).filter(Role.code.like("TEMP_%")).delete(synchronize_session=False)
    db.query(Role).filter(Role.code.like("DEL_%")).delete(synchronize_session=False)


def cleanup_database_after_tests(baseline_keys: dict[str, set]) -> None:
    db = SessionLocal()
    try:
        file_paths: set[str] = set()
        for model in cleanup_models():
            baseline_values = baseline_keys.get(model.__tablename__, set())
            if model in {ExportRecord, Candidate}:
                file_paths.update(fetch_new_file_paths(db, model, baseline_values))
            delete_rows_not_in_baseline(db, model, baseline_values)

        reset_seed_rows(db)
        db.commit()
        delete_generated_files(file_paths)
    finally:
        db.close()


def full_reset_database() -> None:
    db = SessionLocal()
    try:
        file_paths: set[str] = set()
        for model in (Candidate, ExportRecord):
            if table_exists(db, model):
                file_paths.update(fetch_new_file_paths(db, model, set()))
        for model in cleanup_models():
            delete_all_rows(db, model)
        reset_seed_rows(db)
        db.commit()
        delete_generated_files(file_paths)
    finally:
        db.close()


def initialize_test_baseline() -> dict[str, set]:
    db = SessionLocal()
    try:
        reset_seed_rows(db)
        cleanup_obvious_test_artifacts(db)
        db.commit()
        return snapshot_primary_keys(db)
    finally:
        db.close()
