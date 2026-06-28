from __future__ import annotations

from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from fastapi.responses import FileResponse
from . import crud, models, schemas
from .config import settings
from .database import Base, SessionLocal, engine, get_db
from .models import AuditLog, AiTask, Candidate, CandidateNote, CandidateFollowUpRecord, CandidateMailRecord, CandidateOwnershipTransfer, CandidateTrackingEvent, Company, DataPermission, Delivery, EmailConfig, EmploymentRecord, Evaluation, EvaluationLevel, InterviewRecord, Notification, Position, Project, Recommendation, RecommendationFeedback, Role, RolePermission, SalaryRecord, SearchPreset, SystemConfig, TagDictionary, WarrantyRule, User, RecruitCandidateProfile, RecruitResumeDownload, ExportRecord, ImportRecord, RecruitEmployee, RecruitJobPosting, RecruitDailyTaskStat, ResumeParseTask
from . import security
from .security import get_current_user
from backend.seed import seed as seed_data
import os
import json
import re
import time
import pdfplumber
from openai import OpenAI
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(os.path.join(ROOT_DIR, '.env'))


app = FastAPI(title="招聘管理系统 API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def ensure_schema() -> None:
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS recruit"))
    Base.metadata.create_all(bind=engine)

    from sqlalchemy import inspect
    inspector = inspect(engine)

    with engine.begin() as conn:
        # recommendations
        rec_cols = {col['name'] for col in inspector.get_columns("recommendations")}
        if "customer_comment" not in rec_cols:
            conn.execute(text("ALTER TABLE recommendations ADD COLUMN customer_comment TEXT NOT NULL DEFAULT ''"))

        # evaluations
        eval_cols = {col['name'] for col in inspector.get_columns("evaluations")}
        if "position_id" not in eval_cols:
            conn.execute(text("ALTER TABLE evaluations ADD COLUMN position_id INTEGER NOT NULL DEFAULT 1"))

        # ai_tasks
        ai_task_cols = {col['name'] for col in inspector.get_columns("ai_tasks")}
        if "created_by" not in ai_task_cols:
            conn.execute(text("ALTER TABLE ai_tasks ADD COLUMN created_by TEXT NOT NULL DEFAULT ''"))

        # companies
        comp_cols = {col['name'] for col in inspector.get_columns("companies")}
        for column, ddl in {
            "contact_email": "ALTER TABLE companies ADD COLUMN contact_email TEXT NOT NULL DEFAULT ''",
            "address": "ALTER TABLE companies ADD COLUMN address TEXT NOT NULL DEFAULT ''",
            "cooperation_period": "ALTER TABLE companies ADD COLUMN cooperation_period TEXT NOT NULL DEFAULT ''",
            "owner_user_id": "ALTER TABLE companies ADD COLUMN owner_user_id INTEGER",
        }.items():
            if column not in comp_cols:
                conn.execute(text(ddl))

        # projects
        proj_cols = {col['name'] for col in inspector.get_columns("projects")}
        for column, ddl in {
            "project_period": "ALTER TABLE projects ADD COLUMN project_period TEXT NOT NULL DEFAULT ''",
            "owner_user_id": "ALTER TABLE projects ADD COLUMN owner_user_id INTEGER",
        }.items():
            if column not in proj_cols:
                conn.execute(text(ddl))

        # users
        user_cols = {col['name'] for col in inspector.get_columns("users")}
        if "manager_user_id" not in user_cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN manager_user_id INTEGER"))

        # candidate_mail_records
        mail_cols = {col['name'] for col in inspector.get_columns("candidate_mail_records")}
        for column, ddl in {
            "recipient_email": "ALTER TABLE candidate_mail_records ADD COLUMN recipient_email TEXT NOT NULL DEFAULT ''",
            "mail_subject": "ALTER TABLE candidate_mail_records ADD COLUMN mail_subject TEXT NOT NULL DEFAULT ''",
            "mail_body": "ALTER TABLE candidate_mail_records ADD COLUMN mail_body TEXT NOT NULL DEFAULT ''",
            "attachment_name": "ALTER TABLE candidate_mail_records ADD COLUMN attachment_name TEXT NOT NULL DEFAULT ''",
            "sent_by": "ALTER TABLE candidate_mail_records ADD COLUMN sent_by TEXT NOT NULL DEFAULT ''",
            "status": "ALTER TABLE candidate_mail_records ADD COLUMN status TEXT NOT NULL DEFAULT '\u5df2\u53d1\u9001'",
        }.items():
            if column not in mail_cols:
                conn.execute(text(ddl))

        # candidate_follow_up_records
        follow_cols = {col['name'] for col in inspector.get_columns("candidate_follow_up_records")}
        for column, ddl in {
            "status": "ALTER TABLE candidate_follow_up_records ADD COLUMN status TEXT NOT NULL DEFAULT '\u5df2\u5f55\u7528'",
            "follow_up_time": "ALTER TABLE candidate_follow_up_records ADD COLUMN follow_up_time TIMESTAMP",
            "content": "ALTER TABLE candidate_follow_up_records ADD COLUMN content TEXT NOT NULL DEFAULT ''",
            "operator": "ALTER TABLE candidate_follow_up_records ADD COLUMN operator TEXT NOT NULL DEFAULT ''",
        }.items():
            if column not in follow_cols:
                conn.execute(text(ddl))

        # evaluation_levels — PG uses Base.metadata.create_all, no manual CREATE needed
        level_cols = {col['name'] for col in inspector.get_columns("evaluation_levels")} if "evaluation_levels" in inspector.get_table_names() else set()
        for column, ddl in {
            "name": "ALTER TABLE evaluation_levels ADD COLUMN name TEXT NOT NULL DEFAULT ''",
            "score": "ALTER TABLE evaluation_levels ADD COLUMN score INTEGER NOT NULL DEFAULT 5",
            "description": "ALTER TABLE evaluation_levels ADD COLUMN description TEXT NOT NULL DEFAULT ''",
            "color": "ALTER TABLE evaluation_levels ADD COLUMN color TEXT NOT NULL DEFAULT ''",
            "sort_order": "ALTER TABLE evaluation_levels ADD COLUMN sort_order INTEGER NOT NULL DEFAULT 0",
            "enabled": "ALTER TABLE evaluation_levels ADD COLUMN enabled BOOLEAN NOT NULL DEFAULT true",
        }.items():
            if column not in level_cols:
                conn.execute(text(ddl))

        # candidates
        cand_cols = {col['name'] for col in inspector.get_columns("candidates")}
        for column, ddl in {
            "gender": "ALTER TABLE candidates ADD COLUMN gender TEXT NOT NULL DEFAULT ''",
            "age": "ALTER TABLE candidates ADD COLUMN age INTEGER",
            "education": "ALTER TABLE candidates ADD COLUMN education TEXT NOT NULL DEFAULT ''",
            "experience_years": "ALTER TABLE candidates ADD COLUMN experience_years INTEGER",
            "expected_salary": "ALTER TABLE candidates ADD COLUMN expected_salary TEXT NOT NULL DEFAULT ''",
            "id_number": "ALTER TABLE candidates ADD COLUMN id_number TEXT NOT NULL DEFAULT ''",
            "tags": "ALTER TABLE candidates ADD COLUMN tags TEXT NOT NULL DEFAULT ''",
            "candidate_agent_id": "ALTER TABLE candidates ADD COLUMN candidate_agent_id TEXT",
            "birth_date": "ALTER TABLE candidates ADD COLUMN birth_date TEXT NOT NULL DEFAULT ''",
            "hukou_location": "ALTER TABLE candidates ADD COLUMN hukou_location TEXT NOT NULL DEFAULT ''",
            "onboard_cycle": "ALTER TABLE candidates ADD COLUMN onboard_cycle TEXT NOT NULL DEFAULT ''",
            "education_detail": "ALTER TABLE candidates ADD COLUMN education_detail TEXT NOT NULL DEFAULT ''",
            "certificates": "ALTER TABLE candidates ADD COLUMN certificates TEXT NOT NULL DEFAULT ''",
            "comprehensive_evaluation": "ALTER TABLE candidates ADD COLUMN comprehensive_evaluation TEXT NOT NULL DEFAULT ''",
            "work_history": "ALTER TABLE candidates ADD COLUMN work_history TEXT NOT NULL DEFAULT ''",
            "core_value": "ALTER TABLE candidates ADD COLUMN core_value TEXT NOT NULL DEFAULT ''",
            "job_status": "ALTER TABLE candidates ADD COLUMN job_status TEXT NOT NULL DEFAULT ''",
            "family_status": "ALTER TABLE candidates ADD COLUMN family_status TEXT NOT NULL DEFAULT ''",
            "salary_structure": "ALTER TABLE candidates ADD COLUMN salary_structure TEXT NOT NULL DEFAULT ''",
            "job_intention": "ALTER TABLE candidates ADD COLUMN job_intention TEXT NOT NULL DEFAULT ''",
            "project_history": "ALTER TABLE candidates ADD COLUMN project_history TEXT NOT NULL DEFAULT ''",
            "file_path": "ALTER TABLE candidates ADD COLUMN file_path TEXT NOT NULL DEFAULT ''",
            "owner_user_id": "ALTER TABLE candidates ADD COLUMN owner_user_id INTEGER",
        }.items():
            if column not in cand_cols:
                conn.execute(text(ddl))

        # positions
        pos_cols = {col['name'] for col in inspector.get_columns("positions")}
        for column, ddl in {
            "owner_user_id": "ALTER TABLE positions ADD COLUMN owner_user_id INTEGER",
            "age_requirement": "ALTER TABLE positions ADD COLUMN age_requirement TEXT NOT NULL DEFAULT ''",
            "education_requirement": "ALTER TABLE positions ADD COLUMN education_requirement TEXT NOT NULL DEFAULT ''",
            "experience_requirement": "ALTER TABLE positions ADD COLUMN experience_requirement TEXT NOT NULL DEFAULT ''",
            "description": "ALTER TABLE positions ADD COLUMN description TEXT NOT NULL DEFAULT ''",
        }.items():
            if column not in pos_cols:
                conn.execute(text(ddl))

        # candidate_tracking_events
        evt_cols = {col['name'] for col in inspector.get_columns("candidate_tracking_events")}
        for column, ddl in {
            "interview_round": "ALTER TABLE candidate_tracking_events ADD COLUMN interview_round TEXT NOT NULL DEFAULT ''",
            "screening_result": "ALTER TABLE candidate_tracking_events ADD COLUMN screening_result TEXT NOT NULL DEFAULT ''",
            "interview_date": "ALTER TABLE candidate_tracking_events ADD COLUMN interview_date TEXT NOT NULL DEFAULT ''",
            "interviewer": "ALTER TABLE candidate_tracking_events ADD COLUMN interviewer TEXT NOT NULL DEFAULT ''",
            "interview_location": "ALTER TABLE candidate_tracking_events ADD COLUMN interview_location TEXT NOT NULL DEFAULT ''",
            "interview_requirements": "ALTER TABLE candidate_tracking_events ADD COLUMN interview_requirements TEXT NOT NULL DEFAULT ''",
            "interview_contact": "ALTER TABLE candidate_tracking_events ADD COLUMN interview_contact TEXT NOT NULL DEFAULT ''",
            "interview_result": "ALTER TABLE candidate_tracking_events ADD COLUMN interview_result TEXT NOT NULL DEFAULT '-'",
            "note": "ALTER TABLE candidate_tracking_events ADD COLUMN note TEXT NOT NULL DEFAULT ''",
            "employment_status": "ALTER TABLE candidate_tracking_events ADD COLUMN employment_status TEXT NOT NULL DEFAULT '待设置'",
        }.items():
            if column not in evt_cols:
                conn.execute(text(ddl))

        # salary_records
        sal_cols = {col['name'] for col in inspector.get_columns("salary_records")}
        for column, ddl in {
            "position_id": "ALTER TABLE salary_records ADD COLUMN position_id INTEGER",
            "interview_round": "ALTER TABLE salary_records ADD COLUMN interview_round TEXT NOT NULL DEFAULT ''",
            "position_name": "ALTER TABLE salary_records ADD COLUMN position_name TEXT NOT NULL DEFAULT ''",
            "company_name": "ALTER TABLE salary_records ADD COLUMN company_name TEXT NOT NULL DEFAULT ''",
            "agreed_salary": "ALTER TABLE salary_records ADD COLUMN agreed_salary TEXT NOT NULL DEFAULT ''",
            "welfare_desc": "ALTER TABLE salary_records ADD COLUMN welfare_desc TEXT NOT NULL DEFAULT ''",
            "onboard_cond": "ALTER TABLE salary_records ADD COLUMN onboard_cond TEXT NOT NULL DEFAULT ''",
            "candidate_accepted": "ALTER TABLE salary_records ADD COLUMN candidate_accepted TEXT NOT NULL DEFAULT ''",
            "operator": "ALTER TABLE salary_records ADD COLUMN operator TEXT NOT NULL DEFAULT ''",
        }.items():
            if column not in sal_cols:
                conn.execute(text(ddl))

        # export_records — 三个手写信息字段
        exp_cols = {col['name'] for col in inspector.get_columns("export_records")}
        for column, ddl in {
            "contract_no": "ALTER TABLE export_records ADD COLUMN contract_no TEXT NOT NULL DEFAULT ''",
            "project_no": "ALTER TABLE export_records ADD COLUMN project_no TEXT NOT NULL DEFAULT ''",
            "headhunter_position": "ALTER TABLE export_records ADD COLUMN headhunter_position TEXT NOT NULL DEFAULT ''",
        }.items():
            if column not in exp_cols:
                conn.execute(text(ddl))

        # candidate ownership transfers
        if "candidate_ownership_transfers" not in inspector.get_table_names():
            conn.execute(text(
                """
                CREATE TABLE candidate_ownership_transfers (
                    id SERIAL PRIMARY KEY,
                    candidate_id INTEGER NOT NULL,
                    from_user_id INTEGER,
                    to_user_id INTEGER NOT NULL,
                    reason TEXT NOT NULL DEFAULT '',
                    approved_by_id INTEGER,
                    status TEXT NOT NULL DEFAULT '待审批',
                    approved_at TIMESTAMP,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL
                )
                """
            ))


ensure_schema()


def _delete_recommendation_graph(db: Session, recommendation_ids: list[int]) -> None:
    if not recommendation_ids:
        return
    db.query(CandidateTrackingEvent).filter(CandidateTrackingEvent.recommendation_id.in_(recommendation_ids)).delete(synchronize_session=False)
    db.query(RecommendationFeedback).filter(RecommendationFeedback.recommendation_id.in_(recommendation_ids)).delete(synchronize_session=False)
    db.query(Delivery).filter(Delivery.recommendation_id.in_(recommendation_ids)).delete(synchronize_session=False)
    db.query(Recommendation).filter(Recommendation.id.in_(recommendation_ids)).delete(synchronize_session=False)


def _delete_position_graph(db: Session, position_ids: list[int]) -> None:
    if not position_ids:
        return
    recommendation_ids = [row[0] for row in db.query(Recommendation.id).filter(Recommendation.position_id.in_(position_ids)).all()]
    db.query(CandidateTrackingEvent).filter(CandidateTrackingEvent.position_id.in_(position_ids)).delete(synchronize_session=False)
    db.query(Evaluation).filter(Evaluation.position_id.in_(position_ids)).delete(synchronize_session=False)
    _delete_recommendation_graph(db, recommendation_ids)
    db.query(Position).filter(Position.id.in_(position_ids)).delete(synchronize_session=False)


def _resolve_salary_position_snapshot(db: Session, payload: schemas.SalaryRecordCreate) -> None:
    position_id = payload.position_id
    if position_id in (None, 0):
        return
    position = db.get(Position, int(position_id))
    if not position:
        raise HTTPException(status_code=404, detail="岗位不存在")
    project = position.project
    payload.position_id = position.id
    payload.position_name = position.name or ""
    payload.company_name = project.company.name if project and project.company else ""


def _delete_project_graph(db: Session, project_ids: list[int]) -> None:
    if not project_ids:
        return
    position_ids = [row[0] for row in db.query(Position.id).filter(Position.project_id.in_(project_ids)).all()]
    _delete_position_graph(db, position_ids)
    db.query(Project).filter(Project.id.in_(project_ids)).delete(synchronize_session=False)


@app.on_event("startup")
def startup() -> None:
    ensure_schema()
    seed_data()
    backfill_legacy_ownership()


def backfill_legacy_ownership() -> None:
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            return
        updated = db.query(Candidate).filter(Candidate.owner_user_id.is_(None)).update(
            {Candidate.owner_user_id: admin.id},
            synchronize_session=False,
        )
        if updated:
            db.add(AuditLog(
                actor="system",
                module="权限系统",
                action="回填历史候选人归属",
                target_type="candidate",
                target_id="legacy",
                result="成功",
                detail=f"已将 {updated} 条历史候选人归属回填为 admin",
            ))
        db.commit()
    finally:
        db.close()


def require_user(db: Session = Depends(get_db), authorization: str | None = Header(default=None)):
    return get_current_user(db, authorization)


def require_admin_user(user: User = Depends(require_user)):
    return security.require_admin(user)


def enforce_candidate_access(db: Session, user: User, candidate: Candidate) -> None:
    if not security.can_access_scope(db, user, "candidate", candidate.id):
        raise HTTPException(status_code=403, detail="无权访问该候选人")


def enforce_position_access(db: Session, user: User, position_id: int) -> None:
    if not security.can_access_scope(db, user, "position", position_id):
        raise HTTPException(status_code=403, detail="无权访问该岗位")


def enforce_project_access(db: Session, user: User, project_id: int) -> None:
    if not security.can_access_scope(db, user, "project", project_id):
        raise HTTPException(status_code=403, detail="无权访问该项目")


def enforce_company_access(db: Session, user: User, company_id: int) -> None:
    if not security.can_access_scope(db, user, "company", company_id):
        raise HTTPException(status_code=403, detail="无权访问该客户公司")


def can_access_recommendation(db: Session, user: User, recommendation: Recommendation) -> bool:
    return security.can_access_scope(db, user, "candidate", recommendation.candidate_id) or security.can_access_scope(db, user, "position", recommendation.position_id)


def enforce_recommendation_access(db: Session, user: User, recommendation: Recommendation) -> None:
    if not can_access_recommendation(db, user, recommendation):
        raise HTTPException(status_code=403, detail="无权访问该推荐记录")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "hr-platform"}


@app.get("/api/users", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    return crud.list_users(db)


@app.post("/api/users", response_model=schemas.UserOut)
def add_user(payload: schemas.UserCreate, db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    if payload.manager_user_id:
        manager = db.get(User, payload.manager_user_id)
        if not manager or not security.is_leader(manager):
            raise HTTPException(status_code=400, detail="直属上级必须是组长")
    obj = crud.create_user(db, payload)
    crud.add_audit(db, user.username, "用户管理", "新增用户", "user", payload.username, detail=payload.full_name)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/api/users/{user_id}", response_model=schemas.UserOut)
def edit_user(user_id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    obj = db.get(User, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="用户不存在")
    if obj.id == user.id and payload.role is not None and payload.role != "超级管理员":
        raise HTTPException(status_code=400, detail="不能将当前管理员降权")
    if payload.manager_user_id:
        manager = db.get(User, payload.manager_user_id)
        if not manager or not security.is_leader(manager):
            raise HTTPException(status_code=400, detail="直属上级必须是组长")
    crud.update_user(db, obj, payload)
    crud.add_audit(db, user.username, "用户管理", "编辑用户", "user", str(user_id), detail=obj.username)
    db.commit()
    db.refresh(obj)
    return obj


@app.post("/api/users/{user_id}/toggle", response_model=schemas.UserOut)
def toggle_user(user_id: int, db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    obj = db.get(User, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="用户不存在")
    obj.is_active = not obj.is_active
    crud.add_audit(db, user.username, "用户管理", "切换用户状态", "user", str(user_id), detail=obj.username)
    db.commit()
    db.refresh(obj)
    return obj


@app.post("/api/users/{user_id}/reset-password", response_model=schemas.UserOut)
def reset_user_password(user_id: int, payload: schemas.UserResetPassword, db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    obj = db.get(User, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="用户不存在")
    crud.reset_user_password(db, obj, payload)
    crud.add_audit(db, user.username, "用户管理", "重置用户密码", "user", str(user_id), detail=obj.username)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/roles", response_model=list[schemas.RoleOut])
def get_roles(db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    return crud.list_roles(db)


@app.post("/api/roles", response_model=schemas.RoleOut)
def add_role(payload: schemas.RoleCreate, db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    obj = crud.create_role(db, payload)
    crud.add_audit(db, user.username, "角色管理", "新增角色", "role", payload.code, detail=payload.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/api/roles/{role_id}", response_model=schemas.RoleOut)
def edit_role(role_id: int, payload: schemas.RoleUpdate, db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    obj = db.get(Role, role_id)
    if not obj:
        raise HTTPException(status_code=404, detail="角色不存在")
    crud.update_role(db, obj, payload)
    crud.add_audit(db, user.username, "角色管理", "编辑角色", "role", str(role_id), detail=obj.code)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/api/roles/{role_id}")
def remove_role(role_id: int, db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    obj = db.get(Role, role_id)
    if not obj:
        raise HTTPException(status_code=404, detail="角色不存在")
    if obj.code in {"ADMIN", "LEADER", "OPERATOR"}:
        raise HTTPException(status_code=400, detail="预置角色不可删除")
    linked_users = db.query(User).filter(User.role == obj.name).count()
    if linked_users:
        raise HTTPException(status_code=400, detail="该角色仍有关联用户，无法删除")
    db.delete(obj)
    crud.add_audit(db, user.username, "角色管理", "删除角色", "role", str(role_id), detail=obj.code)
    db.commit()
    return {"ok": True}


@app.post("/api/roles/{role_id}/toggle", response_model=schemas.RoleOut)
def toggle_role(role_id: int, db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    obj = db.get(Role, role_id)
    if not obj:
        raise HTTPException(status_code=404, detail="角色不存在")
    obj.description = obj.description if obj.description else "已切换"
    crud.add_audit(db, user.username, "角色管理", "切换角色状态", "role", str(role_id), detail=obj.code)
    db.commit()
    db.refresh(obj)
    return obj


@app.post("/api/auth/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if not security.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    crud.add_audit(db, user.username, "认证登录", "用户登录", "user", str(user.id), detail=user.username)
    db.commit()
    return schemas.TokenResponse(access_token=security.issue_user_token(user))


@app.post("/api/auth/logout")
def logout(user: User = Depends(require_user), db: Session = Depends(get_db)):
    crud.add_audit(db, user.username, "认证登录", "用户退出", "user", str(user.id), detail=user.username)
    db.commit()
    return {"ok": True}


@app.get("/api/me", response_model=schemas.CurrentUser)
def me(user: User = Depends(require_user), db: Session = Depends(get_db)):
    role_code = security.get_role_code(user.role)
    permissions = [
        item.permission_key
        for item in db.query(RolePermission)
        .filter(RolePermission.role_code == role_code, RolePermission.enabled.is_(True))
        .all()
    ]
    if security.is_admin(user) and "all" not in permissions:
        permissions.append("all")
    return schemas.CurrentUser(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        permissions=permissions,
        manager_user_id=user.manager_user_id,
    )


@app.get("/api/dashboard/summary", response_model=schemas.DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db), user: User = Depends(require_user)):
    return schemas.DashboardSummary(**crud.dashboard_summary(db))


@app.get("/api/dashboard/todos", response_model=list[schemas.DashboardTodoOut])
def dashboard_todos(db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.dashboard_todos(db)


@app.get("/api/audit-logs", response_model=list[schemas.AuditLogOut])
def audit_logs(
    limit: int = Query(default=50, ge=1, le=500),
    actor: str | None = Query(default=None),
    module: str | None = Query(default=None),
    action: str | None = Query(default=None),
    target_type: str | None = Query(default=None),
    result: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(require_admin_user),
):
    return crud.list_recent_audit_logs(
        db,
        limit=limit,
        actor=actor,
        module=module,
        action=action,
        target_type=target_type,
        result=result,
        keyword=keyword,
        date_from=date_from,
        date_to=date_to,
    )


@app.get("/api/companies", response_model=list[schemas.CompanyOut])
def list_companies(db: Session = Depends(get_db), user: User = Depends(require_user)):
    items = db.query(Company).order_by(Company.created_at.desc()).all()
    if security.is_admin(user):
        return items
    return [item for item in items if security.can_access_scope(db, user, "company", item.id)]


@app.post("/api/companies", response_model=schemas.CompanyOut)
def add_company(payload: schemas.CompanyCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    if not payload.owner_user_id:
        payload.owner_user_id = user.id
    elif not security.is_admin(user):
        payload.owner_user_id = user.id
    obj = crud.create_company(db, payload)
    crud.add_audit(db, user.username, "客户公司管理", "创建客户公司", "company", "new", detail=payload.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/api/companies/{company_id}", response_model=schemas.CompanyOut)
def edit_company(company_id: int, payload: schemas.CompanyUpdate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(Company, company_id)
    if not obj:
        raise HTTPException(status_code=404, detail="客户公司不存在")
    if not security.is_admin(user):
        enforce_company_access(db, user, company_id)
    crud.update_company(db, obj, payload)
    crud.add_audit(db, user.username, "客户公司管理", "更新客户公司", "company", str(company_id), detail=obj.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.post("/api/companies/{company_id}/toggle", response_model=schemas.CompanyOut)
def toggle_company(company_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(Company, company_id)
    if not obj:
        raise HTTPException(status_code=404, detail="客户公司不存在")
    if not security.is_admin(user):
        enforce_company_access(db, user, company_id)
    status_cycle = {"招聘中": "空闲", "空闲": "失效", "失效": "招聘中"}
    obj.status = status_cycle.get(obj.status, "招聘中")
    crud.add_audit(db, user.username, "客户公司管理", "切换客户状态", "company", str(company_id), detail=obj.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/api/companies/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(Company, company_id)
    if not obj:
        raise HTTPException(status_code=404, detail="客户公司不存在")
    if not security.is_admin(user):
        enforce_company_access(db, user, company_id)
    name = obj.name
    project_ids = [row[0] for row in db.query(Project.id).filter(Project.company_id == company_id).all()]
    _delete_project_graph(db, project_ids)
    db.delete(obj)
    crud.add_audit(db, user.username, "客户公司管理", "删除客户公司", "company", str(company_id), detail=name)
    db.commit()
    return {"ok": True}


@app.get("/api/projects", response_model=list[schemas.ProjectOut])
def list_projects(company_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    query = db.query(Project, Company.name.label("company_name")).join(Company, Company.id == Project.company_id)
    if company_id is not None:
        query = query.filter(Project.company_id == company_id)
    rows = query.order_by(Project.created_at.desc()).all()
    result = []
    for project, company_name in rows:
        if not security.is_admin(user) and not security.can_access_scope(db, user, "project", project.id):
            continue
        item = schemas.ProjectOut.model_validate(project, from_attributes=True).model_dump()
        item["company_name"] = company_name or ""
        result.append(item)
    return result


@app.post("/api/projects", response_model=schemas.ProjectOut)
def add_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    if not security.is_admin(user):
        enforce_company_access(db, user, payload.company_id)
    if not payload.owner_user_id:
        payload.owner_user_id = user.id
    elif not security.is_admin(user):
        payload.owner_user_id = user.id
    obj = crud.create_project(db, payload)
    crud.add_audit(db, user.username, "项目管理", "创建项目", "project", "new", detail=payload.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/api/projects/{project_id}", response_model=schemas.ProjectOut)
def edit_project(project_id: int, payload: schemas.ProjectUpdate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(Project, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="项目不存在")
    if not security.is_admin(user):
        enforce_project_access(db, user, project_id)
    crud.update_project(db, obj, payload)
    crud.add_audit(db, user.username, "项目管理", "更新项目", "project", str(project_id), detail=obj.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.post("/api/projects/{project_id}/toggle", response_model=schemas.ProjectOut)
def toggle_project(project_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(Project, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="项目不存在")
    if not security.is_admin(user):
        enforce_project_access(db, user, project_id)
    status_cycle = {"招聘中": "招聘完毕", "招聘完毕": "招聘中止", "招聘中止": "招聘中"}
    obj.status = status_cycle.get(obj.status, "招聘中")
    crud.add_audit(db, user.username, "项目管理", "切换项目状态", "project", str(project_id), detail=obj.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(Project, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="项目不存在")
    if not security.is_admin(user):
        enforce_project_access(db, user, project_id)
    name = obj.name
    position_ids = [row[0] for row in db.query(Position.id).filter(Position.project_id == project_id).all()]
    _delete_position_graph(db, position_ids)
    db.delete(obj)
    crud.add_audit(db, user.username, "项目管理", "删除项目", "project", str(project_id), detail=name)
    db.commit()
    return {"ok": True}


@app.get("/api/positions", response_model=list[schemas.PositionOut])
def list_positions(project_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    query = db.query(Position)
    if project_id is not None:
        query = query.filter(Position.project_id == project_id)
    items = query.order_by(Position.created_at.desc()).all()
    if security.is_admin(user):
        return items
    return [item for item in items if security.can_access_scope(db, user, "position", item.id)]


@app.post("/api/positions", response_model=schemas.PositionOut)
def add_position(payload: schemas.PositionCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    enforce_project_access(db, user, payload.project_id)
    if not payload.owner_user_id:
        payload.owner_user_id = user.id
    elif not security.is_admin(user):
        payload.owner_user_id = user.id
    obj = crud.create_position(db, payload)
    crud.add_audit(db, user.username, "岗位管理", "创建岗位", "position", "new", detail=payload.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/api/positions/{position_id}", response_model=schemas.PositionOut)
def edit_position(position_id: int, payload: schemas.PositionUpdate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(Position, position_id)
    if not obj:
        raise HTTPException(status_code=404, detail="岗位不存在")
    if not security.is_admin(user):
        enforce_position_access(db, user, position_id)
    crud.update_position(db, obj, payload)
    crud.add_audit(db, user.username, "岗位管理", "更新岗位", "position", str(position_id), detail=obj.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.post("/api/positions/{position_id}/toggle", response_model=schemas.PositionOut)
def toggle_position(position_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(Position, position_id)
    if not obj:
        raise HTTPException(status_code=404, detail="岗位不存在")
    if not security.is_admin(user):
        enforce_position_access(db, user, position_id)
    status_cycle = {"待招": "招聘中", "招聘中": "已关闭", "已关闭": "待招"}
    obj.status = status_cycle.get(obj.status, "待招")
    crud.add_audit(db, user.username, "岗位管理", "切换岗位状态", "position", str(position_id), detail=obj.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/api/positions/{position_id}")
def delete_position(position_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(Position, position_id)
    if not obj:
        raise HTTPException(status_code=404, detail="岗位不存在")
    if not security.is_admin(user):
        enforce_position_access(db, user, position_id)
    name = obj.name
    _delete_position_graph(db, [position_id])
    crud.add_audit(db, user.username, "岗位管理", "删除岗位", "position", str(position_id), detail=name)
    db.commit()
    return {"ok": True}


@app.get("/api/candidates", response_model=list[schemas.CandidateOut])
def list_candidates(
    keyword: str | None = Query(default=None),
    city: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    items = crud.list_candidates(db, keyword=keyword, city=city, status=status)
    if security.is_admin(user):
        return items
    allowed_candidate_ids = set(security.accessible_candidate_ids(db, user))
    filtered = []
    for item in items:
        item_id = int(item.get("id") or 0)
        record_key = str(item.get("record_key") or "")
        if record_key.startswith("candidate:") and item_id in allowed_candidate_ids:
            filtered.append(item)
            continue
        if record_key.startswith("download:"):
            candidate_agent_id = item.get("candidate_agent_id")
            if candidate_agent_id:
                candidate = db.query(Candidate).filter(Candidate.candidate_agent_id == candidate_agent_id).first()
                if candidate and candidate.id in allowed_candidate_ids:
                    filtered.append(item)
    return filtered


@app.post("/api/candidates", response_model=schemas.CandidateOut)
def add_candidate(payload: schemas.CandidateCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    owner_user_id = payload.owner_user_id if security.is_admin(user) and payload.owner_user_id else user.id
    obj = crud.create_candidate(db, payload.model_copy(update={"owner_user_id": owner_user_id}))
    crud.add_audit(db, user.username, "候选人池", "创建候选人", "candidate", "new", detail=payload.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/candidates/{candidate_id}", response_model=schemas.CandidateOut)
def get_candidate(candidate_id: str, db: Session = Depends(get_db), user: User = Depends(require_user)):
    candidate = crud.ensure_local_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    enforce_candidate_access(db, user, candidate)
    return candidate


@app.post("/api/candidates/ai-search", response_model=schemas.CandidateAiSearchOut)
def ai_search_candidates(payload: schemas.CandidateAiSearchRequest, db: Session = Depends(get_db), user: User = Depends(require_user)):
    record_keys = [str(key).strip() for key in payload.record_keys if str(key).strip()]
    if not payload.job_description.strip():
        raise HTTPException(status_code=400, detail="请输入岗位描述")
    if not record_keys:
        raise HTTPException(status_code=400, detail="没有可检索的候选人")

    candidates: list[Candidate] = []
    seen_ids: set[int] = set()
    for key in record_keys:
        candidate = crud.ensure_local_candidate(db, key)
        if not candidate or candidate.id in seen_ids:
            continue
        seen_ids.add(candidate.id)
        candidates.append(candidate)

    if not candidates:
        raise HTTPException(status_code=404, detail="没有找到可参与 AI 检索的候选人")

    matched = ai_match_candidate(payload.job_description, candidates)
    candidate = matched.get("candidate")
    if not candidate:
        raise HTTPException(status_code=404, detail="未能匹配到候选人")

    crud.add_audit(
        db,
        user.username,
        "求职者数据池",
        f"AI检索({matched.get('match_method', 'ai')})",
        "candidate",
        str(candidate.id),
        detail=candidate.name,
    )
    db.commit()
    return {
        "candidate": schemas.CandidateOut.model_validate(candidate, from_attributes=True).model_dump(),
        "reason": matched.get("reason", ""),
        "match_method": matched.get("match_method", "ai"),
        "examined_count": matched.get("examined_count", len(candidates)),
    }


@app.get("/api/search-presets", response_model=list[schemas.SearchPresetOut])
def get_search_presets(db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_search_presets(db)


@app.post("/api/search-presets", response_model=schemas.SearchPresetOut)
def add_search_preset(payload: schemas.SearchPresetCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_search_preset(db, payload)
    crud.add_audit(db, user.username, "候选人池", "保存快捷搜索", "search_preset", payload.name, detail=payload.keyword)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/api/candidates/{candidate_id}", response_model=schemas.CandidateOut)
def edit_candidate(candidate_id: str, payload: schemas.CandidateUpdate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    candidate = crud.ensure_local_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    enforce_candidate_access(db, user, candidate)
    crud.update_candidate(db, candidate, payload)
    crud.add_audit(db, user.username, "候选人池", "更新候选人", "candidate", str(candidate.id), detail=candidate.name)
    db.commit()
    db.refresh(candidate)
    return candidate


@app.post("/api/candidates/{candidate_id}/lock", response_model=schemas.CandidateOut)
def lock_candidate(candidate_id: str, db: Session = Depends(get_db), user: User = Depends(require_user)):
    candidate = crud.ensure_local_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    enforce_candidate_access(db, user, candidate)
    candidate.owner_user_id = user.id
    crud.lock_candidate(db, candidate, True)
    crud.add_audit(db, user.username, "候选人跟踪", "锁定候选人", "candidate", str(candidate.id), detail=candidate.name)
    db.commit()
    db.refresh(candidate)
    return candidate


@app.post("/api/candidates/{candidate_id}/release", response_model=schemas.CandidateOut)
def release_candidate(candidate_id: str, db: Session = Depends(get_db), user: User = Depends(require_user)):
    candidate = crud.ensure_local_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    if not security.is_admin(user) and candidate.owner_user_id not in (None, user.id):
        raise HTTPException(status_code=403, detail="仅归属人可释放该候选人")
    crud.lock_candidate(db, candidate, False)
    candidate.owner_user_id = None
    crud.add_audit(db, user.username, "候选人跟踪", "释放候选人", "candidate", str(candidate.id), detail=candidate.name)
    db.commit()
    db.refresh(candidate)
    return candidate


@app.get("/api/candidate-ownership-transfers", response_model=list[schemas.CandidateOwnershipTransferOut])
def list_candidate_ownership_transfers(candidate_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    return crud.list_candidate_ownership_transfers(db, candidate_id=candidate_id)


@app.post("/api/candidate-ownership-transfers", response_model=schemas.CandidateOwnershipTransferOut)
def add_candidate_ownership_transfer(payload: schemas.CandidateOwnershipTransferCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    candidate = crud.ensure_local_candidate(db, payload.candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    enforce_candidate_access(db, user, candidate)
    obj = crud.create_candidate_ownership_transfer(
        db,
        schemas.CandidateOwnershipTransferCreate(candidate_id=candidate.id, to_user_id=payload.to_user_id, reason=payload.reason),
    )
    obj.from_user_id = candidate.owner_user_id
    crud.add_audit(db, user.username, "候选人权限", "创建候选人转派", "candidate_transfer", str(candidate.id), detail=payload.reason)
    db.commit()
    db.refresh(obj)
    return obj


@app.post("/api/candidate-ownership-transfers/{transfer_id}/approve", response_model=schemas.CandidateOwnershipTransferOut)
def approve_candidate_ownership_transfer(transfer_id: int, payload: schemas.CandidateOwnershipTransferApprove, db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    record = db.get(CandidateOwnershipTransfer, transfer_id)
    if not record:
        raise HTTPException(status_code=404, detail="转派记录不存在")
    obj = crud.approve_candidate_ownership_transfer(db, record, approved_by_id=payload.approved_by_id or user.id)
    crud.add_audit(db, user.username, "候选人权限", "审批候选人转派", "candidate_transfer", str(record.candidate_id), detail=record.reason)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/candidate-tracking-events", response_model=list[schemas.CandidateTrackingEventOut])
def list_candidate_tracking_events(candidate_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_tracking_events(db, candidate_id=candidate_id)


@app.post("/api/candidate-tracking-events", response_model=schemas.CandidateTrackingEventOut)
def add_candidate_tracking_event(payload: schemas.CandidateTrackingEventCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    from .crud import ensure_local_candidate
    candidate = ensure_local_candidate(db, payload.candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    payload.candidate_id = candidate.id
    enforce_candidate_access(db, user, candidate)
    
    if not payload.operator:
        payload.operator = user.full_name or user.username
        
    obj = crud.create_tracking_event(db, payload)
    crud.add_audit(db, user.username, "候选人跟踪", payload.event_type, "candidate_tracking_event", str(candidate.id), detail=payload.interview_round)
    db.commit()
    db.refresh(obj)
    return obj


@app.put("/api/candidate-tracking-events/{event_id}", response_model=schemas.CandidateTrackingEventOut)
def update_candidate_tracking_event(event_id: int, payload: schemas.CandidateTrackingEventCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.get_tracking_event(db, event_id)
    if not obj:
        raise HTTPException(status_code=404, detail="面试记录不存在")
    
    from .crud import ensure_local_candidate
    candidate = ensure_local_candidate(db, payload.candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    payload.candidate_id = candidate.id
    enforce_candidate_access(db, user, candidate)
    
    if not payload.operator:
        payload.operator = user.full_name or user.username
        
    updated_obj = crud.update_tracking_event(db, obj, payload)
    crud.add_audit(db, user.username, "候选人跟踪", payload.event_type, "candidate_tracking_event", str(candidate.id), detail=f"编辑: {payload.interview_round}")
    db.commit()
    db.refresh(updated_obj)
    return updated_obj


@app.delete("/api/candidate-tracking-events/{event_id}")
def delete_candidate_tracking_event(event_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.get_tracking_event(db, event_id)
    if not obj:
        raise HTTPException(status_code=404, detail="面试记录不存在")
    enforce_candidate_access(db, user, obj.candidate)
        
    candidate_id = obj.candidate_id
    interview_round = obj.interview_round
    crud.delete_tracking_event(db, obj)
    crud.add_audit(db, user.username, "候选人跟踪", "删除记录", "candidate_tracking_event", str(candidate_id), detail=f"删除: {interview_round}")
    db.commit()
    return {"success": True, "message": "面试记录删除成功"}


@app.get("/api/interview-records", response_model=list[schemas.InterviewRecordOut])
def list_interview_records(candidate_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_interview_records(db, candidate_id=candidate_id)


@app.post("/api/interview-records", response_model=schemas.InterviewRecordOut)
def add_interview_record(payload: schemas.InterviewRecordCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_interview_record(db, payload)
    crud.add_audit(db, user.username, "候选人跟踪", "新增面试记录", "interview_record", str(payload.candidate_id), detail=payload.round_name)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/salary-records", response_model=list[schemas.SalaryRecordOut])
def list_salary_records(candidate_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_salary_records(db, candidate_id=candidate_id)


@app.post("/api/salary-records", response_model=schemas.SalaryRecordOut)
def add_salary_record(payload: schemas.SalaryRecordCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    candidate = crud.ensure_local_candidate(db, payload.candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    payload.candidate_id = candidate.id
    _resolve_salary_position_snapshot(db, payload)
    if not payload.operator:
        payload.operator = user.username
    
    # 支持添加多条薪资/福利/入职条件跟踪记录
    obj = crud.create_salary_record(db, payload)
    action = "新增薪资记录"
    
    crud.add_audit(db, user.username, "候选人跟踪", action, "salary_record", str(candidate.id), detail=payload.interview_round or "薪资记录")
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/api/salary-records/{record_id}", response_model=schemas.SalaryRecordOut)
def edit_salary_record(record_id: int, payload: schemas.SalaryRecordCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    from .models import SalaryRecord
    record = db.get(SalaryRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="薪资记录不存在")
    
    # 校验：如果数据库表中已经记录了轮次，则直接使用，不允许修改
    if record.interview_round and payload.interview_round and record.interview_round != payload.interview_round:
        payload.interview_round = record.interview_round

    if payload.position_id in (None, 0):
        payload.position_id = record.position_id
    _resolve_salary_position_snapshot(db, payload)
        
    if not payload.operator:
        payload.operator = user.username
        
    obj = crud.update_salary_record(db, record, payload)
    crud.add_audit(db, user.username, "候选人跟踪", "更新薪资记录", "salary_record", str(record.candidate_id), detail=payload.interview_round or "薪资记录")
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/api/salary-records/{record_id}")
def delete_salary_record(record_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    from .models import SalaryRecord
    record = db.get(SalaryRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="薪资记录不存在")
    db.delete(record)
    crud.add_audit(db, user.username, "候选人跟踪", "删除薪资记录", "salary_record", str(record.candidate_id), detail=record.interview_round or "薪资记录")
    db.commit()
    return {"success": True}


@app.get("/api/employment-records", response_model=list[schemas.EmploymentRecordOut])
def list_employment_records(candidate_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_employment_records(db, candidate_id=candidate_id)


@app.post("/api/employment-records", response_model=schemas.EmploymentRecordOut)
def add_employment_record(payload: schemas.EmploymentRecordCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    candidate = crud.ensure_local_candidate(db, payload.candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    payload.candidate_id = candidate.id
    # Upsert：同一候选人已有入职记录则更新，否则新建
    existing = crud.list_employment_records(db, candidate_id=candidate.id)
    if existing:
        obj = crud.update_employment_record(db, existing[0], payload)
        action = "更新入职记录"
    else:
        obj = crud.create_employment_record(db, payload)
        action = "新增入职记录"
        
    # 联动更新候选人跟踪表（面试记录）的最新一条记录的入职状态
    from .models import CandidateTrackingEvent
    latest_event = db.query(CandidateTrackingEvent).filter(
        CandidateTrackingEvent.candidate_id == candidate.id
    ).order_by(CandidateTrackingEvent.created_at.desc()).first()
    if latest_event:
        latest_event.employment_status = payload.status
        db.add(latest_event)
        
    # 联动更新候选人自身状态
    candidate.status = "已录用" if payload.status == "已入职" else "未锁定"
    db.add(candidate)
    
    crud.add_audit(db, user.username, "候选人跟踪", action, "employment_record", str(candidate.id), detail=payload.status)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/api/employment-records/{record_id}", response_model=schemas.EmploymentRecordOut)
def edit_employment_record(record_id: int, payload: schemas.EmploymentRecordCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    from .models import EmploymentRecord
    record = db.get(EmploymentRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="入职记录不存在")
    obj = crud.update_employment_record(db, record, payload)
    crud.add_audit(db, user.username, "候选人跟踪", "更新入职记录", "employment_record", str(record.candidate_id), detail=payload.status)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/candidate-follow-up-records", response_model=list[schemas.CandidateFollowUpRecordOut])
def list_candidate_follow_up_records(candidate_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_candidate_follow_up_records(db, candidate_id=candidate_id)


@app.post("/api/candidate-follow-up-records", response_model=schemas.CandidateFollowUpRecordOut)
def add_candidate_follow_up_record(payload: schemas.CandidateFollowUpRecordCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    candidate = crud.ensure_local_candidate(db, payload.candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    payload.candidate_id = candidate.id
    obj = crud.create_candidate_follow_up_record(db, payload)
    crud.add_audit(db, user.username, "候选人跟踪", "新增随访记录", "candidate_follow_up_record", str(candidate.id), detail=payload.content[:32])
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/candidate-notes", response_model=list[schemas.CandidateNoteOut])
def list_candidate_notes(candidate_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    if candidate_id is not None:
        candidate = crud.ensure_local_candidate(db, candidate_id)
        if candidate:
            enforce_candidate_access(db, user, candidate)
    return crud.list_candidate_notes(db, candidate_id=candidate_id)


@app.post("/api/candidate-notes", response_model=schemas.CandidateNoteOut)
def add_candidate_note(payload: schemas.CandidateNoteCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    candidate = crud.ensure_local_candidate(db, payload.candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    payload.candidate_id = candidate.id
    enforce_candidate_access(db, user, candidate)
    obj = crud.create_candidate_note(db, payload)
    crud.add_audit(db, user.username, "候选人跟踪", "新增备注记录", "candidate_note", str(candidate.id), detail=payload.content[:32])
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/candidate-mail-records", response_model=list[schemas.CandidateMailRecordOut])
def list_candidate_mail_records(candidate_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    if candidate_id is not None:
        candidate = crud.ensure_local_candidate(db, candidate_id)
        if candidate:
            enforce_candidate_access(db, user, candidate)
    return crud.list_candidate_mail_records(db, candidate_id=candidate_id)


@app.post("/api/candidate-mail-records", response_model=schemas.CandidateMailRecordOut)
def add_candidate_mail_record(payload: schemas.CandidateMailRecordCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    candidate = crud.ensure_local_candidate(db, payload.candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    payload.candidate_id = candidate.id
    enforce_candidate_access(db, user, candidate)
    obj = crud.create_candidate_mail_record(db, payload)
    crud.add_audit(db, user.username, "候选人跟踪", "发送邮件", "candidate_mail_record", str(candidate.id), detail=payload.mail_subject)
    db.commit()
    db.refresh(obj)
    return obj


@app.post("/api/recommendations", response_model=schemas.RecommendationOut)
def add_recommendation(payload: schemas.RecommendationCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    candidate = crud.ensure_local_candidate(db, payload.candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    enforce_candidate_access(db, user, candidate)
    enforce_position_access(db, user, payload.position_id)
    if candidate.locked:
        raise HTTPException(status_code=400, detail="候选人已锁定，无法重复推荐")
    obj = crud.create_recommendation(db, payload)
    crud.add_audit(db, user.username, "推荐交付", "创建推荐记录", "recommendation", "new", detail=str(payload.candidate_id))
    db.commit()
    db.refresh(obj)
    return obj


@app.post("/api/recommendations/batch", response_model=schemas.RecommendationBatchOut)
def add_batch_recommendations(payload: schemas.RecommendationBatchCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    record_keys = [str(key).strip() for key in payload.record_keys if str(key).strip()]
    if not record_keys:
        raise HTTPException(status_code=400, detail="没有待推荐的候选人")
    position = db.get(Position, payload.position_id)
    if not position:
        raise HTTPException(status_code=404, detail="岗位不存在")
    enforce_position_access(db, user, position.id)

    items: list[schemas.RecommendationBatchItem] = []
    processed_candidate_ids: set[int] = set()
    succeeded = 0
    skipped = 0
    failed = 0
    recommender = payload.recommender or user.username

    for record_key in record_keys:
        candidate = None
        try:
            candidate = crud.ensure_local_candidate(db, record_key)
            if not candidate:
                failed += 1
                items.append(schemas.RecommendationBatchItem(
                    record_key=record_key,
                    result="failed",
                    reason="候选人不存在",
                ))
                continue
            enforce_candidate_access(db, user, candidate)
            if candidate.id in processed_candidate_ids:
                skipped += 1
                items.append(schemas.RecommendationBatchItem(
                    record_key=record_key,
                    candidate_id=candidate.id,
                    candidate_name=candidate.name,
                    result="skipped",
                    reason="本批次已包含该候选人",
                ))
                continue
            processed_candidate_ids.add(candidate.id)
            if candidate.locked:
                skipped += 1
                items.append(schemas.RecommendationBatchItem(
                    record_key=record_key,
                    candidate_id=candidate.id,
                    candidate_name=candidate.name,
                    result="skipped",
                    reason="候选人已锁定",
                ))
                continue
            existing = db.query(Recommendation).filter(
                Recommendation.candidate_id == candidate.id,
                Recommendation.position_id == position.id,
            ).first()
            if existing:
                skipped += 1
                items.append(schemas.RecommendationBatchItem(
                    record_key=record_key,
                    candidate_id=candidate.id,
                    candidate_name=candidate.name,
                    result="skipped",
                    reason="候选人已推荐至该岗位",
                    recommendation_id=existing.id,
                ))
                continue

            recommendation_payload = schemas.RecommendationCreate(
                candidate_id=candidate.id,
                position_id=position.id,
                recommender=recommender,
                status=payload.status,
                feedback=payload.feedback,
            )
            recommendation = crud.create_recommendation(db, recommendation_payload)
            db.flush()
            crud.add_audit(
                db,
                user.username,
                "推荐交付",
                "批量创建推荐记录",
                "recommendation",
                str(recommendation.id),
                detail=f"候选人 {candidate.id} -> 岗位 {position.id}",
            )
            db.commit()
            db.refresh(recommendation)
            succeeded += 1
            items.append(schemas.RecommendationBatchItem(
                record_key=record_key,
                candidate_id=candidate.id,
                candidate_name=candidate.name,
                result="success",
                reason="推荐成功",
                recommendation_id=recommendation.id,
            ))
        except HTTPException as exc:
            db.rollback()
            failed += 1
            items.append(schemas.RecommendationBatchItem(
                record_key=record_key,
                candidate_id=candidate.id if candidate else None,
                candidate_name=candidate.name if candidate else "",
                result="failed",
                reason=str(exc.detail),
            ))
        except Exception:
            db.rollback()
            failed += 1
            items.append(schemas.RecommendationBatchItem(
                record_key=record_key,
                candidate_id=candidate.id if candidate else None,
                candidate_name=candidate.name if candidate else "",
                result="failed",
                reason="推荐处理失败",
            ))

    notification_id = None
    if succeeded:
        notification = Notification(
            user=user.username,
            title=f"批量推荐完成：{succeeded} 人",
            type="业务处理",
            read=False,
            target_path="./candidates.html",
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        notification_id = notification.id

    return schemas.RecommendationBatchOut(
        total=len(record_keys),
        succeeded=succeeded,
        skipped=skipped,
        failed=failed,
        items=items,
        notification_id=notification_id,
    )


@app.get("/api/recommendations", response_model=list[schemas.RecommendationOut])
def get_recommendations(candidate_id: int | None = Query(default=None), position_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    items = crud.list_recommendations(db, candidate_id=candidate_id, position_id=position_id)
    if security.is_admin(user):
        return items
    return [item for item in items if can_access_recommendation(db, user, item)]


@app.put("/api/recommendations/{recommendation_id}", response_model=schemas.RecommendationOut)
def update_recommendation(recommendation_id: int, payload: schemas.RecommendationUpdate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(Recommendation, recommendation_id)
    if not obj:
        raise HTTPException(status_code=404, detail="推荐记录不存在")
    enforce_recommendation_access(db, user, obj)
    for key, value in payload.model_dump(exclude_unset=True).items():
        if key == "status":
            valid_transitions = {
                "待推荐": ["已推荐", "淘汰"],
                "已推荐": ["面试中", "未录用", "淘汰", "客户已收", "客户未收", "安排面试", "拒绝"],
                "客户已收": ["安排面试", "拒绝"],
                "安排面试": ["已录用", "未录用", "淘汰"],
                "面试中": ["已录用", "未录用", "淘汰"],
                "已录用": [],
                "未录用": [],
                "淘汰": []
            }
            allowed = valid_transitions.get(obj.status, [])
            if allowed and value not in allowed:
                raise HTTPException(status_code=400, detail=f"无法从 {obj.status} 流转到 {value}")
        setattr(obj, key, value)
    crud.add_audit(db, user.username, "推荐交付", "更新推荐状态", "recommendation", str(recommendation_id), detail=obj.status)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/recommendation-feedbacks", response_model=list[schemas.RecommendationFeedbackOut])
def get_recommendation_feedbacks(recommendation_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    items = crud.list_recommendation_feedbacks(db, recommendation_id=recommendation_id)
    if security.is_admin(user):
        return items
    result = []
    for item in items:
        recommendation = db.get(Recommendation, item.recommendation_id)
        if recommendation and can_access_recommendation(db, user, recommendation):
            result.append(item)
    return result


@app.post("/api/recommendation-feedbacks", response_model=schemas.RecommendationFeedbackOut)
def add_recommendation_feedback(payload: schemas.RecommendationFeedbackCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    recommendation = db.get(Recommendation, payload.recommendation_id)
    if not recommendation:
        raise HTTPException(status_code=404, detail="推荐记录不存在")
    enforce_recommendation_access(db, user, recommendation)
    obj = crud.create_recommendation_feedback(db, payload)
    crud.add_audit(db, user.username, "推荐交付", "记录客户反馈", "recommendation_feedback", str(payload.recommendation_id), detail=payload.status)
    db.commit()
    db.refresh(obj)
    return obj





@app.post("/api/deliveries", response_model=schemas.DeliveryOut)
def add_delivery(payload: schemas.DeliveryCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    recommendation = db.get(Recommendation, payload.recommendation_id)
    if not recommendation:
        raise HTTPException(status_code=404, detail="推荐记录不存在")
    enforce_recommendation_access(db, user, recommendation)
    obj = crud.create_delivery(db, payload)
    crud.add_audit(db, user.username, "推荐交付", "创建交付记录", "delivery", "new", detail=str(payload.recommendation_id))
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/deliveries", response_model=list[schemas.DeliveryOut])
def get_deliveries(recommendation_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    items = crud.list_deliveries(db, recommendation_id=recommendation_id)
    if security.is_admin(user):
        return items
    result = []
    for item in items:
        recommendation = db.get(Recommendation, item.recommendation_id)
        if recommendation and can_access_recommendation(db, user, recommendation):
            result.append(item)
    return result


@app.get("/api/evaluations", response_model=list[schemas.EvaluationOut])
def get_evaluations(candidate_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_evaluations(db, candidate_id=candidate_id)


@app.post("/api/evaluations", response_model=schemas.EvaluationOut)
def add_evaluation(payload: schemas.EvaluationCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    candidate = crud.ensure_local_candidate(db, payload.candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    if not db.get(Position, payload.position_id):
        raise HTTPException(status_code=404, detail="岗位不存在")
    payload.candidate_id = candidate.id
    obj = crud.create_evaluation(db, payload)
    crud.add_audit(db, user.username, "评价体系", "新增评价", "evaluation", "new", detail=payload.grade)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/evaluation-levels", response_model=list[schemas.EvaluationLevelOut])
def get_evaluation_levels(db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_evaluation_levels(db)


@app.post("/api/evaluation-levels", response_model=schemas.EvaluationLevelOut)
def add_evaluation_level(payload: schemas.EvaluationLevelCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_evaluation_level(db, payload)
    crud.add_audit(db, user.username, "评价体系", "新增评价等级", "evaluation_level", payload.name, detail=str(payload.score))
    db.commit()
    db.refresh(obj)
    return obj


@app.put("/api/evaluation-levels/{level_id}", response_model=schemas.EvaluationLevelOut)
def update_evaluation_level(level_id: int, payload: schemas.EvaluationLevelCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(EvaluationLevel, level_id)
    if not obj:
        raise HTTPException(status_code=404, detail="评价等级不存在")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    crud.add_audit(db, user.username, "评价体系", "更新评价等级", "evaluation_level", str(level_id), detail=obj.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/api/evaluation-levels/{level_id}")
def delete_evaluation_level(level_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(EvaluationLevel, level_id)
    if not obj:
        raise HTTPException(status_code=404, detail="评价等级不存在")
    name = obj.name
    db.delete(obj)
    crud.add_audit(db, user.username, "评价体系", "删除评价等级", "evaluation_level", str(level_id), detail=name)
    db.commit()
    return {"ok": True}


@app.get("/api/tags", response_model=list[schemas.TagOut])
def get_tags(db: Session = Depends(get_db), user: User = Depends(require_user)):
    security.require_admin(user)
    return crud.list_tags(db)


@app.post("/api/tags", response_model=schemas.TagOut)
def add_tag(payload: schemas.TagCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    security.require_admin(user)
    obj = crud.create_tag(db, payload)
    crud.add_audit(db, user.username, "标签字典", "新增标签", "tag", "new", detail=payload.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/api/tags/{tag_id}", response_model=schemas.TagOut)
def edit_tag(tag_id: int, payload: schemas.TagUpdate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    security.require_admin(user)
    obj = db.get(TagDictionary, tag_id)
    if not obj:
        raise HTTPException(status_code=404, detail="标签不存在")
    crud.update_tag(db, obj, payload)
    crud.add_audit(db, user.username, "标签字典", "更新标签", "tag", str(tag_id), detail=obj.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/api/tags/{tag_id}")
def remove_tag(tag_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    security.require_admin(user)
    obj = db.get(TagDictionary, tag_id)
    if not obj:
        raise HTTPException(status_code=404, detail="标签不存在")
    crud.delete_tag(db, obj)
    crud.add_audit(db, user.username, "标签字典", "删除标签", "tag", str(tag_id), detail=obj.name)
    db.commit()
    return {"ok": True}


@app.get("/api/notifications", response_model=list[schemas.NotificationOut])
def get_notifications(
    type: str | None = Query(default=None),
    read: bool | None = Query(default=None),
    keyword: str | None = Query(default=None),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    items = crud.list_notifications(db, type=type, read=read, keyword=keyword, date_from=date_from, date_to=date_to)
    if security.is_admin(user):
        return items
    return [item for item in items if item.user in {user.username, user.full_name}]


@app.post("/api/notifications", response_model=schemas.NotificationOut)
def add_notification(payload: schemas.NotificationCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_notification(db, payload)
    crud.add_audit(db, user.username, "通知提醒", "新增通知", "notification", "new", detail=payload.title)
    db.commit()
    db.refresh(obj)
    return obj


@app.post("/api/notifications/{notification_id}/read", response_model=schemas.NotificationOut)
def read_notification(notification_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(Notification, notification_id)
    if not obj:
        raise HTTPException(status_code=404, detail="通知不存在")
    if not security.is_admin(user) and obj.user not in {user.username, user.full_name}:
        raise HTTPException(status_code=403, detail="无权访问该通知")
    crud.mark_notification_read(db, obj)
    crud.add_audit(db, user.username, "通知提醒", "已读通知", "notification", str(notification_id), detail=obj.title)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/api/notifications/batch-read")
def batch_read_notifications(payload: list[int], db: Session = Depends(get_db), user: User = Depends(require_user)):
    for notification_id in payload:
        obj = db.get(Notification, notification_id)
        if obj and not security.is_admin(user) and obj.user not in {user.username, user.full_name}:
            continue
        if obj and not obj.read:
            crud.mark_notification_read(db, obj)
    crud.add_audit(db, user.username, "通知提醒", "批量已读通知", "notification", "batch", detail=f"Count: {len(payload)}")
    db.commit()
    return {"ok": True}


@app.get("/api/warranty-rules", response_model=list[schemas.WarrantyRuleOut])
def get_warranty_rules(db: Session = Depends(get_db), user: User = Depends(require_user)):
    security.require_admin(user)
    return crud.list_warranty_rules(db)


@app.post("/api/warranty-rules", response_model=schemas.WarrantyRuleOut)
def add_warranty_rule(payload: schemas.WarrantyRuleCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    security.require_admin(user)
    obj = crud.create_warranty_rule(db, payload)
    crud.add_audit(db, user.username, "质保期管理", "新增质保规则", "warranty_rule", "new", detail=payload.scope)
    db.commit()
    db.refresh(obj)
    return obj


@app.put("/api/warranty-rules/{rule_id}", response_model=schemas.WarrantyRuleOut)
def update_warranty_rule(rule_id: int, payload: schemas.WarrantyRuleCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    security.require_admin(user)
    obj = db.get(WarrantyRule, rule_id)
    if not obj:
        raise HTTPException(status_code=404, detail="质保规则不存在")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    crud.add_audit(db, user.username, "质保期管理", "更新质保规则", "warranty_rule", str(rule_id), detail=obj.scope)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/api/warranty-rules/{rule_id}")
def delete_warranty_rule(rule_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    security.require_admin(user)
    obj = db.get(WarrantyRule, rule_id)
    if not obj:
        raise HTTPException(status_code=404, detail="质保规则不存在")
    scope = obj.scope
    db.delete(obj)
    crud.add_audit(db, user.username, "质保期管理", "删除质保规则", "warranty_rule", str(rule_id), detail=scope)
    db.commit()
    return {"ok": True}


@app.get("/api/analytics/summary")
def analytics_summary(db: Session = Depends(get_db), user: User = Depends(require_user)):
    summary = crud.dashboard_summary(db)
    recommendations = db.query(Recommendation).all()
    projects = db.query(Project, Company.name.label("company_name")).join(Company, Company.id == Project.company_id).all()
    if not security.is_admin(user):
        allowed_candidate_ids = set(security.accessible_candidate_ids(db, user))
        allowed_position_ids = {row[0] for row in db.query(Position.id).all() if security.can_access_scope(db, user, "position", row[0])}
        allowed_project_ids = {row[0] for row in db.query(Project.id).all() if security.can_access_scope(db, user, "project", row[0])}
        allowed_company_ids = {row[0] for row in db.query(Company.id).all() if security.can_access_scope(db, user, "company", row[0])}
        recommendations = [item for item in recommendations if item.candidate_id in allowed_candidate_ids or item.position_id in allowed_position_ids]
        projects = [(project, company_name) for project, company_name in projects if project.id in allowed_project_ids or project.company_id in allowed_company_ids]
        summary = {
            **summary,
            "candidate_count": len(allowed_candidate_ids),
            "company_count": len(allowed_company_ids),
            "project_count": len(allowed_project_ids),
            "position_count": len(allowed_position_ids),
            "recommendation_count": len(recommendations),
            "delivery_count": db.query(Delivery).filter(Delivery.recommendation_id.in_([r.id for r in recommendations] or [0])).count(),
        }
    recommender_stats: dict[str, dict[str, int]] = {}
    for recommendation in recommendations:
        key = recommendation.recommender or "未命名"
        bucket = recommender_stats.setdefault(key, {"total": 0, "active": 0})
        bucket["total"] += 1
        if recommendation.status in {"客户已收", "安排面试", "已录用"}:
            bucket["active"] += 1
    customer_stats: dict[str, dict[str, int]] = {}
    for project, company_name in projects:
        key = company_name or f"客户 {project.company_id}"
        bucket = customer_stats.setdefault(key, {"total": 0, "active": 0})
        bucket["total"] += 1
        if project.status != "招聘完毕":
            bucket["active"] += 1
    team_rankings = sorted(
        [{"name": name, **values} for name, values in recommender_stats.items()],
        key=lambda item: (item["total"], item["active"], item["name"]),
        reverse=True,
    )[:3]
    customer_rankings = sorted(
        [{"name": name, **values} for name, values in customer_stats.items()],
        key=lambda item: (item["active"], item["total"], item["name"]),
        reverse=True,
    )[:3]
    return {
        **summary,
        "evaluation_count": db.query(Evaluation).count(),
        "notification_count": db.query(Notification).count(),
        "tag_count": db.query(TagDictionary).count(),
        "warranty_rule_count": db.query(WarrantyRule).count(),
        "team_rankings": team_rankings,
        "customer_rankings": customer_rankings,
    }


@app.get("/api/recommendation-stats")
def recommendation_stats(
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    position_id: int | None = Query(default=None),
    operator: str | None = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    query = db.query(Recommendation)
    if position_id is not None:
        query = query.filter(Recommendation.position_id == position_id)
    if operator:
        query = query.filter(Recommendation.recommender == operator)
    if date_from is not None:
        query = query.filter(Recommendation.created_at >= date_from)
    if date_to is not None:
        query = query.filter(Recommendation.created_at <= date_to)
    rows = query.all()
    if not security.is_admin(user):
        rows = [row for row in rows if can_access_recommendation(db, user, row)]
    by_position: dict[int, dict[str, int]] = {}
    by_operator: dict[str, dict[str, int]] = {}
    for row in rows:
        pos = by_position.setdefault(row.position_id, {"recommendation": 0, "interview": 0, "delivery": 0})
        pos["recommendation"] += 1
        if row.status in {"客户已收", "安排面试", "已录用"}:
            pos["interview"] += 1
        if row.status == "已录用":
            pos["delivery"] += 1
        op = by_operator.setdefault(row.recommender or "未命名", {"recommendation": 0, "interview": 0, "delivery": 0})
        op["recommendation"] += 1
        if row.status in {"客户已收", "安排面试", "已录用"}:
            op["interview"] += 1
        if row.status == "已录用":
            op["delivery"] += 1
    positions = {p.id: p.name for p in db.query(Position).all()}
    return {
        "total": len(rows),
        "by_position": [{"position_id": pid, "position_name": positions.get(pid, f"岗位 {pid}"), **values} for pid, values in sorted(by_position.items(), key=lambda item: item[1]["recommendation"], reverse=True)],
        "by_operator": [{"name": name, **values} for name, values in sorted(by_operator.items(), key=lambda item: item[1]["recommendation"], reverse=True)],
    }


@app.get("/api/system-configs", response_model=list[schemas.SystemConfigOut])
def list_system_configs(db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_system_configs(db)


@app.post("/api/system-configs", response_model=schemas.SystemConfigOut)
def save_system_config(payload: schemas.SystemConfigCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.upsert_system_config(db, payload)
    crud.add_audit(db, user.username, "系统管理", "保存系统配置", "system_config", payload.key, detail=payload.value)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/email-config", response_model=schemas.EmailConfigOut | None)
def get_email_config(db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.get_email_config(db)


@app.post("/api/email-config", response_model=schemas.EmailConfigOut)
def save_email_config(payload: schemas.EmailConfigCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.save_email_config(db, payload)
    crud.add_audit(db, user.username, "系统管理", "保存邮件配置", "email_config", "global", detail=payload.host)
    db.commit()
    db.refresh(obj)
    return obj


@app.post("/api/email-config/test", response_model=schemas.EmailConfigTestResult)
def test_email_config(payload: schemas.EmailConfigCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    ok, message = crud.test_email_config(payload)
    crud.add_audit(db, user.username, "系统管理", "测试邮件配置", "email_config", "test", result="成功" if ok else "失败", detail=f"{payload.host}:{payload.port}")
    db.commit()
    return schemas.EmailConfigTestResult(ok=ok, message=message)


@app.get("/api/ai/tasks", response_model=list[schemas.AiTaskOut])
def list_ai_tasks(db: Session = Depends(get_db), user: User = Depends(require_user)):
    items = crud.list_ai_tasks(db)
    if security.is_admin(user):
        return items
    return [item for item in items if item.created_by in {user.username, user.full_name}]


@app.post("/api/ai/tasks", response_model=schemas.AiTaskOut)
def create_ai_task(payload: schemas.AiTaskCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_ai_task(db, payload)
    obj.created_by = user.username
    crud.add_audit(db, user.username, "AI能力中心", f"创建AI任务:{payload.task_type}", "ai_task", "new", detail=payload.input_text)
    notification_title = {
        "resume_parse": "AI简历解析完成",
        "jd_generate": "AI JD 生成完成",
        "candidate_match": "AI简历匹配完成",
        "resume_fetch": "AI简历抓取完成",
    }.get(payload.task_type, f"AI任务完成:{payload.task_type}")
    db.add(Notification(user=user.username, title=notification_title, type="AI通知", read=False, target_path="/src/pages/ai-center.html"))
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/role-permissions", response_model=list[schemas.RolePermissionOut])
def get_role_permissions(role_code: str | None = None, db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    return crud.list_role_permissions(db, role_code=role_code)


@app.post("/api/role-permissions", response_model=schemas.RolePermissionOut)
def upsert_role_permission(payload: schemas.RolePermissionCreate, db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    obj = crud.save_role_permission(db, payload)
    crud.add_audit(db, user.username, "权限管理", "保存功能权限", "role_permission", payload.role_code, detail=payload.permission_key)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/data-permissions", response_model=list[schemas.DataPermissionOut])
def get_data_permissions(user_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    return crud.list_data_permissions(db, user_id=user_id)


@app.post("/api/data-permissions", response_model=schemas.DataPermissionOut)
def upsert_data_permission(payload: schemas.DataPermissionCreate, db: Session = Depends(get_db), user: User = Depends(require_admin_user)):
    if payload.scope_type not in {"company", "project", "position"}:
        raise HTTPException(status_code=400, detail="数据权限范围仅支持 company/project/position")
    obj = crud.save_data_permission(db, payload)
    crud.add_audit(db, user.username, "权限管理", "保存数据权限", "data_permission", str(payload.user_id), detail=f"{payload.scope_type}:{payload.scope_id}")
    db.commit()
    db.refresh(obj)
    return obj
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=OPENROUTER_API_KEY,
    )

PROMPT_FILE_PATH = os.path.join(ROOT_DIR, "outputs", "resume_parsing_prompt.md")

def get_system_prompt() -> str:
    if os.path.exists(PROMPT_FILE_PATH):
        with open(PROMPT_FILE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "You are an expert HR recruitment assistant. Please parse the resume text and return structured candidate JSON."

def call_llm_for_json(resume_text: str) -> dict:
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "your_api_key_here":
         raise ValueError("OpenRouter API Key is not configured. Please check your .env file.")
         
    system_prompt = get_system_prompt()
    client = get_openai_client()
    
    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请解析以下简历文本并严格返回要求的 JSON 格式：\n\n{resume_text}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    
    raw_response = response.choices[0].message.content.strip()
    if raw_response.startswith("```json"):
        raw_response = raw_response[7:]
    elif raw_response.startswith("```"):
         raw_response = raw_response[3:]
    if raw_response.endswith("```"):
         raw_response = raw_response[:-3]
         
    return json.loads(raw_response.strip())


def _strip_json_fence(raw_response: str) -> str:
    text = raw_response.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def _truncate_text(value: str | None, limit: int = 240) -> str:
    text = (value or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "…"


def _candidate_ai_summary(candidate: Candidate) -> str:
    parts = [
        f"姓名：{candidate.name or ''}",
        f"当前职位：{candidate.current_title or ''}",
        f"城市：{candidate.city or ''}",
        f"年龄：{candidate.age or ''}",
        f"学历：{candidate.education or ''}",
        f"工作年限：{candidate.experience_years or ''}",
        f"期望薪资：{candidate.expected_salary or ''}",
        f"职位状态：{candidate.job_status or ''}",
        f"来源：{candidate.source or ''}",
        f"标签：{candidate.tags or ''}",
        f"核心价值：{_truncate_text(candidate.core_value, 180)}",
        f"综合评估：{_truncate_text(candidate.comprehensive_evaluation, 180)}",
        f"工作经历：{_truncate_text(candidate.work_history, 320)}",
        f"项目经历：{_truncate_text(candidate.project_history, 320)}",
        f"证书：{_truncate_text(candidate.certificates, 120)}",
        f"教育背景：{_truncate_text(candidate.education_detail, 160)}",
        f"求职意向：{_truncate_text(candidate.job_intention, 160)}",
    ]
    return "\n".join(parts)


def _tokenize_job_description(text: str) -> list[str]:
    tokens = []
    for token in re.findall(r"[\u4e00-\u9fffA-Za-z0-9#+.]+", text.lower()):
        token = token.strip(".,;:，。；：/\\()[]{}<>\"'“”‘’")
        if len(token) >= 2:
            tokens.append(token)
    return tokens


def _candidate_keyword_score(job_description: str, candidate: Candidate) -> int:
    candidate_text = " ".join([
        candidate.name or "",
        candidate.current_title or "",
        candidate.city or "",
        candidate.education or "",
        str(candidate.experience_years or ""),
        candidate.expected_salary or "",
        candidate.tags or "",
        candidate.core_value or "",
        candidate.comprehensive_evaluation or "",
        candidate.work_history or "",
        candidate.project_history or "",
        candidate.certificates or "",
        candidate.education_detail or "",
        candidate.job_intention or "",
    ]).lower()
    tokens = _tokenize_job_description(job_description)
    if not tokens:
        return 0
    score = 0
    for token in tokens:
        if token and token in candidate_text:
            score += 1
    return score


def _fallback_ai_match(job_description: str, candidates: list[Candidate]) -> dict:
    ranked = sorted(
        candidates,
        key=lambda item: (
            _candidate_keyword_score(job_description, item),
            int(item.experience_years or 0),
            item.age or 0,
            item.created_at.timestamp() if getattr(item, "created_at", None) else 0,
            item.id,
        ),
        reverse=True,
    )
    if not ranked:
        return {"candidate": None, "reason": "", "match_method": "fallback", "examined_count": 0}
    best = ranked[0]
    keywords = _tokenize_job_description(job_description)[:5]
    reason_bits = [f"命中关键词：{ '、'.join(keywords) }"] if keywords else []
    if best.current_title:
        reason_bits.append(f"当前职位为{best.current_title}")
    if best.work_history:
        reason_bits.append("工作经历与岗位要求有较强重合")
    return {
        "candidate": best,
        "reason": "；".join(reason_bits) or "基于基础筛选后的候选池规则匹配",
        "match_method": "fallback",
        "examined_count": len(candidates),
    }


def _call_llm_for_candidate_match(job_description: str, candidate_payloads: list[dict]) -> dict:
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "your_api_key_here":
        raise ValueError("OpenRouter API Key is not configured. Please check your .env file.")

    system_prompt = (
        "你是资深猎头匹配专家。"
        "你只允许在给定候选人列表中选出最匹配岗位描述的一位。"
        "请综合岗位描述、工作经历、项目经历、证书、综合评价和求职意向进行判断。"
        "必须返回严格 JSON，对象结构为："
        '{"candidate_id": 1, "reason": "简短说明", "matched_points": ["..."], "risk_points": ["..."], "confidence": 0.0}'
        "其中 candidate_id 必须是候选人列表中的 id。"
    )
    client = get_openai_client()
    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "job_description": job_description,
                        "candidates": candidate_payloads,
                    },
                    ensure_ascii=False,
                ),
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    raw_response = response.choices[0].message.content or "{}"
    parsed = json.loads(_strip_json_fence(raw_response))
    if not isinstance(parsed, dict):
        raise ValueError("AI 返回格式无效")
    return parsed


def ai_match_candidate(job_description: str, candidates: list[Candidate]) -> dict:
    if not candidates:
        return {"candidate": None, "reason": "", "match_method": "empty", "examined_count": 0}

    ranked = sorted(
        candidates,
        key=lambda item: (
            _candidate_keyword_score(job_description, item),
            int(item.experience_years or 0),
            item.created_at.timestamp() if getattr(item, "created_at", None) else 0,
            item.id,
        ),
        reverse=True,
    )
    shortlist = ranked[: min(20, len(ranked))]
    candidate_map = {item.id: item for item in shortlist}
    payloads = [
        {
            "id": item.id,
            "name": item.name,
            "current_title": item.current_title,
            "city": item.city,
            "age": item.age,
            "education": item.education,
            "experience_years": item.experience_years,
            "source": item.source,
            "job_status": item.job_status,
            "summary": _candidate_ai_summary(item),
        }
        for item in shortlist
    ]

    try:
        result = _call_llm_for_candidate_match(job_description, payloads)
        candidate_id = result.get("candidate_id")
        try:
            candidate_id = int(candidate_id)
        except (TypeError, ValueError):
            candidate_id = None
        candidate = candidate_map.get(candidate_id)
        if not candidate:
            raise ValueError("AI 返回的候选人不在当前候选池中")
        reason = str(result.get("reason") or "").strip()
        if not reason:
            reason = "AI 已在当前基础筛选后的候选池中选出最匹配记录"
        return {
            "candidate": candidate,
            "reason": reason,
            "match_method": "ai",
            "examined_count": len(candidates),
        }
    except Exception:
        return _fallback_ai_match(job_description, candidates)

def parse_and_create_candidate(db: Session, full_path: str, save_name: str, username: str, owner_user_id: int | None = None) -> dict:
    text_content = ""
    with pdfplumber.open(full_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_content += page_text + "\n"
                
    if not text_content.strip():
        raise Exception("无法从PDF中提取出任何文本内容。")
        
    parsed_data = call_llm_for_json(text_content)
    candidate_name = parsed_data.get("name") or Path(full_path).stem
    candidate_name = candidate_name.strip()
    
    duplicate = db.query(Candidate).filter(Candidate.name == candidate_name).order_by(Candidate.created_at.desc()).first()
    if duplicate:
        return {"status": "duplicate", "candidate_name": candidate_name, "duplicate": duplicate}
        
    relative_file_path = f"data/resumes/imported/{save_name}"
    
    candidate = Candidate(
        name=candidate_name,
        phone=parsed_data.get("phone") or "",
        email=parsed_data.get("email") or "",
        gender=parsed_data.get("gender") or "",
        birth_date=parsed_data.get("birth_date") or "",
        age=parsed_data.get("age") or 0,
        city=parsed_data.get("city") or "",
        hukou_location=parsed_data.get("hukou_location") or "",
        family_status=parsed_data.get("family_status") or "",
        job_status=parsed_data.get("job_status") or "离职",
        onboard_cycle=parsed_data.get("onboard_cycle") or "",
        expected_salary=parsed_data.get("expected_salary") or "",
        job_intention=parsed_data.get("job_intention") or "",
        education=parsed_data.get("education") or "",
        experience_years=parsed_data.get("experience_years") or 0,
        current_title=parsed_data.get("current_title") or "",
        core_value=parsed_data.get("core_value") or "",
        certificates=parsed_data.get("certificates") or "",
        education_detail=parsed_data.get("education_detail") or "",
        work_history=parsed_data.get("work_history") or "",
        project_history=parsed_data.get("project_history") or "",
        file_path=relative_file_path,
        source="手工导入",
        status="未锁定",
        owner_user_id=owner_user_id,
    )
    db.add(candidate)
    db.flush()
    return {"status": "success", "candidate": candidate}

@app.post("/api/imports/smoke")
def import_smoke(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(require_user)):
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="目前只支持PDF格式的简历文件。")
        
    import_dir = os.path.join(ROOT_DIR, "recruit", "data", "resumes", "imported")
    os.makedirs(import_dir, exist_ok=True)
    
    timestamp = int(time.time())
    save_name = f"{timestamp}_{filename}"
    full_path = os.path.join(import_dir, save_name)
    
    with open(full_path, "wb") as f:
        f.write(file.file.read())
        
    try:
        result = parse_and_create_candidate(db, full_path, save_name, user.username, user.id)
        if result["status"] == "duplicate":
            duplicate = result["duplicate"]
            candidate_name = result["candidate_name"]
            import_record = crud.create_import_record(
                db,
                schemas.ImportRecordCreate(
                    file_name=filename,
                    imported_by=user.username,
                    imported_count=0,
                    failed_count=1,
                    status="复核",
                    note=f"检测到同名候选人：{candidate_name}，等待覆盖确认",
                ),
            )
            crud.add_audit(db, user.username, "简历导入", "导入简历复核", "candidate", str(duplicate.id), result="失败", detail=filename)
            db.commit()
            db.refresh(import_record)
            return {
                "imported": 0,
                "duplicate": schemas.CandidateOut.model_validate(duplicate, from_attributes=True).model_dump(),
                "import_record": schemas.ImportRecordOut.model_validate(import_record, from_attributes=True).model_dump()
            }
        else:
            candidate = result["candidate"]
            import_record = crud.create_import_record(
                db,
                schemas.ImportRecordCreate(
                    file_name=filename,
                    imported_by=user.username,
                    imported_count=1,
                    failed_count=0,
                    status="成功",
                    note=f"导入候选人 {candidate.name}"
                )
            )
            crud.add_audit(db, user.username, "简历导入", "导入简历", "candidate", str(candidate.id), detail=filename)
            db.commit()
            db.refresh(candidate)
            db.refresh(import_record)
            return {
                "imported": 1,
        "candidate": schemas.CandidateOut.model_validate(candidate, from_attributes=True).model_dump(),
                "import_record": schemas.ImportRecordOut.model_validate(import_record, from_attributes=True).model_dump()
            }
    except Exception as e:
        import_record = crud.create_import_record(
            db,
            schemas.ImportRecordCreate(
                file_name=filename,
                imported_by=user.username,
                imported_count=0,
                failed_count=1,
                status="失败",
                note=f"解析失败: {str(e)}"
            )
        )
        crud.add_audit(db, user.username, "简历导入", "导入解析失败", "candidate", "error", result="失败", detail=filename)
        db.commit()
        db.refresh(import_record)
        raise HTTPException(status_code=400, detail=f"简历导入解析失败: {str(e)}")


@app.post("/api/imports/batch")
def import_batch(files: list[UploadFile] = File(...), db: Session = Depends(get_db), user: User = Depends(require_user)):
    imported = 0
    duplicates = 0
    records = []
    candidates = []
    
    # 1. 校验所有的文件只能是 PDF
    for file in files:
        filename = file.filename or ""
        if not filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="目前只支持PDF格式的简历文件。")
            
    # 2. 遍历并保存和解析
    import_dir = os.path.join(ROOT_DIR, "recruit", "data", "resumes", "imported")
    os.makedirs(import_dir, exist_ok=True)
    
    for file in files:
        filename = file.filename or ""
        timestamp = int(time.time())
        save_name = f"{timestamp}_{filename}"
        full_path = os.path.join(import_dir, save_name)
        
        with open(full_path, "wb") as f:
            f.write(file.file.read())
            
        try:
            result = parse_and_create_candidate(db, full_path, save_name, user.username, user.id)
            if result["status"] == "duplicate":
                duplicates += 1
                duplicate = result["duplicate"]
                candidate_name = result["candidate_name"]
                import_record = crud.create_import_record(
                    db,
                    schemas.ImportRecordCreate(
                        file_name=filename,
                        imported_by=user.username,
                        imported_count=0,
                        failed_count=1,
                        status="复核",
                        note=f"检测到同名候选人：{candidate_name}，等待覆盖确认",
                    ),
                )
                crud.add_audit(db, user.username, "简历导入", "批量导入复核", "candidate", str(duplicate.id), result="失败", detail=filename)
                db.flush()
                records.append(schemas.ImportRecordOut.model_validate(import_record, from_attributes=True).model_dump())
            else:
                imported += 1
                candidate = result["candidate"]
                import_record = crud.create_import_record(
                    db,
                    schemas.ImportRecordCreate(
                        file_name=filename,
                        imported_by=user.username,
                        imported_count=1,
                        failed_count=0,
                        status="成功",
                        note=f"导入候选人 {candidate.name}",
                    ),
                )
                crud.add_audit(db, user.username, "简历导入", "批量导入简历", "candidate", str(candidate.id), detail=filename)
                db.flush()
                candidates.append(candidate)
                records.append(schemas.ImportRecordOut.model_validate(import_record, from_attributes=True).model_dump())
                
        except Exception as e:
            import_record = crud.create_import_record(
                db,
                schemas.ImportRecordCreate(
                    file_name=filename,
                    imported_by=user.username,
                    imported_count=0,
                    failed_count=1,
                    status="失败",
                    note=f"解析失败: {str(e)}",
                ),
            )
            crud.add_audit(db, user.username, "简历导入", "批量解析失败", "candidate", "error", result="失败", detail=filename)
            db.flush()
            records.append(schemas.ImportRecordOut.model_validate(import_record, from_attributes=True).model_dump())
            
    db.commit()
    for item in candidates:
        db.refresh(item)
    return {
        "imported": imported,
        "duplicates": duplicates,
        "import_records": records,
        "candidates": [schemas.CandidateOut.model_validate(item, from_attributes=True).model_dump() for item in candidates],
    }


@app.get("/api/import-records", response_model=list[schemas.ImportRecordOut])
def get_import_records(db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_import_records(db)


@app.get("/api/export-records", response_model=list[schemas.ExportRecordOut])
def get_export_records(candidate_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    items = crud.list_export_records(db, candidate_id=candidate_id)
    if security.is_admin(user):
        return items
    allowed_candidate_ids = set(security.accessible_candidate_ids(db, user))
    return [item for item in items if item.candidate_id in allowed_candidate_ids]


@app.post("/api/export-records", response_model=schemas.ExportRecordOut)
def add_export_record(payload: schemas.ExportRecordCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    candidate = db.query(Candidate).filter(Candidate.id == payload.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="未找到对应的候选人")
    enforce_candidate_access(db, user, candidate)
        
    project = None
    if payload.project_name:
        project = db.query(Project).filter(Project.name == payload.project_name).first()
        
    # 确定物理文件名：候选人名 + 时间戳 + ID，确保多人批量导出时文件名不冲突
    import time
    safe_candidate_name = "".join([c for c in (payload.candidate_name or "candidate") if c.isalnum() or c in ("-", "_")]).strip()
    if not safe_candidate_name:
        safe_candidate_name = "candidate"
    timestamp_suffix = str(int(time.time() * 1000))[-6:]  # 取毫秒级后 6 位，提高唯一性
    physical_filename = f"{safe_candidate_name}-{payload.candidate_id}-{timestamp_suffix}.pdf"
    
    # 创建 exports 目录
    exports_dir = os.path.join(ROOT_DIR, "exports")
    os.makedirs(exports_dir, exist_ok=True)
    file_path = os.path.join(exports_dir, physical_filename)
    
    # 运行 PDF 生成器
    from backend.app.pdf_generator import generate_resume_pdf
    try:
        generate_resume_pdf(
            candidate=candidate,
            company_name=payload.company_name,
            project_name=payload.project_name,
            position_name=payload.position_name,
            exported_by=user.username,
            output_path=file_path,
            project_id=project.id if project else None,
            contract_no=payload.contract_no,
            project_no=payload.project_no,
            headhunter_position=payload.headhunter_position,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF 生成失败: {str(e)}")
        
    display_name = f"{payload.candidate_name or '候选人'}-简历报告.pdf"
    payload.file_name = display_name
    payload.file_path = f"/exports/{physical_filename}"
    
    obj = crud.create_export_record(db, payload)
    crud.add_audit(db, user.username, "求职者数据池", "导出简历", "export_record", str(payload.candidate_id), detail=display_name)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/recruit/candidates")
def list_recruit_candidates(keyword: str | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    query = db.query(RecruitCandidateProfile)
    if keyword:
        query = query.filter(RecruitCandidateProfile.candidate_name.like(f"%{keyword}%"))
    profiles = query.order_by(RecruitCandidateProfile.updated_at.desc()).all()
    
    results = []
    for p in profiles:
        download = db.query(RecruitResumeDownload).filter(
            RecruitResumeDownload.candidate_agent_id == p.candidate_agent_id
        ).order_by(RecruitResumeDownload.created_at.desc()).first()
        
        results.append({
            "candidate_agent_id": p.candidate_agent_id,
            "candidate_name": p.candidate_name,
            "candidate_age": p.candidate_age,
            "candidate_education": p.candidate_education,
            "updated_at": p.updated_at,
            "job_title": download.job_title if download else "未知岗位",
            "file_path": download.file_path if download else "",
            "issuer_login_name": download.issuer_login_name if download else "",
            "created_at": download.created_at if download else ""
        })
    return results


RECRUIT_ACTIVITY_CODES = {"1w", "1m", "2m", "3m", "6m"}
RECRUIT_EDUCATION_CODES = {"high_school", "college", "bachelor", "master", "unlimited"}
RECRUIT_DAILY_GREET_LIMITS = {10, 20, 30, 40, 50}


def _format_recruit_time(value) -> str:
    if value is None:
        return ""
    return str(value)


def _recruit_employee_label(employee: RecruitEmployee | None) -> str:
    if not employee:
        return ""
    return employee.display_name or employee.login_name or ""


def _recruit_job_out(job: RecruitJobPosting, employee: RecruitEmployee | None = None) -> dict:
    return {
        "id": job.id,
        "employee_id": job.employee_id,
        "publisher_login": employee.login_name if employee else "",
        "publisher_name": _recruit_employee_label(employee),
        "job_title": job.job_title,
        "work_location": job.work_location,
        "age_min": job.age_min,
        "age_max": job.age_max,
        "education": job.education,
        "candidate_activity": job.candidate_activity or "1m",
        "daily_greet_limit": job.daily_greet_limit or 20,
        "search_keyword": job.search_keyword,
        "is_valid": "N" if str(job.is_valid or "Y").upper() == "N" else "Y",
        "created_at": _format_recruit_time(job.created_at),
    }


def _normalize_recruit_job_payload(payload, *, partial: bool = False) -> dict:
    raw = payload.model_dump(exclude_unset=partial)
    data = {}

    if "job_title" in raw or not partial:
        job_title = str(raw.get("job_title") or "").strip()
        if not job_title:
            raise HTTPException(status_code=400, detail="请填写岗位名称")
        if len(job_title) < 2 or len(job_title) > 80:
            raise HTTPException(status_code=400, detail="岗位名称长度需为 2-80 个字符")
        data["job_title"] = job_title

    if "work_location" in raw or not partial:
        data["work_location"] = str(raw.get("work_location") or "长春").strip() or "长春"

    has_age_min = "age_min" in raw
    has_age_max = "age_max" in raw
    if has_age_min or has_age_max or not partial:
        age_min = raw.get("age_min")
        age_max = raw.get("age_max")
        if age_min in ("", None):
            age_min = None
        if age_max in ("", None):
            age_max = None
        if (age_min is None) != (age_max is None):
            raise HTTPException(status_code=400, detail="年龄下限与上限需同时填写，或同时留空")
        if age_min is not None and age_max is not None:
            age_min = int(age_min)
            age_max = int(age_max)
            if age_min < 16 or age_max > 99 or age_min > age_max:
                raise HTTPException(status_code=400, detail="年龄须在 16-99 岁之间，且下限不能大于上限")
        data["age_min"] = age_min
        data["age_max"] = age_max

    if "education" in raw or not partial:
        education = raw.get("education")
        education = None if education in ("", None) else str(education).strip()
        if education and education not in RECRUIT_EDUCATION_CODES:
            raise HTTPException(status_code=400, detail="学历选项无效")
        data["education"] = education

    if "candidate_activity" in raw or not partial:
        activity = str(raw.get("candidate_activity") or "1m").strip()
        if activity not in RECRUIT_ACTIVITY_CODES:
            raise HTTPException(status_code=400, detail="候选人活跃时间选项无效")
        data["candidate_activity"] = activity

    if "daily_greet_limit" in raw or not partial:
        daily_greet_limit = int(raw.get("daily_greet_limit") or 20)
        if daily_greet_limit not in RECRUIT_DAILY_GREET_LIMITS:
            raise HTTPException(status_code=400, detail="每日打招呼次数须为 10、20、30、40 或 50")
        data["daily_greet_limit"] = daily_greet_limit

    if "search_keyword" in raw or not partial:
        search_keyword = raw.get("search_keyword")
        search_keyword = None if search_keyword in ("", None) else str(search_keyword).strip()[:30]
        data["search_keyword"] = search_keyword

    if "is_valid" in raw or not partial:
        data["is_valid"] = "N" if str(raw.get("is_valid") or "Y").strip().upper() == "N" else "Y"

    if "employee_id" in raw and raw.get("employee_id") not in ("", None):
        data["employee_id"] = int(raw["employee_id"])

    return data


def _resolve_recruit_employee(db: Session, user: User, requested_employee_id: int | None = None) -> RecruitEmployee:
    if requested_employee_id:
        employee = db.get(RecruitEmployee, requested_employee_id)
        if not employee:
            raise HTTPException(status_code=400, detail="指定的 Recruit 发布人不存在")
        return employee

    employee = db.query(RecruitEmployee).filter(RecruitEmployee.login_name == user.username).first()
    if employee:
        return employee

    employee = RecruitEmployee(
        login_name=user.username,
        password_hash="managed-by-hr-platform",
        display_name=user.full_name,
        is_admin=1 if security.is_admin(user) else 0,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    db.add(employee)
    db.flush()
    return employee


@app.get("/api/recruit/employees")
def list_recruit_employees(db: Session = Depends(get_db), user: User = Depends(require_user)):
    rows = db.query(RecruitEmployee).order_by(RecruitEmployee.id.asc()).all()
    return [
        {
            "id": item.id,
            "login_name": item.login_name,
            "display_name": item.display_name or "",
            "is_admin": item.is_admin,
            "created_at": _format_recruit_time(item.created_at),
            "updated_at": _format_recruit_time(item.updated_at),
        }
        for item in rows
    ]


@app.get("/api/recruit/job-postings")
def list_recruit_job_postings(db: Session = Depends(get_db), user: User = Depends(require_user)):
    rows = (
        db.query(RecruitJobPosting, RecruitEmployee)
        .outerjoin(RecruitEmployee, RecruitEmployee.id == RecruitJobPosting.employee_id)
        .order_by(RecruitJobPosting.id.desc())
        .all()
    )
    return {"jobs": [_recruit_job_out(job, employee) for job, employee in rows]}


@app.post("/api/recruit/job-postings")
def create_recruit_job_posting(payload: schemas.RecruitJobPostingCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    data = _normalize_recruit_job_payload(payload)
    employee = _resolve_recruit_employee(db, user, data.pop("employee_id", None))
    obj = RecruitJobPosting(employee_id=employee.id, created_at=datetime.now(timezone.utc).isoformat(), **data)
    db.add(obj)
    crud.add_audit(db, user.username, "Recruit岗位管理", "发布岗位", "recruit_job_posting", "new", detail=obj.job_title)
    db.commit()
    db.refresh(obj)
    return {"job": _recruit_job_out(obj, employee)}


@app.patch("/api/recruit/job-postings/{job_id}")
def update_recruit_job_posting(job_id: int, payload: schemas.RecruitJobPostingUpdate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(RecruitJobPosting, job_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Recruit 岗位不存在")
    data = _normalize_recruit_job_payload(payload, partial=True)
    employee = None
    if "employee_id" in data:
        employee = _resolve_recruit_employee(db, user, data.pop("employee_id"))
        obj.employee_id = employee.id
    for key, value in data.items():
        setattr(obj, key, value)
    crud.add_audit(db, user.username, "Recruit岗位管理", "更新岗位", "recruit_job_posting", str(job_id), detail=obj.job_title)
    db.commit()
    db.refresh(obj)
    if employee is None:
        employee = db.get(RecruitEmployee, obj.employee_id)
    return {"job": _recruit_job_out(obj, employee)}


@app.delete("/api/recruit/job-postings/{job_id}")
def delete_recruit_job_posting(job_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(RecruitJobPosting, job_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Recruit 岗位不存在")
    title = obj.job_title
    crud.add_audit(db, user.username, "Recruit岗位管理", "删除岗位", "recruit_job_posting", str(job_id), detail=title)
    db.delete(obj)
    db.commit()
    return {"ok": True, "deleted_id": job_id}

@app.get("/api/recruit/daily-task-stats")
def list_recruit_daily_task_stats(date: str | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    query = db.query(RecruitDailyTaskStat)
    if date:
        query = query.filter(RecruitDailyTaskStat.stat_date == date)
    rows = query.order_by(RecruitDailyTaskStat.stat_date.desc(), RecruitDailyTaskStat.issuer_login_name.asc(), RecruitDailyTaskStat.job_title.asc()).all()
    return {
        "items": [
            {
                "id": item.id,
                "stat_date": item.stat_date,
                "job_posting_id": item.job_posting_id,
                "issuer_login_name": item.issuer_login_name,
                "job_title": item.job_title,
                "greet_count": item.greet_count,
                "resume_request_count": item.resume_request_count,
                "resume_download_count": item.resume_download_count,
                "resume_ack_count": item.resume_ack_count,
                "updated_at": _format_recruit_time(item.updated_at),
            }
            for item in rows
        ]
    }


@app.get("/api/recruit/resumes/{agent_id}/download")
def download_recruit_resume(agent_id: str, db: Session = Depends(get_db), user: User = Depends(require_user)):
    download = db.query(RecruitResumeDownload).filter(
        RecruitResumeDownload.candidate_agent_id == agent_id
    ).order_by(RecruitResumeDownload.created_at.desc()).first()
    if not download or not download.file_path:
        raise HTTPException(status_code=404, detail="简历下载记录不存在")
    
    ROOT_DIR = Path(__file__).resolve().parents[2]
    abs_path = ROOT_DIR / "Recruit" / download.file_path
    
    if not abs_path.exists():
        raise HTTPException(status_code=404, detail=f"简历文件物理路径不存在: {download.file_path}")
        
    return FileResponse(
        path=str(abs_path),
        filename=abs_path.name,
        media_type="application/octet-stream"
    )


@app.post("/api/recruit/candidates/{agent_id}/import")
def import_recruit_candidate(agent_id: str, db: Session = Depends(get_db), user: User = Depends(require_user)):
    profile = db.query(RecruitCandidateProfile).filter(RecruitCandidateProfile.candidate_agent_id == agent_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="抓取候选人记录不存在")
        
    existing = db.query(Candidate).filter(
        Candidate.name == profile.candidate_name,
        Candidate.education == (profile.candidate_education or "")
    ).first()
    
    if existing:
        return {
            "success": True,
            "candidate": schemas.CandidateOut.model_validate(existing, from_attributes=True).model_dump(),
            "message": "系统内已存在同名且同学历的候选人，已关联现有候选人。"
        }
        
    download = db.query(RecruitResumeDownload).filter(
        RecruitResumeDownload.candidate_agent_id == agent_id
    ).order_by(RecruitResumeDownload.created_at.desc()).first()
    
    import re
    age_val = None
    if profile.candidate_age:
        m = re.search(r'\d+', profile.candidate_age)
        if m:
            age_val = int(m.group(0))
            
    new_c = Candidate(
        name=profile.candidate_name,
        phone="",
        email="",
        current_title=download.job_title if download else "",
        city="",
        status="未锁定",
        source="简历库",
        gender="",
        age=age_val,
        education=profile.candidate_education or "",
        expected_salary="",
        tags="",
        owner_user_id=user.id,
    )
    db.add(new_c)
    db.flush()
    
    crud.add_audit(db, user.username, "求职者数据池", "导入抓取简历", "candidate", str(new_c.id), detail=new_c.name)
    db.commit()
    db.refresh(new_c)
    
    return {
        "success": True,
        "candidate": schemas.CandidateOut.model_validate(new_c, from_attributes=True).model_dump(),
        "message": "成功导入到候选人池"
    }


@app.get("/api/db-tables")
def get_db_table_data(
    table_name: str | None = None,
    limit: int = Query(default=10000, ge=1, le=100000),
    db: Session = Depends(get_db),
    user: User = Depends(require_user)
):
    inspector = inspect(db.bind)
    
    # If no table_name is specified, dynamically inspect all database schemas and return a list of all tables
    if table_name is None:
        all_tables = []
        try:
            schemas = inspector.get_schema_names()
        except Exception:
            schemas = []
            
        # Inspect default schema tables
        try:
            for t in inspector.get_table_names():
                if t != "alembic_version" and t not in all_tables:
                    all_tables.append(t)
        except Exception:
            pass
            
        # Inspect recruit schema tables
        if "recruit" in schemas:
            try:
                for t in inspector.get_table_names(schema="recruit"):
                    if t != "alembic_version" and t not in all_tables:
                        all_tables.append(t)
            except Exception:
                pass
                
        # Inspect public schema tables
        if "public" in schemas:
            try:
                for t in inspector.get_table_names(schema="public"):
                    if t != "alembic_version" and t not in all_tables:
                        all_tables.append(t)
            except Exception:
                pass
                
        all_tables.sort()
        return all_tables

    # We will map table_name to model classes
    model_mapping = {
        "users": User,
        "roles": Role,
        "role_permissions": RolePermission,
        "data_permissions": DataPermission,
        "companies": Company,
        "projects": Project,
        "positions": Position,
        "candidates": Candidate,
        "recommendations": Recommendation,
        "recommendation_feedbacks": RecommendationFeedback,
        "candidate_tracking_events": CandidateTrackingEvent,
        "interview_records": InterviewRecord,
        "salary_records": SalaryRecord,
        "employment_records": EmploymentRecord,
        "candidate_follow_up_records": CandidateFollowUpRecord,
        "candidate_mail_records": CandidateMailRecord,
        "search_presets": SearchPreset,
        "export_records": ExportRecord,
        "import_records": ImportRecord,
        "deliveries": Delivery,
        "audit_logs": AuditLog,
        "warranty_rules": WarrantyRule,
        "system_configs": SystemConfig,
        "email_configs": EmailConfig,
        "ai_tasks": AiTask,
        "resume_parse_tasks": ResumeParseTask,
        "candidate_profiles": RecruitCandidateProfile,
        "resume_downloads": RecruitResumeDownload,
        "employees": RecruitEmployee,
        "job_postings": RecruitJobPosting,
        "daily_task_stats": RecruitDailyTaskStat,
        "candidate_notes": CandidateNote
    }
    
    # Dynamically determine the schema of the requested table
    recruit_tables = {"candidate_profiles", "resume_downloads", "employees", "job_postings", "daily_task_stats"}
    schema = None
    if table_name in recruit_tables:
        schema = "recruit"
    else:
        try:
            if "recruit" in inspector.get_schema_names():
                r_tables = inspector.get_table_names(schema="recruit")
                if table_name in r_tables:
                    schema = "recruit"
        except Exception:
            pass

    # Retrieve columns for the table
    try:
        columns = [col["name"] for col in inspector.get_columns(table_name, schema=schema)]
    except Exception:
        columns = []
        
    if not columns:
        raise HTTPException(status_code=400, detail=f"物理表 {table_name} 不存在或无列结构")
        
    # Execute query
    model = model_mapping.get(table_name)
    data = []
    
    if model:
        # Query using SQLAlchemy ORM
        records = db.query(model).limit(limit).all()
        for r in records:
            row_dict = {}
            for col in columns:
                val = getattr(r, col, None)
                if isinstance(val, datetime):
                    val = val.isoformat()
                row_dict[col] = val
            data.append(row_dict)
    else:
        # Fallback to raw SQL for tables without ORM mapping
        full_table = f'"{schema}"."{table_name}"' if schema else f'"{table_name}"'
        try:
            result = db.execute(text(f"SELECT * FROM {full_table} LIMIT :limit"), {"limit": limit})
            records = result.fetchall()
            for r in records:
                row_dict = {}
                for col in columns:
                    if hasattr(r, "_mapping"):
                        val = r._mapping.get(col)
                    else:
                        val = getattr(r, col, None)
                    if isinstance(val, datetime):
                        val = val.isoformat()
                    row_dict[col] = val
                data.append(row_dict)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"查询表数据失败: {str(e)}")
        
    return {
        "table_name": table_name,
        "columns": columns,
        "records": data
    }


ROOT_DIR = Path(__file__).resolve().parents[2]
app.mount("/", StaticFiles(directory=ROOT_DIR, html=True), name="static")
