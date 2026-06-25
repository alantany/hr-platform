from __future__ import annotations

from pathlib import Path

from sqlalchemy.orm import Session

from backend.app.database import Base, SessionLocal, engine
from backend.app.models import AuditLog, AiTask, Candidate, CandidateTrackingEvent, Company, DataPermission, Delivery, EmailConfig, EmploymentRecord, Evaluation, ExportRecord, ImportRecord, InterviewRecord, Notification, Position, Project, Recommendation, Role, RolePermission, SalaryRecord, SystemConfig, TagDictionary, WarrantyRule, User


def seed() -> None:
    db: Session = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "admin").first():
            db.add(User(username="admin", full_name="系统管理员", password_hash="dev", role="超级管理员", is_active=True))
        if not db.query(User).filter(User.username == "leader").first():
            db.add(User(username="leader", full_name="团队组长", password_hash="dev", role="组长", is_active=True))
        if not db.query(User).filter(User.username == "operator").first():
            db.add(User(username="operator", full_name="一线操作员", password_hash="dev", role="操作员", is_active=True))
        if not db.query(Role).count():
            db.add_all([
                Role(code="ADMIN", name="超级管理员", description="全局管理"),
                Role(code="LEADER", name="组长", description="团队管理"),
                Role(code="OPERATOR", name="操作员", description="一线执行"),
            ])
        if not db.query(RolePermission).count():
            db.add_all([
                RolePermission(role_code="ADMIN", permission_key="all", permission_type="menu", module="系统", enabled=True),
                RolePermission(role_code="ADMIN", permission_key="page:users", permission_type="menu", module="用户管理", enabled=True),
                RolePermission(role_code="ADMIN", permission_key="page:roles", permission_type="menu", module="角色管理", enabled=True),
                RolePermission(role_code="ADMIN", permission_key="page:permissions", permission_type="menu", module="权限管理", enabled=True),
                RolePermission(role_code="ADMIN", permission_key="page:data-permissions", permission_type="menu", module="数据权限", enabled=True),
                RolePermission(role_code="ADMIN", permission_key="page:logs", permission_type="menu", module="操作日志", enabled=True),
                RolePermission(role_code="LEADER", permission_key="page:dashboard", permission_type="menu", module="首页", enabled=True),
                RolePermission(role_code="LEADER", permission_key="page:candidates", permission_type="menu", module="求职者数据池", enabled=True),
                RolePermission(role_code="LEADER", permission_key="page:customers", permission_type="menu", module="客户公司管理", enabled=True),
                RolePermission(role_code="LEADER", permission_key="page:projects", permission_type="menu", module="项目管理", enabled=True),
                RolePermission(role_code="LEADER", permission_key="page:statistics", permission_type="menu", module="统计管理", enabled=True),
                RolePermission(role_code="OPERATOR", permission_key="page:candidates", permission_type="menu", module="求职者数据池", enabled=True),
            ])
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
