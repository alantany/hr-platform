from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import PurePosixPath
import json
import re
import socket

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from . import security
from .models import AuditLog, AiTask, Candidate, CandidateNote, CandidateFollowUpRecord, CandidateMailRecord, CandidateOwnershipTransfer, CandidateTrackingEvent, Company, DataPermission, Delivery, EmailConfig, EmploymentRecord, Evaluation, EvaluationLevel, ExportRecord, ImportRecord, InterviewRecord, Notification, Position, PositionAssignmentTask, Project, Recommendation, RecommendationFeedback, RecruitJobProfile, RecruitParseKeyword, Role, RolePermission, SalaryRecord, SearchHotword, SearchPreset, SystemConfig, TagDictionary, User, WarrantyRule


TAG_OBJECT_LABELS = {
    "candidate": "候选人",
    "position": "岗位",
    "project": "项目",
    "company": "客户",
}

RECOMMENDATION_FLOW_STATUS_MAP = {
    "待推荐": "待推荐",
    "已推荐": "已推荐",
    "客户已收": "已推荐",
    "客户未收": "已推荐",
    "安排面试": "面试中",
    "面试中": "面试中",
    "拒绝": "未录用",
    "淘汰": "未录用",
    "未录用": "未录用",
    "已入职": "已入职",
}

# 单个岗位同时处于锁定关系（有推荐记录）的候选人上限
POSITION_LOCK_LIMIT = 10


def count_position_locked_candidates(db: Session, position_id: int) -> int:
    return (
        db.query(func.count(Recommendation.id))
        .filter(Recommendation.position_id == position_id)
        .scalar()
        or 0
    )


def ensure_position_lock_quota(db: Session, position_id: int, extra: int = 1) -> None:
    """岗位锁定名额不足时抛出 ValueError，供 API 层转成 HTTP 400。"""
    current = count_position_locked_candidates(db, position_id)
    if current + max(int(extra or 0), 0) > POSITION_LOCK_LIMIT:
        raise ValueError(f"此岗位锁定名额已满（上限 {POSITION_LOCK_LIMIT} 人），请先移除后再添加")


def count_position_onboarded(db: Session, position_id: int) -> int:
    return (
        db.query(func.count(Recommendation.id))
        .filter(
            Recommendation.position_id == position_id,
            Recommendation.status == "已入职",
        )
        .scalar()
        or 0
    )


def is_position_hiring_filled(db: Session, position: Position) -> bool:
    needed = max(int(position.hiring_count or 0), 0)
    if needed <= 0:
        return True
    onboarded = count_position_onboarded(db, position.id)
    return onboarded == needed


def is_project_hiring_complete(db: Session, project_id: int) -> bool:
    positions = db.query(Position).filter(Position.project_id == project_id).all()
    if not positions:
        return False
    return all(is_position_hiring_filled(db, position) for position in positions)


def sync_project_completion_status(db: Session, project_id: int | None) -> Project | None:
    """项目下每个岗位均招满（已入职人数 == 应招人数）时，自动标记招聘完毕。"""
    if not project_id:
        return None
    project = db.get(Project, project_id)
    if not project:
        return None
    if project.status == "招聘中止":
        return project
    if is_project_hiring_complete(db, project_id):
        project.status = "招聘完毕"
    elif project.status == "招聘完毕":
        # 若后续入职回退导致未招满，回退为招聘中
        project.status = "招聘中"
    db.add(project)
    return project


def candidate_ids_with_interview_rounds(db: Session) -> set[int]:
    tracked = {
        int(candidate_id)
        for (candidate_id,) in db.query(CandidateTrackingEvent.candidate_id)
        .filter(
            CandidateTrackingEvent.interview_round.isnot(None),
            CandidateTrackingEvent.interview_round != "",
        )
        .distinct()
        .all()
        if candidate_id is not None
    }
    interviewed = {
        int(candidate_id)
        for (candidate_id,) in db.query(InterviewRecord.candidate_id).distinct().all()
        if candidate_id is not None
    }
    return tracked | interviewed


def _created_at_score(value) -> float:
    if not value:
        return 0.0
    if isinstance(value, datetime):
        return value.timestamp()
    text = str(value).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(text[:26], fmt).replace(tzinfo=timezone.utc).timestamp()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return 0.0


def _record_completeness_score(item: dict) -> int:
    fields = [
        "name",
        "phone",
        "email",
        "current_title",
        "city",
        "education",
        "age",
        "expected_salary",
        "birth_date",
        "hukou_location",
        "onboard_cycle",
        "education_detail",
        "certificates",
        "comprehensive_evaluation",
        "work_history",
        "core_value",
        "job_status",
        "family_status",
        "salary_structure",
        "job_intention",
        "project_history",
    ]
    return sum(1 for field in fields if item.get(field) not in (None, "", []))


def _record_priority(item: dict) -> tuple[int, int, float, int]:
    record_key = str(item.get("record_key") or "")
    source_bonus = 1000 if record_key.startswith("candidate:") else 0
    file_bonus = 100 if item.get("file_path") else 0
    return (
        source_bonus + file_bonus + _record_completeness_score(item),
        1 if item.get("source") == "简历库" else 0,
        _created_at_score(item.get("created_at")),
        int(item.get("id") or 0),
    )


def _normalize_resume_file_key(file_path: str | None) -> str | None:
    text = str(file_path or "").strip().replace("\\", "/")
    if not text:
        return None
    name = PurePosixPath(text).name.strip().lower()
    return name or None


def _normalize_phone(value: str | None) -> str:
    return re.sub(r"\D", "", str(value or ""))


def _person_dedupe_key(
    name: str | None = "",
    phone: str | None = "",
    email: str | None = "",
    id_number: str | None = "",
) -> str | None:
    phone_norm = _normalize_phone(phone)
    if phone_norm:
        return f"phone:{phone_norm}"
    email_norm = str(email or "").strip().lower()
    if email_norm:
        return f"email:{email_norm}"
    id_norm = str(id_number or "").strip()
    if id_norm:
        return f"id:{id_norm}"
    name_norm = str(name or "").strip().lower()
    if name_norm:
        return f"name:{name_norm}"
    return None


def _person_dedupe_key_for_item(item: dict) -> str:
    file_key = _normalize_resume_file_key(item.get("file_path"))
    if file_key:
        return f"file:{file_key}"
    person_key = _person_dedupe_key(
        item.get("name"),
        item.get("phone"),
        item.get("email"),
        item.get("id_number"),
    )
    if person_key:
        return person_key
    candidate_agent_id = item.get("candidate_agent_id")
    if candidate_agent_id:
        return f"agent:{candidate_agent_id}"
    return str(item.get("record_key") or f"candidate:{item.get('id')}")


def find_candidate_by_resume_file(db: Session, file_path: str | None) -> Candidate | None:
    file_key = _normalize_resume_file_key(file_path)
    if not file_key:
        return None
    matches = [
        row
        for row in db.query(Candidate).filter(Candidate.file_path.isnot(None), Candidate.file_path != "").all()
        if _normalize_resume_file_key(row.file_path) == file_key
    ]
    if not matches:
        return None
    return max(
        matches,
        key=lambda row: (
            _record_completeness_score(
                {
                    "name": row.name,
                    "phone": row.phone,
                    "email": row.email,
                    "current_title": row.current_title,
                    "city": row.city,
                    "education": row.education,
                    "age": row.age,
                    "file_path": row.file_path,
                }
            ),
            int(row.id or 0),
        ),
    )


def find_candidate_by_person(
    db: Session,
    *,
    name: str = "",
    phone: str = "",
    email: str = "",
    id_number: str = "",
    file_path: str = "",
) -> Candidate | None:
    by_file = find_candidate_by_resume_file(db, file_path)
    if by_file:
        return by_file

    id_norm = str(id_number or "").strip()
    if id_norm:
        found = db.query(Candidate).filter(Candidate.id_number == id_norm).first()
        if found:
            return found

    phone_norm = _normalize_phone(phone)
    if phone_norm:
        for row in db.query(Candidate).filter(Candidate.phone.isnot(None), Candidate.phone != "").all():
            if _normalize_phone(row.phone) == phone_norm:
                return row

    email_norm = str(email or "").strip().lower()
    if email_norm:
        found = db.query(Candidate).filter(func.lower(Candidate.email) == email_norm).first()
        if found:
            return found

    name_norm = str(name or "").strip()
    if name_norm:
        rows = (
            db.query(Candidate)
            .filter(Candidate.name == name_norm)
            .all()
        )
        if rows:
            return max(
                rows,
                key=lambda row: (
                    1 if _normalize_phone(row.phone) else 0,
                    1 if str(row.email or "").strip() else 0,
                    _record_completeness_score({"name": row.name, "phone": row.phone, "email": row.email, "current_title": row.current_title, "city": row.city, "education": row.education, "age": row.age}),
                    int(row.id or 0),
                ),
            )
    return None


def _dedupe_key_for_item(item: dict) -> str:
    return _person_dedupe_key_for_item(item)


def add_audit(db: Session, actor: str, module: str, action: str, target_type: str = "", target_id: str = "", result: str = "成功", detail: str = ""):
    log = AuditLog(
        actor=actor,
        module=module,
        action=action,
        target_type=target_type,
        target_id=target_id,
        result=result,
        detail=detail,
    )
    db.add(log)
    return log


def assigned_project_ids_for_user(db: Session, user_id: int) -> list[int]:
    position_ids: set[int] = set()
    for (position_id,) in db.query(PositionAssignmentTask.position_id).filter(
        PositionAssignmentTask.assignee_user_id == user_id,
        PositionAssignmentTask.status.in_(["pending", "accepted"]),
    ).all():
        position_ids.add(int(position_id))
    for (scope_id,) in db.query(DataPermission.scope_id).filter(
        DataPermission.user_id == user_id,
        DataPermission.scope_type == "position",
        DataPermission.active.is_(True),
    ).all():
        if str(scope_id).isdigit():
            position_ids.add(int(scope_id))
    for (position_id,) in db.query(Position.id).filter(Position.owner_user_id == user_id).all():
        position_ids.add(int(position_id))
    if not position_ids:
        return []
    rows = db.query(Position.project_id).filter(Position.id.in_(position_ids)).distinct().all()
    return sorted({int(project_id) for (project_id,) in rows if project_id is not None})


def dashboard_summary(db: Session) -> dict:
    # 求职者总数以简历池列表口径为准（Recruit 下载 + 上传等 list_candidates 结果）
    return {
        "candidate_count": len(list_candidates(db)),
        "company_count": db.query(func.count(Company.id)).scalar() or 0,
        "project_count": db.query(func.count(Project.id)).scalar() or 0,
        "position_count": db.query(func.count(Position.id)).scalar() or 0,
        "user_count": db.query(func.count(User.id)).scalar() or 0,
        # 已推荐口径：曾经变为已推荐（recommended_at 有值）；待推荐不计
        "recommendation_count": db.query(func.count(Recommendation.id)).filter(
            Recommendation.recommended_at.isnot(None)
        ).scalar() or 0,
        "delivery_count": db.query(func.count(Delivery.id)).scalar() or 0,
        "audit_log_count": db.query(func.count(AuditLog.id)).scalar() or 0,
    }


def dashboard_todos(db: Session, limit: int = 4) -> list[dict]:
    todos: list[dict] = []
    notices = db.query(Notification).order_by(Notification.created_at.desc()).limit(2).all()
    audits = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(2).all()
    warranties = db.query(WarrantyRule).order_by(WarrantyRule.created_at.desc()).limit(2).all()
    recommendations = db.query(Recommendation).order_by(Recommendation.created_at.desc()).limit(2).all()
    if notices:
        notice = notices[0]
        todos.append({
            "title": notice.title,
            "meta": f"{notice.type or '通知'} · {notice.target_path or ''}".strip(" ·"),
            "tag": "查看" if notice.read else "提醒",
            "color": "blue" if notice.read else "red",
            "source": "notification",
            "target_path": notice.target_path or "./notifications.html",
        })
    if audits:
        log = audits[0]
        todos.append({
            "title": log.action,
            "meta": f"{log.module} · {log.actor}",
            "tag": "处理",
            "color": "orange",
            "source": "audit_log",
            "target_path": "./logs.html",
        })
    if warranties:
        rule = warranties[0]
        todos.append({
            "title": f"质保：{rule.scope}",
            "meta": f"{rule.months} 个月 · 提前 {rule.remind_days} 天提醒",
            "tag": "查看" if rule.auto_expire else "提醒",
            "color": "blue" if rule.auto_expire else "red",
            "source": "warranty_rule",
            "target_path": "./warranty.html",
        })
    if recommendations:
        rec = recommendations[0]
        todos.append({
            "title": f"推荐 {rec.candidate_id} → {rec.position_id}",
            "meta": f"{rec.recommender} · {rec.status}",
            "tag": "推进",
            "color": "green" if rec.status in {"客户已收", "安排面试", "已入职"} else "orange",
            "source": "recommendation",
            "target_path": "./dashboard.html",
        })
    return todos[:limit]


def list_recent_audit_logs(
    db: Session,
    limit: int = 50,
    actor: str | None = None,
    module: str | None = None,
    action: str | None = None,
    target_type: str | None = None,
    result: str | None = None,
    keyword: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
):
    query = db.query(AuditLog)
    if actor:
        query = query.filter(AuditLog.actor.like(f"%{actor}%"))
    if module:
        query = query.filter(AuditLog.module.like(f"%{module}%"))
    if action:
        query = query.filter(AuditLog.action.like(f"%{action}%"))
    if target_type:
        query = query.filter(AuditLog.target_type == target_type)
    if result:
        query = query.filter(AuditLog.result == result)
    if keyword:
        pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                AuditLog.actor.like(pattern),
                AuditLog.module.like(pattern),
                AuditLog.action.like(pattern),
                AuditLog.target_type.like(pattern),
                AuditLog.target_id.like(pattern),
                AuditLog.result.like(pattern),
                AuditLog.detail.like(pattern),
            )
        )
    if date_from:
        query = query.filter(AuditLog.created_at >= date_from)
    if date_to:
        query = query.filter(AuditLog.created_at <= date_to)
    return query.order_by(AuditLog.created_at.desc()).limit(limit).all()


def list_users(db: Session):
    return db.query(User).order_by(User.id.asc()).all()


def create_user(db: Session, payload):
    data = payload.model_dump()
    data["password_hash"] = security.hash_password(data["password_hash"])
    obj = User(**data)
    db.add(obj)
    return obj


def update_user(db: Session, user: User, payload):
    for key, value in payload.model_dump(exclude_unset=True).items():
        if key == "password_hash":
            value = security.hash_password(value)
        setattr(user, key, value)
    return user


def reset_user_password(db: Session, user: User, payload):
    user.password_hash = security.hash_password(payload.password_hash)
    return user


def delete_user(db: Session, user: User):
    """删除用户前解绑所有指向 users.id 的可空外键，保留业务历史记录。"""
    uid = user.id
    # 可空 FK：置 NULL，不级联删业务数据
    db.query(Recommendation).filter(Recommendation.recommender_user_id == uid).update(
        {Recommendation.recommender_user_id: None}, synchronize_session=False
    )
    db.query(InterviewRecord).filter(InterviewRecord.creator_user_id == uid).update(
        {InterviewRecord.creator_user_id: None}, synchronize_session=False
    )
    db.query(SalaryRecord).filter(SalaryRecord.operator_user_id == uid).update(
        {SalaryRecord.operator_user_id: None}, synchronize_session=False
    )
    db.query(EmploymentRecord).filter(EmploymentRecord.operator_user_id == uid).update(
        {EmploymentRecord.operator_user_id: None}, synchronize_session=False
    )
    db.delete(user)
    return True


def list_roles(db: Session):
    return db.query(Role).order_by(Role.id.asc()).all()


def create_role(db: Session, payload):
    obj = Role(**payload.model_dump())
    db.add(obj)
    return obj


def update_role(db: Session, role: Role, payload):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(role, key, value)
    return role


def create_company(db: Session, payload):
    obj = Company(**payload.model_dump())
    db.add(obj)
    return obj


def update_company(db: Session, company: Company, payload):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(company, key, value)
    return company


def create_project(db: Session, payload):
    obj = Project(**payload.model_dump())
    db.add(obj)
    return obj


def update_project(db: Session, project: Project, payload):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    return project


def create_position(db: Session, payload):
    data = payload.model_dump()
    # 岗位锁定名额固定为 10，创建时不再自动从简历池搜索锁定
    data["target_resume_count"] = POSITION_LOCK_LIMIT
    tags = dict(data.get("requirement_tags") or {})
    tags["keyword"] = ""
    data["requirement_tags"] = tags
    obj = Position(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_position(db: Session, position: Position, payload):
    changes = payload.model_dump(exclude_unset=True)
    if "target_resume_count" in changes:
        changes["target_resume_count"] = POSITION_LOCK_LIMIT
    for key, value in changes.items():
        setattr(position, key, value)
    return position


def _parse_search_keyword_groups(keyword: str | None) -> list[list[str]]:
    if not keyword:
        return []
    groups: list[list[str]] = []
    for group in keyword.strip().lower().split():
        or_tokens = [part.strip() for part in re.split(r"[,|，]", group) if part.strip()]
        if or_tokens:
            groups.append(or_tokens)
    return groups


def _join_search_parts(parts: list) -> str:
    return " ".join(str(p) for p in parts if p).lower()


def _token_matches_text(token: str, text: str) -> bool:
    """短英文词（如 ai）用边界匹配，避免命中 AIGC/training 等。"""
    hay = (text or "").lower()
    needle = (token or "").lower()
    if not needle:
        return False
    if re.fullmatch(r"[a-z0-9]{1,2}", needle):
        return re.search(rf"(^|[^a-z0-9#+.]){re.escape(needle)}([^a-z0-9#+.]|$)", hay) is not None
    return needle in hay


def _candidate_l1_search_text(item: dict) -> str:
    """L1：岗位名（发布岗位名称 + 求职意向 + 当前/期望职位名，最高优先）。"""
    return _join_search_parts([item.get("job_posting_name"), item.get("job_intention"), item.get("current_title")])


def _candidate_l2_search_text(item: dict) -> str:
    """L2：工作/项目经历、核心价值、证书（职位名已在 L1）。"""
    return _join_search_parts(
        [
            item.get("work_history"),
            item.get("project_history"),
            item.get("core_value"),
            item.get("certificates"),
        ]
    )


def _candidate_search_text(item: dict) -> str:
    """岗位相关全文 = L1 + L2；姓名/手机/城市等不参与关键词匹配。"""
    return _join_search_parts([_candidate_l1_search_text(item), _candidate_l2_search_text(item)])


def _count_keyword_group_hits(text: str, groups: list[list[str]]) -> int:
    if not groups:
        return 0
    return sum(1 for or_tokens in groups if any(_token_matches_text(token, text) for token in or_tokens))


def _matches_search_keyword(text: str, keyword: str | None) -> bool:
    groups = _parse_search_keyword_groups(keyword)
    if not groups:
        return True
    return all(any(_token_matches_text(token, text) for token in or_tokens) for or_tokens in groups)


def _score_candidate_keyword_match(item: dict, keyword: str | None) -> tuple[int, int]:
    """返回 (L1命中组数, L2命中组数)，用于相关性排序。"""
    groups = _parse_search_keyword_groups(keyword)
    if not groups:
        return (0, 0)
    l1 = _count_keyword_group_hits(_candidate_l1_search_text(item), groups)
    l2 = _count_keyword_group_hits(_candidate_l2_search_text(item), groups)
    return (l1, l2)


def create_candidate(db: Session, payload):
    obj = Candidate(**payload.model_dump(exclude={"record_key"}))
    db.add(obj)
    return obj


def list_candidates(db: Session, keyword: str | None = None, city: str | None = None, status: str | None = None):
    from .models import RecruitResumeDownload, Candidate, RecruitJobPosting
    
    # 0. 查出 recruit.job_postings 建立 job_posting_id -> job_title 映射
    job_postings = db.query(RecruitJobPosting).all()
    job_posting_map = {jp.id: jp.job_title for jp in job_postings}

    # 1. 联合查询：用 SQLAlchemy 的 outerjoin 将抓取端的简历下载表与交付端扩展表进行 LEFT JOIN
    rows = db.query(RecruitResumeDownload, Candidate).outerjoin(
        Candidate, Candidate.candidate_agent_id == RecruitResumeDownload.candidate_agent_id
    ).all()

    # 2. 查出交付端纯手动创建（未绑定抓取端 ID）的候选人
    local_only = db.query(Candidate).filter(Candidate.candidate_agent_id == None).all()
    
    merged_results = []
    seen_candidate_ids = set()
    
    # 首先把纯手创的候选人放进结果集
    for c in local_only:
        if c.id in seen_candidate_ids:
            continue
        seen_candidate_ids.add(c.id)
            
        merged_results.append({
            "id": c.id,
            "name": c.name,
            "phone": c.phone,
            "email": c.email,
            "current_title": c.current_title,
            "city": c.city,
            "status": c.status,
            "delivery_status": c.delivery_status,
            "candidate_warranty_status": c.candidate_warranty_status,
            "source": c.source,
            "locked": c.locked,
            "gender": c.gender,
            "age": c.age,
            "education": c.education,
            "experience_years": c.experience_years,
            "expected_salary": c.expected_salary,
            "id_number": c.id_number,
            "tags": c.tags,
            "birth_date": c.birth_date,
            "hukou_location": c.hukou_location,
            "onboard_cycle": c.onboard_cycle,
            "education_detail": c.education_detail,
            "certificates": c.certificates,
            "comprehensive_evaluation": c.comprehensive_evaluation,
            "work_history": c.work_history,
            "core_value": c.core_value,
            "job_status": c.job_status,
            "family_status": c.family_status,
            "salary_structure": c.salary_structure,
            "job_intention": c.job_intention,
            "project_history": c.project_history,
            "job_posting_name": None,
            "candidate_agent_id": None,
            "record_key": f"candidate:{c.id}",
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S") if c.created_at else None,
            "file_path": getattr(c, "file_path", None) or None
        })
        
    # 处理联合查询的结果
    for d, c in rows:
        jp_name = job_posting_map.get(d.job_posting_id) if (d and d.job_posting_id) else None
        if c:
            if c.id in seen_candidate_ids:
                continue
            seen_candidate_ids.add(c.id)
                
            # 已关联的候选人，取交付表数据，并补充可能的抓取基本信息
            merged_results.append({
                "id": c.id,
                "name": c.name or d.candidate_name,
                "phone": c.phone,
                "email": c.email,
                "current_title": c.current_title or d.job_title,
                "city": c.city,
                "status": c.status,
                "delivery_status": c.delivery_status,
                "candidate_warranty_status": c.candidate_warranty_status,
                "source": c.source or "简历库",
                "locked": c.locked,
                "gender": c.gender,
                "age": c.age,
                "education": c.education,
                "experience_years": c.experience_years,
                "expected_salary": c.expected_salary,
                "id_number": c.id_number,
                "tags": c.tags,
                "birth_date": c.birth_date,
                "hukou_location": c.hukou_location,
                "onboard_cycle": c.onboard_cycle,
                "education_detail": c.education_detail,
                "certificates": c.certificates,
                "comprehensive_evaluation": c.comprehensive_evaluation,
                "work_history": c.work_history,
                "core_value": c.core_value,
                "job_status": c.job_status,
                "family_status": c.family_status,
                "salary_structure": c.salary_structure,
                "job_intention": c.job_intention,
                "project_history": c.project_history,
                "job_posting_name": jp_name,
                "candidate_agent_id": d.candidate_agent_id,
                "record_key": f"candidate:{c.id}",
                # 入池时间：优先用 recruit 抓取下载时间，否则用交付表创建时间
                "created_at": d.created_at or (c.created_at.strftime("%Y-%m-%d %H:%M:%S") if c.created_at else None),
                "file_path": getattr(c, "file_path", None) or d.file_path
            })
        else:
            # 纯抓取来的候选人，未同步，不做任何写入与硬编码硬塞值，独有字段全为 None
            merged_results.append({
                "id": d.id, # 整数虚拟 ID，直接使用下载记录 ID
                "name": d.candidate_name,
                "phone": None,
                "email": None,
                "current_title": d.job_title or "",
                "city": None,
                "status": "未锁定",
                "delivery_status": "未推荐",
                "candidate_warranty_status": "",
                "source": "简历库",
                "locked": False,
                "gender": None,
                "age": None,
                "education": "",
                "experience_years": None,
                "expected_salary": None,
                "id_number": None,
                "tags": None,
                "birth_date": None,
                "hukou_location": None,
                "onboard_cycle": None,
                "education_detail": None,
                "certificates": None,
                "comprehensive_evaluation": None,
                "work_history": None,
                "core_value": None,
                "job_status": None,
                "family_status": None,
                "salary_structure": None,
                "job_intention": None,
                "project_history": None,
                "job_posting_name": jp_name,
                "candidate_agent_id": d.candidate_agent_id,
                "record_key": f"download:{d.id}",
                "created_at": d.created_at,
                "file_path": d.file_path
            })

    # 4. 在内存中进行过滤
    filtered = []
    for item in merged_results:
        if keyword:
            text = _candidate_search_text(item)
            if not _matches_search_keyword(text, keyword):
                continue
        if city:
            if item["city"] != city:
                continue
        if status:
            if item["status"] != status:
                continue
        filtered.append(item)

    canonical_results: dict[str, dict] = {}
    for item in filtered:
        dedupe_key = _dedupe_key_for_item(item)
        item["record_key"] = item.get("record_key") or f"candidate:{item['id']}"
        current = canonical_results.get(dedupe_key)
        if current is None or _record_priority(item) > _record_priority(current):
            canonical_results[dedupe_key] = item

    def _sort_key(item: dict):
        created = _created_at_score(item.get("created_at"))
        cid = int(item.get("id") or 0)
        if keyword:
            l1, l2 = _score_candidate_keyword_match(item, keyword)
            # 期望岗位命中优先，其次 L2，再按创建时间
            return (l1, l2, created, cid)
        return (created, cid)

    return sorted(canonical_results.values(), key=_sort_key, reverse=True)


def ensure_local_candidate(db: Session, candidate_id: int | str) -> Candidate | None:
    from .models import RecruitCandidateProfile, RecruitResumeDownload, Candidate
    import re
    
    # 尝试把 candidate_id 解析为整数
    val = None
    key_type = None
    key_value = None
    candidate_key = str(candidate_id).strip()
    if candidate_key.startswith("candidate:"):
        key_type = "candidate"
        key_value = candidate_key.split(":", 1)[1].strip()
    elif candidate_key.startswith("download:"):
        key_type = "download"
        key_value = candidate_key.split(":", 1)[1].strip()
    elif candidate_key.startswith("agent:"):
        key_type = "agent"
        key_value = candidate_key.split(":", 1)[1].strip()
    else:
        key_value = candidate_key
    try:
        val = int(key_value)
    except ValueError:
        pass

    def _build_candidate(download: RecruitResumeDownload, profile: RecruitCandidateProfile, target_id: int | None):
        age_val = None
        if profile.candidate_age:
            m = re.search(r'\d+', profile.candidate_age)
            if m:
                age_val = int(m.group(0))

        kwargs = dict(
            name=profile.candidate_name,
            phone="",
            email="",
            current_title=download.job_title,
            city="",
            status="未锁定",
            source="简历库",
            gender="",
            age=age_val,
            education=profile.candidate_education or "",
            expected_salary="",
            tags="",
            candidate_agent_id=download.candidate_agent_id,
            file_path=download.file_path or "",
        )
        if target_id is not None:
            kwargs["id"] = target_id
        return Candidate(**kwargs)

    if val is not None:
        if key_type == "download":
            download = db.get(RecruitResumeDownload, val)
            if not download:
                return None
            profile = db.query(RecruitCandidateProfile).filter(RecruitCandidateProfile.candidate_agent_id == download.candidate_agent_id).first()
            if not profile:
                return None
            existing = db.query(Candidate).filter(Candidate.candidate_agent_id == download.candidate_agent_id).first()
            if existing:
                return existing
            existing_by_person = find_candidate_by_person(
                db,
                name=profile.candidate_name,
                phone=getattr(profile, "candidate_phone", "") or "",
                email=getattr(profile, "candidate_email", "") or "",
                file_path=download.file_path or "",
            )
            if existing_by_person:
                return existing_by_person
            target_id = val if db.get(Candidate, val) is None else None
            new_c = _build_candidate(download, profile, target_id)
            db.add(new_c)
            db.commit()
            db.refresh(new_c)
            return new_c

        # 1. 如果能转成整数，优先查交付表 Candidate 是否已落库
        existing = db.get(Candidate, val)
        if existing and (key_type != "candidate" or existing.id == val):
            return existing
            
        # 2. 若未落库，则以该 val (即 download.id) 去 resume_downloads 查找下载记录
        download = db.get(RecruitResumeDownload, val)
        if not download:
            return None
            
        # 3. 找到下载记录，拉取抓取表的完整 Profile
        agent_id = download.candidate_agent_id
        profile = db.query(RecruitCandidateProfile).filter(RecruitCandidateProfile.candidate_agent_id == agent_id).first()
        if not profile:
            return None
        existing_by_agent = db.query(Candidate).filter(Candidate.candidate_agent_id == agent_id).first()
        if existing_by_agent:
            return existing_by_agent
        existing_by_person = find_candidate_by_person(
            db,
            name=profile.candidate_name,
            phone=getattr(profile, "candidate_phone", "") or "",
            email=getattr(profile, "candidate_email", "") or "",
            file_path=download.file_path or "",
        )
        if existing_by_person:
            return existing_by_person
        target_id = val if db.get(Candidate, val) is None else None
        new_c = _build_candidate(download, profile, target_id)
        db.add(new_c)
        db.commit()
        db.refresh(new_c)
        return new_c
    else:
        # 如果是字符串形式的 key 或 agent_id
        if key_type == "candidate" and key_value and key_value.isdigit():
            candidate_obj = db.get(Candidate, int(key_value))
            if candidate_obj:
                return candidate_obj

        if key_type == "agent":
            agent_id = key_value or ""
        else:
            agent_id = key_value

        existing = db.query(Candidate).filter(Candidate.candidate_agent_id == agent_id).first()
        if existing:
            return existing
            
        profile = db.query(RecruitCandidateProfile).filter(RecruitCandidateProfile.candidate_agent_id == agent_id).first()
        if not profile:
            return None
            
        download = db.query(RecruitResumeDownload).filter(
            RecruitResumeDownload.candidate_agent_id == agent_id
        ).order_by(RecruitResumeDownload.created_at.desc()).first()
        if not download:
            return None
        existing_by_agent = db.query(Candidate).filter(Candidate.candidate_agent_id == agent_id).first()
        if existing_by_agent:
            return existing_by_agent
        existing_by_person = find_candidate_by_person(
            db,
            name=profile.candidate_name,
            phone=getattr(profile, "candidate_phone", "") or "",
            email=getattr(profile, "candidate_email", "") or "",
            file_path=download.file_path or "",
        )
        if existing_by_person:
            return existing_by_person
        target_id = download.id if db.get(Candidate, download.id) is None else None
        new_c = _build_candidate(download, profile, target_id)
        db.add(new_c)
        db.commit()
        db.refresh(new_c)
        return new_c


def update_candidate(db: Session, candidate: Candidate, payload):
    changes = payload.model_dump(exclude_unset=True)
    for key, value in changes.items():
        if key in {"locked", "status"}:
            continue
        setattr(candidate, key, value)
    return candidate


def sync_candidate_recommendation_state(db: Session, candidate: Candidate) -> Candidate:
    """从推荐记录反算候选人池摘要，禁止锁定状态与推荐进度各自漂移。"""
    employment = (
        db.query(EmploymentRecord)
        .filter(EmploymentRecord.candidate_id == candidate.id)
        .order_by(EmploymentRecord.created_at.desc(), EmploymentRecord.id.desc())
        .first()
    )
    if employment and employment.status == "已入职":
        candidate.locked = True
        candidate.status = "锁定"
        candidate.delivery_status = "已入职"
        db.add(candidate)
        return candidate

    recommendation = (
        db.query(Recommendation)
        .filter(Recommendation.candidate_id == candidate.id)
        .order_by(Recommendation.created_at.desc(), Recommendation.id.desc())
        .first()
    )
    if recommendation:
        candidate.locked = True
        candidate.status = "锁定"
        candidate.delivery_status = RECOMMENDATION_FLOW_STATUS_MAP.get(recommendation.status, "已推荐")
    else:
        candidate.locked = False
        candidate.status = "未锁定"
        candidate.delivery_status = "未推荐"
        candidate.owner_user_id = None
    db.add(candidate)
    return candidate


def sync_candidate_warranty_state(db: Session, candidate: Candidate) -> Candidate:
    """质保只由最新的已入职记录及其入职日期驱动。"""
    record = (
        db.query(EmploymentRecord)
        .filter(EmploymentRecord.candidate_id == candidate.id)
        .order_by(EmploymentRecord.created_at.desc(), EmploymentRecord.id.desc())
        .first()
    )
    if not record or record.status != "已入职" or not record.onboard_date:
        candidate.candidate_warranty_status = ""
        db.add(candidate)
        return candidate

    rule = db.query(WarrantyRule).filter(WarrantyRule.scope == "入职质保期").first()
    warranty_days = max(int(rule.months if rule else 6), 0) * 30
    onboard = record.onboard_date
    if onboard.tzinfo is None:
        onboard = onboard.replace(tzinfo=timezone.utc)
    candidate.candidate_warranty_status = (
        "质保到期" if datetime.now(timezone.utc) > onboard + timedelta(days=warranty_days) else "质保中"
    )
    db.add(candidate)
    return candidate


def reconcile_candidate_recommendation_states(db: Session) -> int:
    changed = 0
    for candidate in db.query(Candidate).all():
        before = (candidate.locked, candidate.status, candidate.delivery_status, candidate.candidate_warranty_status, candidate.owner_user_id)
        sync_candidate_recommendation_state(db, candidate)
        sync_candidate_warranty_state(db, candidate)
        after = (candidate.locked, candidate.status, candidate.delivery_status, candidate.candidate_warranty_status, candidate.owner_user_id)
        changed += int(before != after)
    return changed


def create_search_preset(db: Session, payload):
    obj = SearchPreset(**payload.model_dump())
    db.add(obj)
    return obj


def list_search_presets(db: Session):
    return db.query(SearchPreset).order_by(SearchPreset.created_at.desc()).all()


def lock_candidate(db: Session, candidate: Candidate, locked: bool):
    candidate.locked = locked
    candidate.status = "锁定" if locked else "未锁定"
    return candidate


def create_candidate_ownership_transfer(db: Session, payload):
    obj = CandidateOwnershipTransfer(**payload.model_dump())
    db.add(obj)
    return obj


def list_candidate_ownership_transfers(db: Session, candidate_id: int | None = None):
    query = db.query(CandidateOwnershipTransfer)
    if candidate_id is not None:
        query = query.filter(CandidateOwnershipTransfer.candidate_id == candidate_id)
    return query.order_by(CandidateOwnershipTransfer.created_at.desc()).all()


def approve_candidate_ownership_transfer(db: Session, record: CandidateOwnershipTransfer, approved_by_id: int | None = None):
    record.status = "已审批"
    record.approved_by_id = approved_by_id
    record.approved_at = datetime.now(timezone.utc)
    candidate = db.get(Candidate, record.candidate_id)
    if candidate:
        candidate.owner_user_id = record.to_user_id
        candidate.locked = True
        candidate.status = "锁定"
    return record


def create_tracking_event(db: Session, payload):
    obj = CandidateTrackingEvent(**payload.model_dump())
    db.add(obj)
    return obj


def list_tracking_events(db: Session, candidate_id: int | None = None):
    query = db.query(CandidateTrackingEvent)
    if candidate_id is not None:
      query = query.filter(CandidateTrackingEvent.candidate_id == candidate_id)
    return query.order_by(CandidateTrackingEvent.created_at.desc()).all()


def get_tracking_event(db: Session, event_id: int):
    return db.query(CandidateTrackingEvent).filter(CandidateTrackingEvent.id == event_id).first()


def update_tracking_event(db: Session, record: CandidateTrackingEvent, payload):
    for key, value in payload.model_dump().items():
        setattr(record, key, value)
    db.flush()
    return record


def delete_tracking_event(db: Session, record: CandidateTrackingEvent):
    db.delete(record)
    db.flush()


def create_interview_record(db: Session, payload):
    obj = InterviewRecord(**payload.model_dump())
    db.add(obj)
    return obj


def list_interview_records(db: Session, candidate_id: int | None = None):
    query = db.query(InterviewRecord)
    if candidate_id is not None:
      query = query.filter(InterviewRecord.candidate_id == candidate_id)
    return query.order_by(InterviewRecord.created_at.desc()).all()


def create_salary_record(db: Session, payload):
    obj = SalaryRecord(**payload.model_dump())
    db.add(obj)
    return obj


def update_salary_record(db: Session, record: SalaryRecord, payload):
    for key, value in payload.model_dump(exclude_unset=True).items():
        if key != 'candidate_id':
            setattr(record, key, value)
    return record


def list_salary_records(db: Session, candidate_id: int | None = None):
    query = db.query(SalaryRecord)
    if candidate_id is not None:
      query = query.filter(SalaryRecord.candidate_id == candidate_id)
    return query.order_by(SalaryRecord.created_at.desc()).all()


def create_employment_record(db: Session, payload):
    obj = EmploymentRecord(**payload.model_dump())
    db.add(obj)
    return obj


def update_employment_record(db: Session, record: EmploymentRecord, payload):
    for key, value in payload.model_dump(exclude_unset=True).items():
        if key != 'candidate_id':
            setattr(record, key, value)
    return record


def list_employment_records(db: Session, candidate_id: int | None = None):
    from sqlalchemy.orm import joinedload
    query = db.query(EmploymentRecord).options(joinedload(EmploymentRecord.candidate))
    if candidate_id is not None:
      query = query.filter(EmploymentRecord.candidate_id == candidate_id)
    return query.order_by(EmploymentRecord.created_at.desc()).all()


def create_candidate_follow_up_record(db: Session, payload):
    obj = CandidateFollowUpRecord(**payload.model_dump())
    db.add(obj)
    return obj


def list_candidate_follow_up_records(db: Session, candidate_id: int | None = None):
    query = db.query(CandidateFollowUpRecord)
    if candidate_id is not None:
        query = query.filter(CandidateFollowUpRecord.candidate_id == candidate_id)
    return query.order_by(CandidateFollowUpRecord.created_at.desc()).all()


def create_candidate_mail_record(db: Session, payload):
    obj = CandidateMailRecord(**payload.model_dump())
    db.add(obj)
    return obj


def list_candidate_mail_records(db: Session, candidate_id: int | None = None):
    query = db.query(CandidateMailRecord)
    if candidate_id is not None:
        query = query.filter(CandidateMailRecord.candidate_id == candidate_id)
    return query.order_by(CandidateMailRecord.created_at.desc()).all()


def create_export_record(db: Session, payload):
    obj = ExportRecord(**payload.model_dump())
    db.add(obj)
    return obj


def list_export_records(db: Session, candidate_id: int | None = None):
    query = db.query(ExportRecord)
    if candidate_id is not None:
        query = query.filter(ExportRecord.candidate_id == candidate_id)
    return query.order_by(ExportRecord.created_at.desc()).all()


def create_import_record(db: Session, payload):
    obj = ImportRecord(**payload.model_dump())
    db.add(obj)
    return obj


def list_import_records(db: Session):
    return db.query(ImportRecord).order_by(ImportRecord.created_at.desc()).all()


def create_recommendation(db: Session, payload):
    obj = Recommendation(**payload.model_dump())
    db.add(obj)
    return obj


def is_client_interview_round(interview_round: str | None) -> bool:
    """初筛是内部判断，不算客户侧面试；第N轮等才触发自动已推荐。"""
    value = str(interview_round or "").strip()
    if not value or value == "初筛":
        return False
    return True


def mark_recommendation_recommended(
    db: Session,
    recommendation: Recommendation,
    *,
    status: str = "已推荐",
    at: datetime | None = None,
) -> Recommendation:
    """将待推荐升为已推荐，并写入 recommended_at（只写一次）。"""
    now = at or datetime.now(timezone.utc)
    if recommendation.status == "待推荐":
        recommendation.status = status
    if recommendation.recommended_at is None and recommendation.status != "待推荐":
        recommendation.recommended_at = now
    db.add(recommendation)
    return recommendation


def resolve_recommendation_for_interview(
    db: Session,
    *,
    candidate_id: int,
    recommendation_id: int | None = None,
    position_id: int | None = None,
) -> Recommendation | None:
    if recommendation_id:
        obj = db.get(Recommendation, recommendation_id)
        if obj and obj.candidate_id == candidate_id:
            return obj
    query = db.query(Recommendation).filter(Recommendation.candidate_id == candidate_id)
    if position_id:
        query = query.filter(Recommendation.position_id == position_id)
    return query.order_by(Recommendation.created_at.desc(), Recommendation.id.desc()).first()


def promote_recommendation_on_interview(
    db: Session,
    *,
    candidate_id: int,
    interview_round: str | None = None,
    recommendation_id: int | None = None,
    position_id: int | None = None,
) -> Recommendation | None:
    if not is_client_interview_round(interview_round):
        return None
    recommendation = resolve_recommendation_for_interview(
        db,
        candidate_id=candidate_id,
        recommendation_id=recommendation_id,
        position_id=position_id,
    )
    if not recommendation:
        return None
    mark_recommendation_recommended(db, recommendation, status="已推荐")
    candidate = db.get(Candidate, candidate_id)
    if candidate:
        sync_candidate_recommendation_state(db, candidate)
    return recommendation


def list_recommendations(db: Session, candidate_id: int | None = None, position_id: int | None = None):
    query = db.query(Recommendation)
    if candidate_id is not None:
        query = query.filter(Recommendation.candidate_id == candidate_id)
    if position_id is not None:
        query = query.filter(Recommendation.position_id == position_id)
    return query.order_by(Recommendation.created_at.desc()).all()


def create_recommendation_feedback(db: Session, payload):
    obj = RecommendationFeedback(**payload.model_dump())
    db.add(obj)
    return obj


def list_recommendation_feedbacks(db: Session, recommendation_id: int | None = None):
    query = db.query(RecommendationFeedback)
    if recommendation_id is not None:
        query = query.filter(RecommendationFeedback.recommendation_id == recommendation_id)
    return query.order_by(RecommendationFeedback.created_at.desc()).all()


def create_delivery(db: Session, payload):
    obj = Delivery(recommendation_id=payload.recommendation_id, delivered_by=payload.delivered_by, channel=payload.channel, note=payload.note, delivered_at=datetime.now(timezone.utc))
    db.add(obj)
    return obj


def list_deliveries(db: Session, recommendation_id: int | None = None):
    query = db.query(Delivery)
    if recommendation_id is not None:
        query = query.filter(Delivery.recommendation_id == recommendation_id)
    return query.order_by(Delivery.delivered_at.desc()).all()


def create_evaluation(db: Session, payload):
    obj = Evaluation(**payload.model_dump())
    db.add(obj)
    return obj


def list_evaluations(db: Session, candidate_id: int | None = None):
    query = db.query(Evaluation)
    if candidate_id is not None:
        query = query.filter(Evaluation.candidate_id == candidate_id)
    return query.order_by(Evaluation.created_at.desc()).all()


def create_evaluation_level(db: Session, payload):
    obj = EvaluationLevel(**payload.model_dump())
    db.add(obj)
    return obj


def list_evaluation_levels(db: Session):
    return db.query(EvaluationLevel).order_by(EvaluationLevel.sort_order.asc(), EvaluationLevel.id.asc()).all()


def create_tag(db: Session, payload):
    data = payload.model_dump()
    object_type = str(data.get("object_type") or "candidate").strip() or "candidate"
    field_key = str(data.get("field_key") or "").strip()
    field_label = str(data.get("field_label") or data.get("name") or field_key).strip()
    style_key = str(data.get("style_key") or data.get("color") or "neutral").strip() or "neutral"
    sort_order = int(data.get("sort_order") or 0)
    data.update({
        "object_type": object_type,
        "field_key": field_key,
        "field_label": field_label,
        "style_key": style_key,
        "sort_order": sort_order,
        "category": TAG_OBJECT_LABELS.get(object_type, "标签字段"),
        "name": field_label,
        "color": style_key,
    })
    obj = TagDictionary(**data)
    db.add(obj)
    return obj


def update_tag(db: Session, tag: TagDictionary, payload):
    changes = payload.model_dump(exclude_unset=True)
    needs_normalize = any(key in changes for key in {"object_type", "field_key", "field_label", "style_key", "sort_order", "category", "name", "color"})
    for key, value in changes.items():
        setattr(tag, key, value)
    if needs_normalize:
        tag.object_type = str(tag.object_type or "candidate").strip() or "candidate"
        tag.field_key = str(tag.field_key or "").strip()
        tag.field_label = str(tag.field_label or tag.name or tag.field_key).strip()
        tag.style_key = str(tag.style_key or tag.color or "neutral").strip() or "neutral"
        tag.sort_order = int(tag.sort_order or 0)
        tag.category = TAG_OBJECT_LABELS.get(tag.object_type, "标签字段")
        tag.name = tag.field_label
        tag.color = tag.style_key
    return tag


def delete_tag(db: Session, tag: TagDictionary):
    db.delete(tag)
    return None


def list_tags(db: Session):
    return db.query(TagDictionary).filter(TagDictionary.field_key != "").order_by(TagDictionary.object_type.asc(), TagDictionary.sort_order.asc(), TagDictionary.id.asc()).all()


DEFAULT_SEARCH_HOTWORDS = [
    "销售",
    "课程顾问",
    "招聘",
    "行政",
    "客服",
    "Java",
    "前端",
    "产品经理",
]


def list_search_hotwords(db: Session, enabled_only: bool = False):
    query = db.query(SearchHotword)
    if enabled_only:
        query = query.filter(SearchHotword.enabled.is_(True))
    return query.order_by(SearchHotword.sort_order.asc(), SearchHotword.id.asc()).all()


def create_search_hotword(db: Session, payload):
    keyword = str(payload.keyword or "").strip()
    if not keyword:
        raise ValueError("热词不能为空")
    obj = SearchHotword(
        keyword=keyword[:64],
        sort_order=int(payload.sort_order or 0),
        enabled=bool(payload.enabled),
    )
    db.add(obj)
    return obj


def update_search_hotword(db: Session, item: SearchHotword, payload):
    changes = payload.model_dump(exclude_unset=True)
    if "keyword" in changes:
        keyword = str(changes["keyword"] or "").strip()
        if not keyword:
            raise ValueError("热词不能为空")
        changes["keyword"] = keyword[:64]
    for key, value in changes.items():
        setattr(item, key, value)
    return item


def delete_search_hotword(db: Session, item: SearchHotword):
    db.delete(item)
    return None


def ensure_default_search_hotwords(db: Session) -> int:
    """表为空时写入默认热词，返回新增条数。"""
    if db.query(SearchHotword).count() > 0:
        return 0
    for idx, keyword in enumerate(DEFAULT_SEARCH_HOTWORDS):
        db.add(SearchHotword(keyword=keyword, sort_order=idx * 10, enabled=True))
    db.flush()
    return len(DEFAULT_SEARCH_HOTWORDS)


def create_notification(db: Session, payload):
    obj = Notification(**payload.model_dump())
    db.add(obj)
    return obj


def list_notifications(
    db: Session,
    type: str | None = None,
    read: bool | None = None,
    keyword: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
):
    query = db.query(Notification)
    if type:
        query = query.filter(Notification.type == type)
    if read is not None:
        query = query.filter(Notification.read == read)
    if keyword:
        pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                Notification.user.like(pattern),
                Notification.title.like(pattern),
                Notification.type.like(pattern),
                Notification.target_path.like(pattern),
            )
        )
    if date_from:
        query = query.filter(Notification.created_at >= date_from)
    if date_to:
        query = query.filter(Notification.created_at <= date_to)
    return query.order_by(Notification.created_at.desc()).all()


def mark_notification_read(db: Session, notification: Notification):
    notification.read = True
    return notification


def create_warranty_rule(db: Session, payload):
    obj = WarrantyRule(**payload.model_dump())
    db.add(obj)
    return obj


def list_warranty_rules(db: Session):
    return db.query(WarrantyRule).order_by(WarrantyRule.scope.asc()).all()


def list_system_configs(db: Session):
    return db.query(SystemConfig).order_by(SystemConfig.key.asc()).all()


def upsert_system_config(db: Session, payload):
    obj = db.query(SystemConfig).filter(SystemConfig.key == payload.key).first()
    if obj:
        obj.value = payload.value
        obj.description = payload.description
    else:
        obj = SystemConfig(**payload.model_dump())
        db.add(obj)
    return obj


def get_email_config(db: Session):
    return db.query(EmailConfig).first()


def save_email_config(db: Session, payload):
    obj = db.query(EmailConfig).first()
    if obj:
        for key, value in payload.model_dump().items():
            setattr(obj, key, value)
    else:
        obj = EmailConfig(**payload.model_dump())
        db.add(obj)
    return obj


def test_email_config(payload):
    try:
        with socket.create_connection((payload.host, int(payload.port)), timeout=2):
            return True, "SMTP 连接成功"
    except Exception as exc:
        return False, f"SMTP 连接失败：{exc.__class__.__name__}"


def create_ai_task(db: Session, payload):
    output = f"RESULT<{payload.task_type}>:{payload.input_text[:64]}"
    obj = AiTask(task_type=payload.task_type, input_text=payload.input_text, output_text=output, status="完成")
    db.add(obj)
    return obj


def save_role_permission(db: Session, payload):
    obj = (
        db.query(RolePermission)
        .filter(RolePermission.role_code == payload.role_code, RolePermission.permission_key == payload.permission_key)
        .first()
    )
    if obj:
        obj.permission_type = payload.permission_type
        obj.module = payload.module
        obj.enabled = payload.enabled
    else:
        obj = RolePermission(**payload.model_dump())
        db.add(obj)
    return obj


def list_role_permissions(db: Session, role_code: str | None = None):
    query = db.query(RolePermission)
    if role_code:
        query = query.filter(RolePermission.role_code == role_code)
    return query.order_by(RolePermission.role_code.asc(), RolePermission.permission_key.asc()).all()


def save_data_permission(db: Session, payload):
    obj = (
        db.query(DataPermission)
        .filter(
            DataPermission.user_id == payload.user_id,
            DataPermission.scope_type == payload.scope_type,
            DataPermission.scope_id == payload.scope_id,
        )
        .first()
    )
    if obj:
        obj.scope_name = payload.scope_name
        obj.granted_by = payload.granted_by
        obj.active = payload.active
    else:
        obj = DataPermission(**payload.model_dump())
        db.add(obj)
    return obj


def list_data_permissions(db: Session, user_id: int | None = None):
    query = db.query(DataPermission)
    if user_id is not None:
        query = query.filter(DataPermission.user_id == user_id)
    return query.order_by(DataPermission.user_id.asc(), DataPermission.scope_type.asc()).all()


def list_ai_tasks(db: Session):
    return db.query(AiTask).order_by(AiTask.created_at.desc()).all()


def create_candidate_note(db: Session, payload):
    obj = CandidateNote(**payload.model_dump())
    db.add(obj)
    return obj


def list_candidate_notes(db: Session, candidate_id: int | None = None):
    query = db.query(CandidateNote)
    if candidate_id is not None:
        query = query.filter(CandidateNote.candidate_id == candidate_id)
    return query.order_by(CandidateNote.created_at.desc()).all()


def list_parse_keywords(db: Session, category: str | None = None, is_active: bool | None = None):
    query = db.query(RecruitParseKeyword)
    if category:
        query = query.filter(RecruitParseKeyword.category == category)
    if is_active is not None:
        query = query.filter(RecruitParseKeyword.is_active == is_active)
    rows = query.order_by(RecruitParseKeyword.id.asc()).all()
    
    # 若数据库尚无任何关键词记录，自动植入 8 个预置核心矩阵关键词
    if not rows and category is None and is_active is None:
        default_keywords = [
            ("education", "学历"),
            ("age", "年龄"),
            ("licenses", "证书"),
            ("industry", "行业"),
            ("job_category", "岗位"),
            ("skills", "技能"),
            ("awards", "获奖情况"),
            ("experience", "工作年限"),
        ]
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        for cat, kw in default_keywords:
            item = RecruitParseKeyword(category=cat, keyword=kw, is_active=True, created_at=now_str)
            db.add(item)
        db.commit()
        rows = db.query(RecruitParseKeyword).order_by(RecruitParseKeyword.id.asc()).all()

    return rows


def create_parse_keyword(db: Session, payload) -> RecruitParseKeyword:
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    obj = RecruitParseKeyword(
        category=payload.category if hasattr(payload, 'category') and payload.category else "general",
        keyword=payload.keyword.strip(),
        is_active=getattr(payload, 'is_active', True),
        created_at=now_str
    )
    db.add(obj)
    return obj


def update_parse_keyword(db: Session, keyword_id: int, payload) -> RecruitParseKeyword | None:
    obj = db.get(RecruitParseKeyword, keyword_id)
    if not obj:
        return None
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        if key == "keyword" and value is not None:
            value = value.strip()
        setattr(obj, key, value)
    db.add(obj)
    return obj


def delete_parse_keyword(db: Session, keyword_id: int) -> bool:
    obj = db.get(RecruitParseKeyword, keyword_id)
    if not obj:
        return False
    db.delete(obj)
    return True


def parse_jd_text_to_profile(jd_text: str, job_title: str = "", job_category: str = "", db: Session | None = None) -> dict:
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    
    # 动态查询用户在【解析关键词矩阵】中已勾选启用的关键词
    active_keywords = []
    if db:
        db_kws = list_parse_keywords(db, is_active=True)
        active_keywords = [item.keyword for item in db_kws if item.is_active]
    if not active_keywords:
        active_keywords = ["学历", "年龄", "证书", "行业", "岗位", "技能", "获奖情况", "工作年限"]

    # 尝试使用大模型 API (DeepSeek / OpenAI 规范) 进行大模型级精准解析
    llm_result = None
    try:
        from .config import get_deepseek_config
        base_url, api_key, model = get_deepseek_config()
        if api_key and api_key not in ("your_api_key_here", "replace_with_your_openrouter_key", "replace_with_your_deepseek_key"):
            from openai import OpenAI
            client = OpenAI(base_url=base_url, api_key=api_key)
            
            prompt = f"""你是资深招聘分析专家。
用户在配置矩阵中【已勾选启用】了以下需要从岗位描述 (JD) 中强抓取的【关注关键词列表】：
{json.dumps(active_keywords, ensure_ascii=False)}

请你分析输入的 JD 岗位描述文本，严格抓取与上述【关注关键词】相关的具体要求内容，并将提取出的内容结构化整理，填入【职位画像】中：
- 针对"年龄"、"学历"、"证书"、"工作年限"等硬性指标，填入 hard_requirements 字典中；
- 针对"技能"、"岗位"、"行业"、"获奖情况/其他"等优先能力项，提取核心词/短语填入 priority_requirements 画像对象中；
- 提取最能代表该岗位的 4~6 个精准搜索关键词填入 search_keywords。

必须严格返回 JSON 对象，格式如下：
{{
  "age_range": "例如 18-35岁 或 不限",
  "education": "例如 本科及以上",
  "special_licenses": "例如 必须有 / 无特殊要求",
  "job_category": "岗位类别名称",
  "industry": "行业名称",
  "skills": ["技能词1", "技能词2"],
  "experience": "工作年限与经验要求说明",
  "other": "获奖情况或其他重点要求说明",
  "search_keywords": ["搜索词1", "搜索词2"]
}}"""
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"岗位名称: {job_title}\nJD文本:\n{jd_text[:3000]}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
            )
            raw = response.choices[0].message.content or "{}"
            llm_result = json.loads(raw)
    except Exception:
        llm_result = None

    # 基础规则过滤与提取
    age_min, age_max = 16, 40
    age_match = re.search(r'(\d{2})[-~至到](\d{2})岁', jd_text)
    if age_match:
        age_min, age_max = int(age_match.group(1)), int(age_match.group(2))
    else:
        age_max_match = re.search(r'(\d{2})岁以[内下]', jd_text)
        if age_max_match:
            age_max = int(age_max_match.group(1))

    education = "不限"
    if "本科" in jd_text:
        education = "本科及以上"
    elif "大专" in jd_text:
        education = "大专及以上"
    elif "硕士" in jd_text:
        education = "硕士及以上"

    # 动态匹配用户在系统【解析关键词】中配置的词
    skills = []
    skill_candidates = category_map["skills"] if category_map["skills"] else ["办公软件", "沟通协作", "团队配合", "项目管理", "技术研发"]
    for sc in skill_candidates:
        if sc.lower() in jd_text.lower():
            skills.append(sc)
    if not skills:
        skills = skill_candidates[:3]

    category_name = job_category or job_title or (category_map["job_category"][0] if category_map["job_category"] else "通用岗位")
    for cat_item in category_map["job_category"]:
        if cat_item.lower() in jd_text.lower():
            category_name = cat_item
            break

    industry_name = category_map["industry"][0] if category_map["industry"] else "通用行业"
    for ind_item in category_map["industry"]:
        if ind_item.lower() in jd_text.lower():
            industry_name = ind_item
            break

    special_req = "无特殊要求"
    for lic in category_map["licenses"]:
        if lic.lower() in jd_text.lower():
            special_req = f"必须有{lic}"
            break
    if special_req == "无特殊要求" and ("证书" in jd_text or "特种" in jd_text or "登高" in jd_text or "电工" in jd_text):
        special_req = "必须有相关专业证书"

    # 大模型 LLM 成功解析时的结果融合
    if isinstance(llm_result, dict):
        age_range_str = llm_result.get("age_range") or f"{age_min}-{age_max}岁"
        edu_str = llm_result.get("education") or education
        license_str = llm_result.get("special_licenses") or special_req
        cat_str = llm_result.get("job_category") or category_name
        ind_str = llm_result.get("industry") or industry_name
        skill_tags = llm_result.get("skills") if isinstance(llm_result.get("skills"), list) and llm_result.get("skills") else skills
        exp_str = llm_result.get("experience") or "1-3年相关工作经验"
        other_str = llm_result.get("other") or "具备强烈的责任心与服务意识"
        search_kws = llm_result.get("search_keywords") if isinstance(llm_result.get("search_keywords"), list) and llm_result.get("search_keywords") else list(set(skills + [cat_str, ind_str]))[:6]

        return {
            "parsed_at": now_str,
            "raw_jd_text": jd_text,
            "hard_requirements": {
                "age_range": age_range_str,
                "age_min": age_min,
                "age_max": age_max,
                "education": edu_str,
                "special_licenses": license_str,
            },
            "priority_requirements": {
                "job_category": {"name": cat_str, "weight": 20.0},
                "industry": {"name": ind_str, "weight": 10.0},
                "skills": {"tags": skill_tags, "weight": 30.0},
                "experience": {"desc": exp_str, "weight": 20.0},
                "other": {"desc": other_str, "weight": 20.0},
            },
            "search_keywords": search_kws[:6],
            "use_portrait_weights": True,
        }

    return {
        "parsed_at": now_str,
        "raw_jd_text": jd_text,
        "hard_requirements": {
            "age_range": f"{age_min}-{age_max}岁",
            "age_min": age_min,
            "age_max": age_max,
            "education": education,
            "special_licenses": special_req,
        },
        "priority_requirements": {
            "job_category": {"name": category_name, "weight": 20.0},
            "industry": {"name": industry_name, "weight": 10.0},
            "skills": {"tags": skills, "weight": 30.0},
            "experience": {"desc": "1-3年相关工作经验", "weight": 20.0},
            "other": {"desc": "具备良好的沟通协同能力", "weight": 20.0},
        },
        "search_keywords": list(set(skills + [category_name, industry_name]))[:6],
        "use_portrait_weights": True,
    }


def create_or_update_job_profile(db: Session, job_posting_id: int | None, profile_data: dict) -> RecruitJobProfile:
    existing = None
    if job_posting_id:
        existing = db.query(RecruitJobProfile).filter(RecruitJobProfile.job_posting_id == job_posting_id).first()
    
    if existing:
        existing.raw_jd_text = profile_data.get("raw_jd_text", existing.raw_jd_text)
        existing.parsed_at = profile_data.get("parsed_at", existing.parsed_at)
        existing.hard_requirements = profile_data.get("hard_requirements", existing.hard_requirements)
        existing.priority_requirements = profile_data.get("priority_requirements", existing.priority_requirements)
        existing.search_keywords = profile_data.get("search_keywords", existing.search_keywords)
        existing.use_portrait_weights = profile_data.get("use_portrait_weights", True)
        db.add(existing)
        return existing
    else:
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        obj = RecruitJobProfile(
            job_posting_id=job_posting_id,
            raw_jd_text=profile_data.get("raw_jd_text", ""),
            parsed_at=profile_data.get("parsed_at", now_str),
            hard_requirements=profile_data.get("hard_requirements"),
            priority_requirements=profile_data.get("priority_requirements"),
            search_keywords=profile_data.get("search_keywords"),
            use_portrait_weights=profile_data.get("use_portrait_weights", True),
            created_at=now_str,
        )
        db.add(obj)
        return obj


def get_job_profile_by_posting_id(db: Session, job_posting_id: int) -> RecruitJobProfile | None:
    return db.query(RecruitJobProfile).filter(RecruitJobProfile.job_posting_id == job_posting_id).first()


