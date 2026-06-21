from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from fastapi.responses import FileResponse
from . import crud, models, schemas
from .config import settings
from .database import Base, engine, get_db
from .models import AuditLog, AiTask, Candidate, CandidateFollowUpRecord, CandidateMailRecord, CandidateTrackingEvent, Company, DataPermission, Delivery, EmailConfig, EmploymentRecord, Evaluation, EvaluationLevel, InterviewRecord, Notification, Position, Project, Recommendation, RecommendationFeedback, Role, RolePermission, SalaryRecord, SearchPreset, SystemConfig, TagDictionary, WarrantyRule, User, RecruitCandidateProfile, RecruitResumeDownload
from .security import get_current_user
from backend.seed import seed as seed_data


app = FastAPI(title="招聘管理系统 API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def ensure_schema() -> None:
    Base.metadata.create_all(bind=engine)
    with engine.begin() as conn:
      cols = {row[1] for row in conn.execute(text("PRAGMA table_info(recommendations)")).fetchall()} if engine.url.get_backend_name() == "sqlite" else set()
      if "customer_comment" not in cols:
          conn.execute(text("ALTER TABLE recommendations ADD COLUMN customer_comment TEXT NOT NULL DEFAULT ''"))
      eval_cols = {row[1] for row in conn.execute(text("PRAGMA table_info(evaluations)")).fetchall()} if engine.url.get_backend_name() == "sqlite" else set()
      if "position_id" not in eval_cols:
          conn.execute(text("ALTER TABLE evaluations ADD COLUMN position_id INTEGER NOT NULL DEFAULT 1"))
      company_cols = {row[1] for row in conn.execute(text("PRAGMA table_info(companies)")).fetchall()} if engine.url.get_backend_name() == "sqlite" else set()
      for column, ddl in {
          "contact_email": "ALTER TABLE companies ADD COLUMN contact_email TEXT NOT NULL DEFAULT ''",
          "address": "ALTER TABLE companies ADD COLUMN address TEXT NOT NULL DEFAULT ''",
          "cooperation_period": "ALTER TABLE companies ADD COLUMN cooperation_period TEXT NOT NULL DEFAULT ''",
      }.items():
          if column not in company_cols:
              conn.execute(text(ddl))
      project_cols = {row[1] for row in conn.execute(text("PRAGMA table_info(projects)")).fetchall()} if engine.url.get_backend_name() == "sqlite" else set()
      if "project_period" not in project_cols:
          conn.execute(text("ALTER TABLE projects ADD COLUMN project_period TEXT NOT NULL DEFAULT ''"))
      mail_cols = {row[1] for row in conn.execute(text("PRAGMA table_info(candidate_mail_records)")).fetchall()} if engine.url.get_backend_name() == "sqlite" else set()
      for column, ddl in {
          "recipient_email": "ALTER TABLE candidate_mail_records ADD COLUMN recipient_email TEXT NOT NULL DEFAULT ''",
          "mail_subject": "ALTER TABLE candidate_mail_records ADD COLUMN mail_subject TEXT NOT NULL DEFAULT ''",
          "mail_body": "ALTER TABLE candidate_mail_records ADD COLUMN mail_body TEXT NOT NULL DEFAULT ''",
          "attachment_name": "ALTER TABLE candidate_mail_records ADD COLUMN attachment_name TEXT NOT NULL DEFAULT ''",
          "sent_by": "ALTER TABLE candidate_mail_records ADD COLUMN sent_by TEXT NOT NULL DEFAULT ''",
          "status": "ALTER TABLE candidate_mail_records ADD COLUMN status TEXT NOT NULL DEFAULT '已发送'",
      }.items():
          if column not in mail_cols:
              conn.execute(text(ddl))
      follow_cols = {row[1] for row in conn.execute(text("PRAGMA table_info(candidate_follow_up_records)")).fetchall()} if engine.url.get_backend_name() == "sqlite" else set()
      for column, ddl in {
          "status": "ALTER TABLE candidate_follow_up_records ADD COLUMN status TEXT NOT NULL DEFAULT '已录用'",
          "follow_up_time": "ALTER TABLE candidate_follow_up_records ADD COLUMN follow_up_time DATETIME",
          "content": "ALTER TABLE candidate_follow_up_records ADD COLUMN content TEXT NOT NULL DEFAULT ''",
          "operator": "ALTER TABLE candidate_follow_up_records ADD COLUMN operator TEXT NOT NULL DEFAULT ''",
      }.items():
          if column not in follow_cols:
              conn.execute(text(ddl))
      level_cols = {row[1] for row in conn.execute(text("PRAGMA table_info(evaluation_levels)")).fetchall()} if engine.url.get_backend_name() == "sqlite" else set()
      for column, ddl in {
          "name": "ALTER TABLE evaluation_levels ADD COLUMN name TEXT NOT NULL DEFAULT ''",
          "score": "ALTER TABLE evaluation_levels ADD COLUMN score INTEGER NOT NULL DEFAULT 5",
          "description": "ALTER TABLE evaluation_levels ADD COLUMN description TEXT NOT NULL DEFAULT ''",
          "color": "ALTER TABLE evaluation_levels ADD COLUMN color TEXT NOT NULL DEFAULT ''",
          "sort_order": "ALTER TABLE evaluation_levels ADD COLUMN sort_order INTEGER NOT NULL DEFAULT 0",
          "enabled": "ALTER TABLE evaluation_levels ADD COLUMN enabled BOOLEAN NOT NULL DEFAULT 1",
      }.items():
          if column not in level_cols:
              conn.execute(text(ddl))
      if engine.url.get_backend_name() == "sqlite" and not level_cols:
          conn.execute(text("CREATE TABLE IF NOT EXISTS evaluation_levels (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL DEFAULT '', score INTEGER NOT NULL DEFAULT 5, description TEXT NOT NULL DEFAULT '', color TEXT NOT NULL DEFAULT '', sort_order INTEGER NOT NULL DEFAULT 0, enabled BOOLEAN NOT NULL DEFAULT 1, created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)"))
      feedback_cols = {row[1] for row in conn.execute(text("PRAGMA table_info(recommendation_feedbacks)")).fetchall()} if engine.url.get_backend_name() == "sqlite" else set()
      if engine.url.get_backend_name() == "sqlite" and not feedback_cols:
          conn.execute(text("CREATE TABLE IF NOT EXISTS recommendation_feedbacks (id INTEGER PRIMARY KEY AUTOINCREMENT, recommendation_id INTEGER NOT NULL, status TEXT NOT NULL, feedback TEXT NOT NULL DEFAULT '', customer_comment TEXT NOT NULL DEFAULT '', operator TEXT NOT NULL DEFAULT '', created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)"))
      candidate_cols = {row[1] for row in conn.execute(text("PRAGMA table_info(candidates)")).fetchall()} if engine.url.get_backend_name() == "sqlite" else set()
      for column, ddl in {
          "gender": "ALTER TABLE candidates ADD COLUMN gender TEXT NOT NULL DEFAULT ''",
          "age": "ALTER TABLE candidates ADD COLUMN age INTEGER",
          "education": "ALTER TABLE candidates ADD COLUMN education TEXT NOT NULL DEFAULT ''",
          "experience_years": "ALTER TABLE candidates ADD COLUMN experience_years INTEGER",
          "expected_salary": "ALTER TABLE candidates ADD COLUMN expected_salary TEXT NOT NULL DEFAULT ''",
          "id_number": "ALTER TABLE candidates ADD COLUMN id_number TEXT NOT NULL DEFAULT ''",
          "tags": "ALTER TABLE candidates ADD COLUMN tags TEXT NOT NULL DEFAULT ''",
          "candidate_agent_id": "ALTER TABLE candidates ADD COLUMN candidate_agent_id TEXT",
      }.items():
          if column not in candidate_cols:
              conn.execute(text(ddl))

      position_cols = {row[1] for row in conn.execute(text("PRAGMA table_info(positions)")).fetchall()} if engine.url.get_backend_name() == "sqlite" else set()
      for column, ddl in {
          "age_requirement": "ALTER TABLE positions ADD COLUMN age_requirement TEXT NOT NULL DEFAULT ''",
          "education_requirement": "ALTER TABLE positions ADD COLUMN education_requirement TEXT NOT NULL DEFAULT ''",
          "experience_requirement": "ALTER TABLE positions ADD COLUMN experience_requirement TEXT NOT NULL DEFAULT ''",
          "description": "ALTER TABLE positions ADD COLUMN description TEXT NOT NULL DEFAULT ''",
      }.items():
          if column not in position_cols:
              conn.execute(text(ddl))


ensure_schema()


@app.on_event("startup")
def startup() -> None:
    ensure_schema()
    seed_data()


def require_user(db: Session = Depends(get_db), authorization: str | None = Header(default=None)):
    return get_current_user(db, authorization)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "hr-platform"}


@app.get("/api/users", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_users(db)


@app.post("/api/users", response_model=schemas.UserOut)
def add_user(payload: schemas.UserCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_user(db, payload)
    crud.add_audit(db, user.username, "用户管理", "新增用户", "user", payload.username, detail=payload.full_name)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/api/users/{user_id}", response_model=schemas.UserOut)
def edit_user(user_id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(User, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="用户不存在")
    crud.update_user(db, obj, payload)
    crud.add_audit(db, user.username, "用户管理", "编辑用户", "user", str(user_id), detail=obj.username)
    db.commit()
    db.refresh(obj)
    return obj


@app.post("/api/users/{user_id}/toggle", response_model=schemas.UserOut)
def toggle_user(user_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(User, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="用户不存在")
    obj.is_active = not obj.is_active
    crud.add_audit(db, user.username, "用户管理", "切换用户状态", "user", str(user_id), detail=obj.username)
    db.commit()
    db.refresh(obj)
    return obj


@app.post("/api/users/{user_id}/reset-password", response_model=schemas.UserOut)
def reset_user_password(user_id: int, payload: schemas.UserResetPassword, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(User, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="用户不存在")
    crud.reset_user_password(db, obj, payload)
    crud.add_audit(db, user.username, "用户管理", "重置用户密码", "user", str(user_id), detail=obj.username)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/roles", response_model=list[schemas.RoleOut])
def get_roles(db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_roles(db)


@app.post("/api/roles", response_model=schemas.RoleOut)
def add_role(payload: schemas.RoleCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_role(db, payload)
    crud.add_audit(db, user.username, "角色管理", "新增角色", "role", payload.code, detail=payload.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/api/roles/{role_id}", response_model=schemas.RoleOut)
def edit_role(role_id: int, payload: schemas.RoleUpdate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(Role, role_id)
    if not obj:
        raise HTTPException(status_code=404, detail="角色不存在")
    crud.update_role(db, obj, payload)
    crud.add_audit(db, user.username, "角色管理", "编辑角色", "role", str(role_id), detail=obj.code)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/api/roles/{role_id}")
def remove_role(role_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
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
def toggle_role(role_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
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
    if payload.password != "admin123":
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return schemas.TokenResponse(access_token=settings.access_token)


@app.get("/api/me", response_model=schemas.CurrentUser)
def me(user: User = Depends(require_user)):
    return schemas.CurrentUser(id=user.id, username=user.username, full_name=user.full_name, role=user.role, is_active=user.is_active)


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
    user: User = Depends(require_user),
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
    return db.query(Company).order_by(Company.created_at.desc()).all()


@app.post("/api/companies", response_model=schemas.CompanyOut)
def add_company(payload: schemas.CompanyCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
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
    name = obj.name
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
        item = schemas.ProjectOut.model_validate(project, from_attributes=True).model_dump()
        item["company_name"] = company_name or ""
        result.append(item)
    return result


@app.post("/api/projects", response_model=schemas.ProjectOut)
def add_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
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
    name = obj.name
    db.delete(obj)
    crud.add_audit(db, user.username, "项目管理", "删除项目", "project", str(project_id), detail=name)
    db.commit()
    return {"ok": True}


@app.get("/api/positions", response_model=list[schemas.PositionOut])
def list_positions(project_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    query = db.query(Position)
    if project_id is not None:
        query = query.filter(Position.project_id == project_id)
    return query.order_by(Position.created_at.desc()).all()


@app.post("/api/positions", response_model=schemas.PositionOut)
def add_position(payload: schemas.PositionCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
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
    status_cycle = {"待招": "招聘中", "招聘中": "已关闭", "已关闭": "待招"}
    obj.status = status_cycle.get(obj.status, "待招")
    crud.add_audit(db, user.username, "岗位管理", "切换岗位状态", "position", str(position_id), detail=obj.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/candidates", response_model=list[schemas.CandidateOut])
def list_candidates(
    keyword: str | None = Query(default=None),
    city: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    return crud.list_candidates(db, keyword=keyword, city=city, status=status)


@app.post("/api/candidates", response_model=schemas.CandidateOut)
def add_candidate(payload: schemas.CandidateCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_candidate(db, payload)
    crud.add_audit(db, user.username, "候选人池", "创建候选人", "candidate", "new", detail=payload.name)
    db.commit()
    db.refresh(obj)
    return obj


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
    crud.lock_candidate(db, candidate, False)
    crud.add_audit(db, user.username, "候选人跟踪", "释放候选人", "candidate", str(candidate.id), detail=candidate.name)
    db.commit()
    db.refresh(candidate)
    return candidate


@app.get("/api/candidate-tracking-events", response_model=list[schemas.CandidateTrackingEventOut])
def list_candidate_tracking_events(candidate_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_tracking_events(db, candidate_id=candidate_id)


@app.post("/api/candidate-tracking-events", response_model=schemas.CandidateTrackingEventOut)
def add_candidate_tracking_event(payload: schemas.CandidateTrackingEventCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_tracking_event(db, payload)
    crud.add_audit(db, user.username, "候选人跟踪", payload.event_type, "candidate_tracking_event", str(payload.candidate_id), detail=payload.summary)
    db.commit()
    db.refresh(obj)
    return obj


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
    obj = crud.create_salary_record(db, payload)
    crud.add_audit(db, user.username, "候选人跟踪", "新增薪资记录", "salary_record", str(payload.candidate_id), detail=payload.service_status)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/employment-records", response_model=list[schemas.EmploymentRecordOut])
def list_employment_records(candidate_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_employment_records(db, candidate_id=candidate_id)


@app.post("/api/employment-records", response_model=schemas.EmploymentRecordOut)
def add_employment_record(payload: schemas.EmploymentRecordCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_employment_record(db, payload)
    crud.add_audit(db, user.username, "候选人跟踪", "新增入职记录", "employment_record", str(payload.candidate_id), detail=payload.status)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/candidate-follow-up-records", response_model=list[schemas.CandidateFollowUpRecordOut])
def list_candidate_follow_up_records(candidate_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_candidate_follow_up_records(db, candidate_id=candidate_id)


@app.post("/api/candidate-follow-up-records", response_model=schemas.CandidateFollowUpRecordOut)
def add_candidate_follow_up_record(payload: schemas.CandidateFollowUpRecordCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_candidate_follow_up_record(db, payload)
    crud.add_audit(db, user.username, "候选人跟踪", "新增随访记录", "candidate_follow_up_record", str(payload.candidate_id), detail=payload.content[:32])
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/candidate-mail-records", response_model=list[schemas.CandidateMailRecordOut])
def list_candidate_mail_records(candidate_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_candidate_mail_records(db, candidate_id=candidate_id)


@app.post("/api/candidate-mail-records", response_model=schemas.CandidateMailRecordOut)
def add_candidate_mail_record(payload: schemas.CandidateMailRecordCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_candidate_mail_record(db, payload)
    crud.add_audit(db, user.username, "候选人跟踪", "发送邮件", "candidate_mail_record", str(payload.candidate_id), detail=payload.mail_subject)
    db.commit()
    db.refresh(obj)
    return obj


@app.post("/api/recommendations", response_model=schemas.RecommendationOut)
def add_recommendation(payload: schemas.RecommendationCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    candidate = db.get(Candidate, payload.candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    if candidate.locked:
        raise HTTPException(status_code=400, detail="候选人已锁定，无法重复推荐")
    obj = crud.create_recommendation(db, payload)
    crud.add_audit(db, user.username, "推荐交付", "创建推荐记录", "recommendation", "new", detail=str(payload.candidate_id))
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/recommendations", response_model=list[schemas.RecommendationOut])
def get_recommendations(candidate_id: int | None = Query(default=None), position_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_recommendations(db, candidate_id=candidate_id, position_id=position_id)


@app.put("/api/recommendations/{recommendation_id}", response_model=schemas.RecommendationOut)
def update_recommendation(recommendation_id: int, payload: schemas.RecommendationUpdate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = db.get(Recommendation, recommendation_id)
    if not obj:
        raise HTTPException(status_code=404, detail="推荐记录不存在")
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
    return crud.list_recommendation_feedbacks(db, recommendation_id=recommendation_id)


@app.post("/api/recommendation-feedbacks", response_model=schemas.RecommendationFeedbackOut)
def add_recommendation_feedback(payload: schemas.RecommendationFeedbackCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_recommendation_feedback(db, payload)
    crud.add_audit(db, user.username, "推荐交付", "记录客户反馈", "recommendation_feedback", str(payload.recommendation_id), detail=payload.status)
    db.commit()
    db.refresh(obj)
    return obj





@app.post("/api/deliveries", response_model=schemas.DeliveryOut)
def add_delivery(payload: schemas.DeliveryCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_delivery(db, payload)
    crud.add_audit(db, user.username, "推荐交付", "创建交付记录", "delivery", "new", detail=str(payload.recommendation_id))
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/deliveries", response_model=list[schemas.DeliveryOut])
def get_deliveries(recommendation_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_deliveries(db, recommendation_id=recommendation_id)


@app.get("/api/evaluations", response_model=list[schemas.EvaluationOut])
def get_evaluations(candidate_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_evaluations(db, candidate_id=candidate_id)


@app.post("/api/evaluations", response_model=schemas.EvaluationOut)
def add_evaluation(payload: schemas.EvaluationCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
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
    return crud.list_tags(db)


@app.post("/api/tags", response_model=schemas.TagOut)
def add_tag(payload: schemas.TagCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_tag(db, payload)
    crud.add_audit(db, user.username, "标签字典", "新增标签", "tag", "new", detail=payload.name)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/api/tags/{tag_id}", response_model=schemas.TagOut)
def edit_tag(tag_id: int, payload: schemas.TagUpdate, db: Session = Depends(get_db), user: User = Depends(require_user)):
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
    return crud.list_notifications(db, type=type, read=read, keyword=keyword, date_from=date_from, date_to=date_to)


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
    crud.mark_notification_read(db, obj)
    crud.add_audit(db, user.username, "通知提醒", "已读通知", "notification", str(notification_id), detail=obj.title)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/api/notifications/batch-read")
def batch_read_notifications(payload: list[int], db: Session = Depends(get_db), user: User = Depends(require_user)):
    for notification_id in payload:
        obj = db.get(Notification, notification_id)
        if obj and not obj.read:
            crud.mark_notification_read(db, obj)
    crud.add_audit(db, user.username, "通知提醒", "批量已读通知", "notification", "batch", detail=f"Count: {len(payload)}")
    db.commit()
    return {"ok": True}


@app.get("/api/warranty-rules", response_model=list[schemas.WarrantyRuleOut])
def get_warranty_rules(db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_warranty_rules(db)


@app.post("/api/warranty-rules", response_model=schemas.WarrantyRuleOut)
def add_warranty_rule(payload: schemas.WarrantyRuleCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_warranty_rule(db, payload)
    crud.add_audit(db, user.username, "质保期管理", "新增质保规则", "warranty_rule", "new", detail=payload.scope)
    db.commit()
    db.refresh(obj)
    return obj


@app.put("/api/warranty-rules/{rule_id}", response_model=schemas.WarrantyRuleOut)
def update_warranty_rule(rule_id: int, payload: schemas.WarrantyRuleCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
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
    recommendation_rows = db.query(Recommendation.recommender, Recommendation.status).all()
    project_rows = db.query(Project.company_id, Project.status, Company.name).join(Company, Company.id == Project.company_id).all()
    recommender_stats: dict[str, dict[str, int]] = {}
    for recommender, status in recommendation_rows:
        key = recommender or "未命名"
        bucket = recommender_stats.setdefault(key, {"total": 0, "active": 0})
        bucket["total"] += 1
        if status in {"客户已收", "安排面试", "已录用"}:
            bucket["active"] += 1
    customer_stats: dict[str, dict[str, int]] = {}
    for company_id, status, company_name in project_rows:
        key = company_name or f"客户 {company_id}"
        bucket = customer_stats.setdefault(key, {"total": 0, "active": 0})
        bucket["total"] += 1
        if status != "招聘完毕":
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
        "candidate_count": db.query(Candidate).count(),
        "recommendation_count": db.query(Recommendation).count(),
        "delivery_count": db.query(Delivery).count(),
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
    return crud.list_ai_tasks(db)


@app.post("/api/ai/tasks", response_model=schemas.AiTaskOut)
def create_ai_task(payload: schemas.AiTaskCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_ai_task(db, payload)
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
def get_role_permissions(role_code: str | None = None, db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_role_permissions(db, role_code=role_code)


@app.post("/api/role-permissions", response_model=schemas.RolePermissionOut)
def upsert_role_permission(payload: schemas.RolePermissionCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.save_role_permission(db, payload)
    crud.add_audit(db, user.username, "权限管理", "保存功能权限", "role_permission", payload.role_code, detail=payload.permission_key)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/data-permissions", response_model=list[schemas.DataPermissionOut])
def get_data_permissions(user_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(require_user)):
    return crud.list_data_permissions(db, user_id=user_id)


@app.post("/api/data-permissions", response_model=schemas.DataPermissionOut)
def upsert_data_permission(payload: schemas.DataPermissionCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.save_data_permission(db, payload)
    crud.add_audit(db, user.username, "权限管理", "保存数据权限", "data_permission", str(payload.user_id), detail=f"{payload.scope_type}:{payload.scope_id}")
    db.commit()
    db.refresh(obj)
    return obj
@app.post("/api/imports/smoke")
def import_smoke(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(require_user)):
    name = Path(file.filename or "").stem or "未命名简历"
    duplicate = db.query(Candidate).filter(Candidate.name == name).order_by(Candidate.created_at.desc()).first()
    if duplicate:
        import_record = crud.create_import_record(
            db,
            schemas.ImportRecordCreate(
                file_name=file.filename or name,
                imported_by=user.username,
                imported_count=0,
                failed_count=1,
                status="复核",
                note=f"检测到同名候选人：{duplicate.name}，等待覆盖确认",
            ),
        )
        crud.add_audit(db, user.username, "简历导入", "导入简历复核", "candidate", str(duplicate.id), result="失败", detail=file.filename or "")
        db.commit()
        db.refresh(import_record)
        return {"imported": 0, "duplicate": schemas.CandidateOut.model_validate(duplicate, from_attributes=True).model_dump(), "import_record": schemas.ImportRecordOut.model_validate(import_record, from_attributes=True).model_dump()}
    candidate = Candidate(name=name, source="文件导入", status="激活", locked=False)
    db.add(candidate)
    import_record = crud.create_import_record(db, schemas.ImportRecordCreate(file_name=file.filename or name, imported_by=user.username, imported_count=1, failed_count=0, status="成功", note=f"导入候选人 {name}"))
    crud.add_audit(db, user.username, "简历导入", "导入简历", "candidate", "new", detail=file.filename or "")
    db.commit()
    db.refresh(candidate)
    db.refresh(import_record)
    return {"imported": 1, "candidate": schemas.CandidateOut.model_validate(candidate, from_attributes=True).model_dump(), "import_record": schemas.ImportRecordOut.model_validate(import_record, from_attributes=True).model_dump()}


@app.post("/api/imports/batch")
def import_batch(files: list[UploadFile] = File(...), db: Session = Depends(get_db), user: User = Depends(require_user)):
    imported = 0
    duplicates = 0
    records = []
    candidates = []
    for file in files:
        name = Path(file.filename or "").stem or "未命名简历"
        duplicate = db.query(Candidate).filter(Candidate.name == name).order_by(Candidate.created_at.desc()).first()
        if duplicate:
            duplicates += 1
            import_record = crud.create_import_record(
                db,
                schemas.ImportRecordCreate(
                    file_name=file.filename or name,
                    imported_by=user.username,
                    imported_count=0,
                    failed_count=1,
                    status="复核",
                    note=f"检测到同名候选人：{duplicate.name}，等待覆盖确认",
                ),
            )
            crud.add_audit(db, user.username, "简历导入", "批量导入复核", "candidate", str(duplicate.id), result="失败", detail=file.filename or "")
            db.flush()
            records.append(schemas.ImportRecordOut.model_validate(import_record, from_attributes=True).model_dump())
            continue
        candidate = Candidate(name=name, source="批量导入", status="激活", locked=False)
        db.add(candidate)
        import_record = crud.create_import_record(
            db,
            schemas.ImportRecordCreate(file_name=file.filename or name, imported_by=user.username, imported_count=1, failed_count=0, status="成功", note=f"导入候选人 {name}"),
        )
        crud.add_audit(db, user.username, "简历导入", "批量导入简历", "candidate", "new", detail=file.filename or "")
        db.flush()
        candidates.append(candidate)
        records.append(schemas.ImportRecordOut.model_validate(import_record, from_attributes=True).model_dump())
        imported += 1
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
    return crud.list_export_records(db, candidate_id=candidate_id)


@app.post("/api/export-records", response_model=schemas.ExportRecordOut)
def add_export_record(payload: schemas.ExportRecordCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    obj = crud.create_export_record(db, payload)
    crud.add_audit(db, user.username, "求职者数据池", "导出简历", "export_record", str(payload.candidate_id), detail=payload.file_name)
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
        status="新入库",
        source="智联抓取",
        gender="",
        age=age_val,
        education=profile.candidate_education or "",
        expected_salary="",
        tags=""
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


ROOT_DIR = Path(__file__).resolve().parents[2]
app.mount("/", StaticFiles(directory=ROOT_DIR, html=True), name="static")

