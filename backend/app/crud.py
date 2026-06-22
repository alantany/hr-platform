from __future__ import annotations

from datetime import datetime, timezone
import socket

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from .models import AuditLog, AiTask, Candidate, CandidateFollowUpRecord, CandidateMailRecord, CandidateTrackingEvent, Company, DataPermission, Delivery, EmailConfig, EmploymentRecord, Evaluation, EvaluationLevel, ExportRecord, ImportRecord, InterviewRecord, Notification, Position, Project, Recommendation, RecommendationFeedback, Role, RolePermission, SalaryRecord, SearchPreset, SystemConfig, TagDictionary, User, WarrantyRule


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


def dashboard_summary(db: Session) -> dict:
    return {
        "candidate_count": db.query(func.count(Candidate.id)).scalar() or 0,
        "company_count": db.query(func.count(Company.id)).scalar() or 0,
        "project_count": db.query(func.count(Project.id)).scalar() or 0,
        "position_count": db.query(func.count(Position.id)).scalar() or 0,
        "user_count": db.query(func.count(User.id)).scalar() or 0,
        "recommendation_count": db.query(func.count(Recommendation.id)).scalar() or 0,
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
            "color": "green" if rec.status in {"客户已收", "安排面试", "已录用"} else "orange",
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
    obj = User(**payload.model_dump())
    db.add(obj)
    return obj


def update_user(db: Session, user: User, payload):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    return user


def reset_user_password(db: Session, user: User, payload):
    user.password_hash = payload.password_hash
    return user


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
    obj = Position(**payload.model_dump())
    db.add(obj)
    return obj


def update_position(db: Session, position: Position, payload):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(position, key, value)
    return position


def create_candidate(db: Session, payload):
    obj = Candidate(**payload.model_dump())
    db.add(obj)
    return obj


def list_candidates(db: Session, keyword: str | None = None, city: str | None = None, status: str | None = None):
    from .models import RecruitCandidateProfile, RecruitResumeDownload, Candidate
    
    # 1. 联合查询：用 SQLAlchemy 的 outerjoin 将抓取端主表与交付端扩展表进行 LEFT JOIN
    rows = db.query(RecruitCandidateProfile, Candidate).outerjoin(
        Candidate, Candidate.candidate_agent_id == RecruitCandidateProfile.candidate_agent_id
    ).all()
    
    # 2. 查出交付端纯手动创建（未绑定抓取端 ID）的候选人
    local_only = db.query(Candidate).filter(Candidate.candidate_agent_id == None).all()
    
    merged_results = []
    
    # 首先把纯手创的候选人放进结果集
    for c in local_only:
        merged_results.append({
            "id": c.id,
            "name": c.name,
            "phone": c.phone,
            "email": c.email,
            "current_title": c.current_title,
            "city": c.city,
            "status": c.status,
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
            "candidate_agent_id": None,
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S") if c.created_at else None,
            "file_path": None
        })
        
    # 处理联合查询的结果
    for p, c in rows:
        download = db.query(RecruitResumeDownload).filter(
            RecruitResumeDownload.candidate_agent_id == p.candidate_agent_id
        ).order_by(RecruitResumeDownload.created_at.desc()).first()
        
        import re
        age_val = None
        if p.candidate_age:
            m = re.search(r'\d+', p.candidate_age)
            if m:
                age_val = int(m.group(0))
                
        if c:
            # 已关联的候选人，取交付表数据，并补充可能的抓取基本信息
            merged_results.append({
                "id": c.id,
                "name": c.name or p.candidate_name,
                "phone": c.phone,
                "email": c.email,
                "current_title": c.current_title or (download.job_title if download else ""),
                "city": c.city,
                "status": c.status,
                "source": c.source or "智联抓取",
                "locked": c.locked,
                "gender": c.gender,
                "age": c.age or age_val,
                "education": c.education or p.candidate_education or "",
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
                "candidate_agent_id": p.candidate_agent_id,
                "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S") if c.created_at else (download.created_at if download else p.updated_at),
                "file_path": download.file_path if download else None
            })
        else:
            # 纯抓取来的候选人，未同步，不做任何写入与硬编码硬塞值，独有字段全为 None
            merged_results.append({
                "id": download.id if download else p.candidate_agent_id, # 整数虚拟 ID，直接使用下载记录 ID；无下载记录时以 agent_id 兜底
                "name": p.candidate_name,
                "phone": None,
                "email": None,
                "current_title": download.job_title if download else "",
                "city": None,
                "status": "未锁定",
                "source": "智联抓取",
                "locked": False,
                "gender": None,
                "age": age_val,
                "education": p.candidate_education or "",
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
                "candidate_agent_id": p.candidate_agent_id,
                "created_at": download.created_at if download else p.updated_at,
                "file_path": download.file_path if download else None
            })

    # 4. 在内存中进行过滤
    filtered = []
    for item in merged_results:
        if keyword:
            pattern = keyword.lower()
            match = (
                pattern in (item["name"] or "").lower() or
                pattern in (item["phone"] or "").lower() or
                pattern in (item["current_title"] or "").lower() or
                pattern in (item["city"] or "").lower() or
                pattern in (item["source"] or "").lower()
            )
            if not match:
                continue
        if city:
            if item["city"] != city:
                continue
        if status:
            if item["status"] != status:
                continue
        filtered.append(item)
    return filtered
def ensure_local_candidate(db: Session, candidate_id: int | str) -> Candidate | None:
    from .models import RecruitCandidateProfile, RecruitResumeDownload, Candidate
    import re
    
    # 尝试把 candidate_id 解析为整数
    val = None
    try:
        val = int(candidate_id)
    except ValueError:
        pass
        
    if val is not None:
        # 1. 如果能转成整数，优先查交付表 Candidate 是否已落库
        existing = db.get(Candidate, val)
        if existing:
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
            
        age_val = None
        if profile.candidate_age:
            m = re.search(r'\d+', profile.candidate_age)
            if m:
                age_val = int(m.group(0))
                
        # 4. 显式指定 id=val 创建交付表记录，实现主键一致
        new_c = Candidate(
            id=val,
            name=profile.candidate_name,
            phone="",
            email="",
            current_title=download.job_title,
            city="",
            status="未锁定",
            source="智联抓取",
            gender="",
            age=age_val,
            education=profile.candidate_education or "",
            expected_salary="",
            tags="",
            candidate_agent_id=agent_id
        )
        db.add(new_c)
        db.commit()
        db.refresh(new_c)
        return new_c
    else:
        # 如果是字符串形式的 agent_id (即 "C_xxx")
        agent_id = str(candidate_id)
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
            
        age_val = None
        if profile.candidate_age:
            m = re.search(r'\d+', profile.candidate_age)
            if m:
                age_val = int(m.group(0))
                
        # 也是显式指定 id=download.id 插入
        new_c = Candidate(
            id=download.id,
            name=profile.candidate_name,
            phone="",
            email="",
            current_title=download.job_title,
            city="",
            status="未锁定",
            source="智联抓取",
            gender="",
            age=age_val,
            education=profile.candidate_education or "",
            expected_salary="",
            tags="",
            candidate_agent_id=agent_id
        )
        db.add(new_c)
        db.commit()
        db.refresh(new_c)
        return new_c


def update_candidate(db: Session, candidate: Candidate, payload):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(candidate, key, value)
    return candidate


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


def create_tracking_event(db: Session, payload):
    obj = CandidateTrackingEvent(**payload.model_dump())
    db.add(obj)
    return obj


def list_tracking_events(db: Session, candidate_id: int | None = None):
    query = db.query(CandidateTrackingEvent)
    if candidate_id is not None:
      query = query.filter(CandidateTrackingEvent.candidate_id == candidate_id)
    return query.order_by(CandidateTrackingEvent.created_at.desc()).all()


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
    query = db.query(EmploymentRecord)
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
    obj = TagDictionary(**payload.model_dump())
    db.add(obj)
    return obj


def update_tag(db: Session, tag: TagDictionary, payload):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(tag, key, value)
    return tag


def delete_tag(db: Session, tag: TagDictionary):
    db.delete(tag)
    return None


def list_tags(db: Session):
    return db.query(TagDictionary).order_by(TagDictionary.category.asc(), TagDictionary.name.asc()).all()


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
