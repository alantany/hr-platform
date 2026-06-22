from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Role(Base, TimestampMixin):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(255), default="", nullable=False)


class RolePermission(Base, TimestampMixin):
    __tablename__ = "role_permissions"
    __table_args__ = (UniqueConstraint("role_code", "permission_key", name="uq_role_permission"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_code: Mapped[str] = mapped_column(String(32), nullable=False)
    permission_key: Mapped[str] = mapped_column(String(128), nullable=False)
    permission_type: Mapped[str] = mapped_column(String(32), default="menu", nullable=False)
    module: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class DataPermission(Base, TimestampMixin):
    __tablename__ = "data_permissions"
    __table_args__ = (UniqueConstraint("user_id", "scope_type", "scope_id", name="uq_data_permission"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    scope_type: Mapped[str] = mapped_column(String(32), nullable=False)
    scope_id: Mapped[str] = mapped_column(String(64), nullable=False)
    scope_name: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    granted_by: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Company(Base, TimestampMixin):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    contact_name: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    contact_phone: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    contact_email: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    address: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    cooperation_period: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="招聘中", nullable=False)
    remark: Mapped[str] = mapped_column(Text, default="", nullable=False)

    projects = relationship("Project", back_populates="company", cascade="all, delete-orphan")


class Project(Base, TimestampMixin):
    __tablename__ = "projects"
    __table_args__ = (UniqueConstraint("company_id", "name", name="uq_project_company_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="招聘中", nullable=False)
    level: Mapped[str] = mapped_column(String(16), default="A", nullable=False)
    hiring_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    work_location: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    project_period: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)

    company = relationship("Company", back_populates="projects")
    positions = relationship("Position", back_populates="project", cascade="all, delete-orphan")


class Position(Base, TimestampMixin):
    __tablename__ = "positions"
    __table_args__ = (UniqueConstraint("project_id", "name", name="uq_position_project_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    urgency: Mapped[str] = mapped_column(String(16), default="中", nullable=False)
    hiring_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    location: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="待招", nullable=False)
    age_requirement: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    education_requirement: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    experience_requirement: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)

    project = relationship("Project", back_populates="positions")
    recommendations = relationship("Recommendation", back_populates="position")


class Candidate(Base, TimestampMixin):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    phone: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    email: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    current_title: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    city: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="未锁定", nullable=False)
    source: Mapped[str] = mapped_column(String(64), default="导入", nullable=False)
    locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    gender: Mapped[str] = mapped_column(String(16), default="", nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    education: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    experience_years: Mapped[int | None] = mapped_column(Integer, nullable=True)
    expected_salary: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    id_number: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    tags: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    candidate_agent_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    # Resume template fields
    birth_date: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    hukou_location: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    onboard_cycle: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    education_detail: Mapped[str] = mapped_column(Text, default="", nullable=False)
    certificates: Mapped[str] = mapped_column(Text, default="", nullable=False)
    comprehensive_evaluation: Mapped[str] = mapped_column(Text, default="", nullable=False)
    work_history: Mapped[str] = mapped_column(Text, default="", nullable=False)
    core_value: Mapped[str] = mapped_column(Text, default="", nullable=False)
    job_status: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    family_status: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    salary_structure: Mapped[str] = mapped_column(Text, default="", nullable=False)
    job_intention: Mapped[str] = mapped_column(Text, default="", nullable=False)
    project_history: Mapped[str] = mapped_column(Text, default="", nullable=False)

    recommendations = relationship("Recommendation", back_populates="candidate")
    tracking_events = relationship("CandidateTrackingEvent", back_populates="candidate", cascade="all, delete-orphan")
    interview_records = relationship("InterviewRecord", back_populates="candidate", cascade="all, delete-orphan")
    salary_records = relationship("SalaryRecord", back_populates="candidate", cascade="all, delete-orphan")
    employment_records = relationship("EmploymentRecord", back_populates="candidate", cascade="all, delete-orphan")
    search_presets = relationship("SearchPreset", back_populates="candidate", cascade="all, delete-orphan")


class Recommendation(Base, TimestampMixin):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"), nullable=False)
    recommender: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="待推荐", nullable=False)
    feedback: Mapped[str] = mapped_column(Text, default="", nullable=False)
    customer_comment: Mapped[str] = mapped_column(Text, default="", nullable=False)

    candidate = relationship("Candidate", back_populates="recommendations")
    position = relationship("Position", back_populates="recommendations")
    deliveries = relationship("Delivery", back_populates="recommendation", cascade="all, delete-orphan")


class RecommendationFeedback(Base, TimestampMixin):
    __tablename__ = "recommendation_feedbacks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recommendation_id: Mapped[int] = mapped_column(ForeignKey("recommendations.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    feedback: Mapped[str] = mapped_column(Text, default="", nullable=False)
    customer_comment: Mapped[str] = mapped_column(Text, default="", nullable=False)
    operator: Mapped[str] = mapped_column(String(64), default="", nullable=False)

    recommendation = relationship("Recommendation")


class CandidateTrackingEvent(Base, TimestampMixin):
    __tablename__ = "candidate_tracking_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    summary: Mapped[str] = mapped_column(Text, default="", nullable=False)
    operator: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    position_id: Mapped[int | None] = mapped_column(ForeignKey("positions.id"), nullable=True)
    recommendation_id: Mapped[int | None] = mapped_column(ForeignKey("recommendations.id"), nullable=True)

    candidate = relationship("Candidate", back_populates="tracking_events")


class InterviewRecord(Base, TimestampMixin):
    __tablename__ = "interview_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    round_name: Mapped[str] = mapped_column(String(32), default="第1轮", nullable=False)
    result: Mapped[str] = mapped_column(String(32), default="未进行", nullable=False)
    interviewer: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    interview_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    note: Mapped[str] = mapped_column(Text, default="", nullable=False)

    candidate = relationship("Candidate", back_populates="interview_records")


class SalaryRecord(Base, TimestampMixin):
    __tablename__ = "salary_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    expected_salary: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    offered_salary: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    service_status: Mapped[str] = mapped_column(String(32), default="未进行", nullable=False)
    note: Mapped[str] = mapped_column(Text, default="", nullable=False)

    candidate = relationship("Candidate", back_populates="salary_records")


class EmploymentRecord(Base, TimestampMixin):
    __tablename__ = "employment_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="未入职", nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    position_name: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    onboard_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    note: Mapped[str] = mapped_column(Text, default="", nullable=False)

    candidate = relationship("Candidate", back_populates="employment_records")


class CandidateFollowUpRecord(Base, TimestampMixin):
    __tablename__ = "candidate_follow_up_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="已录用", nullable=False)
    follow_up_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    content: Mapped[str] = mapped_column(Text, default="", nullable=False)
    operator: Mapped[str] = mapped_column(String(64), default="", nullable=False)

    candidate = relationship("Candidate")


class CandidateMailRecord(Base, TimestampMixin):
    __tablename__ = "candidate_mail_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    recipient_email: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    mail_subject: Mapped[str] = mapped_column(String(255), nullable=False)
    mail_body: Mapped[str] = mapped_column(Text, default="", nullable=False)
    attachment_name: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    sent_by: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="已发送", nullable=False)

    candidate = relationship("Candidate")


class SearchPreset(Base, TimestampMixin):
    __tablename__ = "search_presets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int | None] = mapped_column(ForeignKey("candidates.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    keyword: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    city: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    created_by: Mapped[str] = mapped_column(String(64), default="", nullable=False)

    candidate = relationship("Candidate", back_populates="search_presets")


class ExportRecord(Base, TimestampMixin):
    __tablename__ = "export_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(Integer, nullable=False)
    candidate_name: Mapped[str] = mapped_column(String(128), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    project_name: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    position_name: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    format: Mapped[str] = mapped_column(String(16), default="PDF", nullable=False)
    watermarked: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    exported_by: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), default="", nullable=False)


class ImportRecord(Base, TimestampMixin):
    __tablename__ = "import_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    imported_by: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    imported_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    failed_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="成功", nullable=False)
    note: Mapped[str] = mapped_column(Text, default="", nullable=False)


class Delivery(Base, TimestampMixin):
    __tablename__ = "deliveries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recommendation_id: Mapped[int] = mapped_column(ForeignKey("recommendations.id"), nullable=False)
    delivered_by: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    delivered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    channel: Mapped[str] = mapped_column(String(32), default="系统交付", nullable=False)
    note: Mapped[str] = mapped_column(Text, default="", nullable=False)

    recommendation = relationship("Recommendation", back_populates="deliveries")


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor: Mapped[str] = mapped_column(String(64), nullable=False)
    module: Mapped[str] = mapped_column(String(64), nullable=False)
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    target_type: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    target_id: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    result: Mapped[str] = mapped_column(String(32), default="成功", nullable=False)
    detail: Mapped[str] = mapped_column(Text, default="", nullable=False)


class Evaluation(Base, TimestampMixin):
    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"), nullable=False, default=1)
    evaluator: Mapped[str] = mapped_column(String(64), nullable=False)
    round_name: Mapped[str] = mapped_column(String(32), default="第1轮", nullable=False)
    grade: Mapped[str] = mapped_column(String(32), nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    content: Mapped[str] = mapped_column(Text, default="", nullable=False)


class EvaluationLevel(Base, TimestampMixin):
    __tablename__ = "evaluation_levels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    color: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class TagDictionary(Base, TimestampMixin):
    __tablename__ = "tag_dictionaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    color: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(64), nullable=False)
    read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    target_path: Mapped[str] = mapped_column(String(255), default="", nullable=False)


class WarrantyRule(Base, TimestampMixin):
    __tablename__ = "warranty_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scope: Mapped[str] = mapped_column(String(32), nullable=False)
    months: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    remind_days: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    auto_expire: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class SystemConfig(Base, TimestampMixin):
    __tablename__ = "system_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    value: Mapped[str] = mapped_column(Text, default="", nullable=False)
    description: Mapped[str] = mapped_column(String(255), default="", nullable=False)


class EmailConfig(Base, TimestampMixin):
    __tablename__ = "email_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    host: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    port: Mapped[int] = mapped_column(Integer, default=25, nullable=False)
    sender: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    username: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    password: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    use_tls: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class AiTask(Base, TimestampMixin):
    __tablename__ = "ai_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_type: Mapped[str] = mapped_column(String(64), nullable=False)
    input_text: Mapped[str] = mapped_column(Text, default="", nullable=False)
    output_text: Mapped[str] = mapped_column(Text, default="", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="完成", nullable=False)


class RecruitCandidateProfile(Base):
    __tablename__ = "candidate_profiles"
    __table_args__ = {"schema": "recruit"}

    candidate_agent_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    candidate_name: Mapped[str] = mapped_column(String(255), nullable=False)
    candidate_age: Mapped[str | None] = mapped_column(String(64), nullable=True)
    candidate_education: Mapped[str | None] = mapped_column(String(64), nullable=True)
    updated_at: Mapped[str] = mapped_column(String(64), nullable=False)


class RecruitResumeDownload(Base):
    __tablename__ = "resume_downloads"
    __table_args__ = {"schema": "recruit"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_posting_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    candidate_agent_id: Mapped[str] = mapped_column(String(255), nullable=False)
    candidate_name: Mapped[str] = mapped_column(String(255), nullable=False)
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    issuer_login_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    time_folder: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[str] = mapped_column(String(64), nullable=False)


class RecruitEmployee(Base):
    __tablename__ = "employees"
    __table_args__ = {"schema": "recruit"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[str] = mapped_column(String(64), nullable=False)
    updated_at: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_admin: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class RecruitJobPosting(Base):
    __tablename__ = "job_postings"
    __table_args__ = {"schema": "recruit"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[int] = mapped_column(Integer, nullable=False)
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    work_location: Mapped[str] = mapped_column(String(255), nullable=False)
    age_requirement: Mapped[str | None] = mapped_column(String(255), nullable=True)
    education: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[str] = mapped_column(String(64), nullable=False)
    age_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    age_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    candidate_activity: Mapped[str] = mapped_column(String(64), nullable=False)
    daily_greet_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    search_keyword: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_valid: Mapped[str] = mapped_column(String(8), nullable=False)


class RecruitDailyTaskStat(Base):
    __tablename__ = "daily_task_stats"
    __table_args__ = {"schema": "recruit"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stat_date: Mapped[str] = mapped_column(String(64), nullable=False)
    job_posting_id: Mapped[int] = mapped_column(Integer, nullable=False)
    issuer_login_name: Mapped[str] = mapped_column(String(255), nullable=False)
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    greet_count: Mapped[int] = mapped_column(Integer, nullable=False)
    resume_request_count: Mapped[int] = mapped_column(Integer, nullable=False)
    resume_download_count: Mapped[int] = mapped_column(Integer, nullable=False)
    resume_ack_count: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[str] = mapped_column(String(64), nullable=False)

