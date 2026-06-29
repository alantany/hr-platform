from __future__ import annotations

from pathlib import Path

from sqlalchemy.orm import Session

from backend.app.database import Base, SessionLocal, engine
from backend.app.models import AuditLog, AiTask, Candidate, CandidateTrackingEvent, Company, DataPermission, Delivery, EmailConfig, EmploymentRecord, Evaluation, ExportRecord, ImportRecord, InterviewRecord, Notification, Position, Project, Recommendation, Role, RolePermission, SalaryRecord, SystemConfig, TagDictionary, WarrantyRule, User
from backend.app.security import hash_password


DEFAULT_ROLE_PERMISSIONS = [
    ("ADMIN", "all", "menu", "系统"),
    ("ADMIN", "page:users", "menu", "用户管理"),
    ("ADMIN", "page:roles", "menu", "角色管理"),
    ("ADMIN", "page:permissions", "menu", "权限管理"),
    ("ADMIN", "page:data-permissions", "menu", "数据权限"),
    ("ADMIN", "page:logs", "menu", "操作日志"),
    ("ADMIN", "page:dictionary", "menu", "标签字典"),
    ("ADMIN", "page:warranty", "menu", "质保期管理"),
    ("ADMIN", "page:statistics", "menu", "统计管理"),
    ("ADMIN", "page:ai-center", "menu", "AI能力中心"),
    ("LEADER", "page:dashboard", "menu", "首页"),
    ("LEADER", "page:candidates", "menu", "求职者数据池"),
    ("LEADER", "page:import", "menu", "简历导入"),
    ("LEADER", "page:customers", "menu", "客户公司管理"),
    ("LEADER", "page:projects", "menu", "项目管理"),
    ("LEADER", "page:positions", "menu", "岗位管理"),
    ("LEADER", "page:evaluations", "menu", "评价体系"),
    ("LEADER", "page:statistics", "menu", "统计管理"),
    ("LEADER", "page:notifications", "menu", "通知提醒"),
    ("LEADER", "page:dictionary", "menu", "标签字典"),
    ("LEADER", "page:warranty", "menu", "质保期管理"),
    ("LEADER", "page:ai-center", "menu", "AI能力中心"),
    ("OPERATOR", "page:dashboard", "menu", "首页"),
    ("OPERATOR", "page:candidates", "menu", "求职者数据池"),
    ("OPERATOR", "page:import", "menu", "简历导入"),
    ("OPERATOR", "page:projects", "menu", "项目管理"),
    ("OPERATOR", "page:positions", "menu", "岗位管理"),
    ("OPERATOR", "page:evaluations", "menu", "评价体系"),
    ("OPERATOR", "page:notifications", "menu", "通知提醒"),
    ("OPERATOR", "page:ai-center", "menu", "AI能力中心"),
]


def seed() -> None:
    db: Session = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "admin").first():
            db.add(User(username="admin", full_name="系统管理员", phone="", email="", password_hash=hash_password("admin123"), role="超级管理员", is_active=True))
        else:
            admin = db.query(User).filter(User.username == "admin").first()
            if admin.password_hash == "dev":
                admin.password_hash = hash_password("admin123")
            admin.phone = admin.phone or ""
            admin.email = admin.email or ""
        if not db.query(User).filter(User.username == "leader").first():
            db.add(User(username="leader", full_name="团队组长", phone="", email="", password_hash=hash_password("leader123"), role="组长", is_active=True))
        else:
            leader = db.query(User).filter(User.username == "leader").first()
            if leader.password_hash == "dev":
                leader.password_hash = hash_password("leader123")
            leader.phone = leader.phone or ""
            leader.email = leader.email or ""
        if not db.query(User).filter(User.username == "operator").first():
            db.add(User(username="operator", full_name="一线操作员", phone="", email="", password_hash=hash_password("operator123"), role="操作员", is_active=True))
        else:
            operator = db.query(User).filter(User.username == "operator").first()
            if operator.password_hash == "dev":
                operator.password_hash = hash_password("operator123")
            operator.phone = operator.phone or ""
            operator.email = operator.email or ""
        if not db.query(Role).count():
            db.add_all([
                Role(code="ADMIN", name="超级管理员", description="全局管理"),
                Role(code="LEADER", name="组长", description="团队管理"),
                Role(code="OPERATOR", name="操作员", description="一线执行"),
            ])
        for role_code, permission_key, permission_type, module in DEFAULT_ROLE_PERMISSIONS:
            existing = db.query(RolePermission).filter(RolePermission.role_code == role_code, RolePermission.permission_key == permission_key).first()
            if existing:
                existing.permission_type = permission_type
                existing.module = module
                existing.enabled = True
            else:
                db.add(RolePermission(role_code=role_code, permission_key=permission_key, permission_type=permission_type, module=module, enabled=True))
        if not db.query(DataPermission).count():
            db.add(DataPermission(user_id=1, scope_type="company", scope_id="1", scope_name="科技有限公司A", granted_by="system", active=True))

        if not db.query(TagDictionary).count():
            db.add_all([
                TagDictionary(category="求职者标签", name="Java", enabled=True),
                TagDictionary(category="求职者标签", name="前端", enabled=True),
                TagDictionary(category="客户需求标签", name="急招", enabled=True),
                TagDictionary(category="评价体系标签", name="优秀", enabled=True),
            ])
        warranty_defaults = {
            "简历": (3, 10, True),
            "客户": (6, 7, True),
            "项目": (6, 7, True),
            "岗位": (3, 5, True),
            "入职质保期": (2, 5, True),
        }
        existing_scopes = {item.scope for item in db.query(WarrantyRule).all()}
        for scope, (months, remind_days, auto_expire) in warranty_defaults.items():
            if scope not in existing_scopes:
                db.add(WarrantyRule(scope=scope, months=months, remind_days=remind_days, auto_expire=auto_expire))

        if not db.query(SystemConfig).count():
            db.add_all([
                SystemConfig(key="site_name", value="AI招聘管理平台", description="系统名称"),
                SystemConfig(key="watermark", value="招聘管理系统", description="水印模板"),
                SystemConfig(key="log_retention_days", value="90", description="日志保留天数"),
                SystemConfig(key="responsive_breakpoint", value="1280", description="响应式断点"),
            ])
        if not db.query(EmailConfig).count():
            db.add(EmailConfig(host="smtp.example.com", port=25, sender="noreply@example.com", username="", password="", use_tls=False, enabled=False))

        if not db.query(AuditLog).count():
            db.add(AuditLog(actor="system", module="系统", action="初始化种子数据", target_type="seed", target_id="0", result="成功", detail="seed"))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
