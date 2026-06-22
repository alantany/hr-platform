from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class CurrentUser(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    is_active: bool


class UserCreate(BaseModel):
    username: str
    full_name: str
    password_hash: str = "dev"
    role: str = "操作员"
    is_active: bool = True


class UserOut(UserCreate):
    id: int


class UserUpdate(BaseModel):
    full_name: str | None = None
    password_hash: str | None = None
    role: str | None = None
    is_active: bool | None = None


class UserResetPassword(BaseModel):
    password_hash: str


class RoleCreate(BaseModel):
    code: str
    name: str
    description: str = ""


class RoleOut(RoleCreate):
    id: int


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class RolePermissionCreate(BaseModel):
    role_code: str
    permission_key: str
    permission_type: str = "menu"
    module: str = ""
    enabled: bool = True


class RolePermissionOut(RolePermissionCreate):
    id: int


class DataPermissionCreate(BaseModel):
    user_id: int
    scope_type: str
    scope_id: str
    scope_name: str = ""
    granted_by: str = ""
    active: bool = True


class DataPermissionOut(DataPermissionCreate):
    id: int


class DashboardSummary(BaseModel):
    candidate_count: int
    company_count: int
    project_count: int
    position_count: int
    user_count: int
    recommendation_count: int
    delivery_count: int
    audit_log_count: int


class DashboardTodoOut(BaseModel):
    title: str
    meta: str
    tag: str
    color: str
    source: str = ""
    target_path: str = ""


class CompanyCreate(BaseModel):
    name: str
    contact_name: str = ""
    contact_phone: str = ""
    contact_email: str = ""
    address: str = ""
    cooperation_period: str = ""
    status: str = "招聘中"
    remark: str = ""


class CompanyOut(CompanyCreate):
    id: int


class CompanyUpdate(BaseModel):
    name: str | None = None
    contact_name: str | None = None
    contact_phone: str | None = None
    contact_email: str | None = None
    address: str | None = None
    cooperation_period: str | None = None
    status: str | None = None
    remark: str | None = None


class ProjectCreate(BaseModel):
    company_id: int
    name: str
    status: str = "招聘中"
    level: str = "A"
    hiring_count: int = 1
    work_location: str = ""
    project_period: str = ""
    description: str = ""


class ProjectOut(ProjectCreate):
    id: int
    company_name: str = ""


class ProjectUpdate(BaseModel):
    company_id: int | None = None
    name: str | None = None
    status: str | None = None
    level: str | None = None
    hiring_count: int | None = None
    work_location: str | None = None
    project_period: str | None = None
    description: str | None = None


class PositionCreate(BaseModel):
    project_id: int
    name: str
    urgency: str = "中"
    hiring_count: int = 1
    salary_min: int | None = None
    salary_max: int | None = None
    location: str = ""
    status: str = "待招"
    age_requirement: str = ""
    education_requirement: str = ""
    experience_requirement: str = ""
    description: str = ""


class PositionOut(PositionCreate):
    id: int


class PositionUpdate(BaseModel):
    project_id: int | None = None
    name: str | None = None
    urgency: str | None = None
    hiring_count: int | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    location: str | None = None
    status: str | None = None
    age_requirement: str | None = None
    education_requirement: str | None = None
    experience_requirement: str | None = None
    description: str | None = None


class CandidateCreate(BaseModel):
    name: str
    phone: str | None = ""
    email: str | None = ""
    current_title: str | None = ""
    city: str | None = ""
    status: str | None = "新入库"
    source: str | None = "手动创建"
    locked: bool | None = False
    gender: str | None = ""
    age: int | None = None
    education: str | None = ""
    experience_years: int | None = None
    expected_salary: str | None = ""
    id_number: str | None = ""
    tags: str | None = ""
    candidate_agent_id: str | None = None
    
    # Resume template fields
    birth_date: str | None = ""
    hukou_location: str | None = ""
    onboard_cycle: str | None = ""
    education_detail: str | None = ""
    certificates: str | None = ""
    comprehensive_evaluation: str | None = ""
    work_history: str | None = ""
    core_value: str | None = ""
    job_status: str | None = ""
    family_status: str | None = ""
    salary_structure: str | None = ""
    job_intention: str | None = ""
    project_history: str | None = ""


class CandidateOut(CandidateCreate):
    id: int | str
    created_at: datetime | str | None = None
    file_path: str | None = None

    @field_validator('phone', mode='after')
    @classmethod
    def mask_phone(cls, v: str | None) -> str | None:
        if not v:
            return ""
        if len(v) == 11:
            return v[:3] + "****" + v[7:]
        elif len(v) > 4:
            return v[:-4] + "****"
        return v


class CandidateTrackingEventCreate(BaseModel):
    candidate_id: int
    event_type: str
    status: str = ""
    summary: str = ""
    operator: str = ""
    position_id: int | None = None
    recommendation_id: int | None = None


class CandidateTrackingEventOut(CandidateTrackingEventCreate):
    id: int
    created_at: datetime


class InterviewRecordCreate(BaseModel):
    candidate_id: int
    round_name: str = "第1轮"
    result: str = "未进行"
    interviewer: str = ""
    interview_time: datetime | None = None
    note: str = ""


class InterviewRecordOut(InterviewRecordCreate):
    id: int
    created_at: datetime


class SalaryRecordCreate(BaseModel):
    candidate_id: int | str
    expected_salary: str = ""
    offered_salary: str = ""
    service_status: str = "未进行"
    note: str = ""


class SalaryRecordOut(SalaryRecordCreate):
    id: int
    created_at: datetime


class EmploymentRecordCreate(BaseModel):
    candidate_id: int | str
    status: str = "未入职"
    company_name: str = ""
    position_name: str = ""
    onboard_date: datetime | None = None
    note: str = ""


class EmploymentRecordOut(EmploymentRecordCreate):
    id: int
    created_at: datetime


class CandidateFollowUpRecordCreate(BaseModel):
    candidate_id: int | str
    status: str = "已录用"
    follow_up_time: datetime | None = None
    content: str = ""
    operator: str = ""


class CandidateFollowUpRecordOut(CandidateFollowUpRecordCreate):
    id: int
    created_at: datetime


class CandidateMailRecordCreate(BaseModel):
    candidate_id: int | str
    recipient_email: str
    mail_subject: str
    mail_body: str = ""
    attachment_name: str = ""
    sent_by: str = ""
    status: str = "已发送"


class CandidateMailRecordOut(CandidateMailRecordCreate):
    id: int
    created_at: datetime


class ExportRecordCreate(BaseModel):
    candidate_id: int
    candidate_name: str
    company_name: str = ""
    project_name: str = ""
    position_name: str = ""
    format: str = "PDF"
    watermarked: bool = True
    exported_by: str = ""
    file_name: str = ""
    file_path: str = ""


class ExportRecordOut(ExportRecordCreate):
    id: int
    created_at: datetime


class ImportRecordCreate(BaseModel):
    file_name: str
    imported_by: str = ""
    imported_count: int = 1
    failed_count: int = 0
    status: str = "成功"
    note: str = ""


class ImportRecordOut(ImportRecordCreate):
    id: int
    created_at: datetime


class CandidateUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    current_title: str | None = None
    city: str | None = None
    status: str | None = None
    source: str | None = None
    locked: bool | None = None
    gender: str | None = None
    age: int | None = None
    education: str | None = None
    experience_years: int | None = None
    expected_salary: str | None = None
    id_number: str | None = None
    tags: str | None = None
    
    # Resume template fields
    birth_date: str | None = None
    hukou_location: str | None = None
    onboard_cycle: str | None = None
    education_detail: str | None = None
    certificates: str | None = None
    comprehensive_evaluation: str | None = None
    work_history: str | None = None
    core_value: str | None = None
    job_status: str | None = None
    family_status: str | None = None
    salary_structure: str | None = None
    job_intention: str | None = None
    project_history: str | None = None


class SearchPresetCreate(BaseModel):
    name: str
    keyword: str = ""
    city: str = ""
    status: str = ""
    created_by: str = "admin"


class SearchPresetOut(SearchPresetCreate):
    id: int


class RecommendationCreate(BaseModel):
    candidate_id: int
    position_id: int
    recommender: str = ""
    status: str = "待推荐"
    feedback: str = ""


class RecommendationOut(RecommendationCreate):
    id: int


class RecommendationUpdate(BaseModel):
    status: str | None = None
    feedback: str | None = None
    customer_comment: str | None = None


class DeliveryCreate(BaseModel):
    recommendation_id: int
    delivered_by: str = ""
    channel: str = "系统交付"
    note: str = ""


class DeliveryOut(DeliveryCreate):
    id: int
    delivered_at: datetime


class RecommendationFeedbackCreate(BaseModel):
    recommendation_id: int
    status: str
    feedback: str = ""
    customer_comment: str = ""
    operator: str = ""


class RecommendationFeedbackOut(RecommendationFeedbackCreate):
    id: int
    created_at: datetime


class AuditLogOut(BaseModel):
    id: int
    actor: str
    module: str
    action: str
    target_type: str
    target_id: str
    result: str
    detail: str
    created_at: datetime


class EvaluationCreate(BaseModel):
    candidate_id: int
    position_id: int = 1
    evaluator: str
    round_name: str = "第1轮"
    grade: str
    score: int = 5
    content: str = ""


class EvaluationOut(EvaluationCreate):
    id: int
    created_at: datetime


class EvaluationLevelCreate(BaseModel):
    name: str
    score: int
    description: str = ""
    color: str = ""
    sort_order: int = 0
    enabled: bool = True


class EvaluationLevelOut(EvaluationLevelCreate):
    id: int


class TagCreate(BaseModel):
    category: str
    name: str
    color: str = ""
    enabled: bool = True


class TagOut(TagCreate):
    id: int


class TagUpdate(BaseModel):
    category: str | None = None
    name: str | None = None
    color: str | None = None
    enabled: bool | None = None


class NotificationCreate(BaseModel):
    user: str
    title: str
    type: str
    target_path: str = ""


class NotificationOut(NotificationCreate):
    id: int
    read: bool
    created_at: datetime


class WarrantyRuleCreate(BaseModel):
    scope: str
    months: int = 3
    remind_days: int = 10
    auto_expire: bool = True


class WarrantyRuleOut(WarrantyRuleCreate):
    id: int


class SystemConfigCreate(BaseModel):
    key: str
    value: str = ""
    description: str = ""


class SystemConfigOut(SystemConfigCreate):
    id: int


class EmailConfigCreate(BaseModel):
    host: str = ""
    port: int = 25
    sender: str = ""
    username: str = ""
    password: str = ""
    use_tls: bool = True
    enabled: bool = True


class EmailConfigOut(EmailConfigCreate):
    id: int


class EmailConfigTestResult(BaseModel):
    ok: bool
    message: str


class AiTaskCreate(BaseModel):
    task_type: str
    input_text: str = ""


class AiTaskOut(AiTaskCreate):
    id: int
    output_text: str
    status: str


class RecruitCandidateProfileOut(BaseModel):
    candidate_agent_id: str
    candidate_name: str
    candidate_age: str | None = None
    candidate_education: str | None = None
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class RecruitResumeDownloadOut(BaseModel):
    id: int
    job_posting_id: int | None = None
    candidate_agent_id: str
    candidate_name: str
    job_title: str
    file_path: str
    issuer_login_name: str | None = None
    time_folder: str | None = None
    created_at: str

    model_config = ConfigDict(from_attributes=True)

