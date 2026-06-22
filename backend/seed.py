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
        if not db.query(Role).count():
            db.add_all([
                Role(code="ADMIN", name="超级管理员", description="全局管理"),
                Role(code="LEADER", name="组长", description="团队管理"),
                Role(code="OPERATOR", name="操作员", description="一线执行"),
            ])
        if not db.query(RolePermission).count():
            db.add_all([
                RolePermission(role_code="ADMIN", permission_key="all", permission_type="menu", module="系统", enabled=True),
                RolePermission(role_code="LEADER", permission_key="page:dashboard", permission_type="menu", module="首页", enabled=True),
            ])
        if not db.query(DataPermission).count():
            db.add(DataPermission(user_id=1, scope_type="company", scope_id="1", scope_name="科技有限公司A", granted_by="system", active=True))
        if not db.query(Company).count():
            company = Company(name="科技有限公司A", contact_name="王总", contact_phone="13800000000", status="招聘中", remark="种子客户")
            project = Project(name="2026核心招聘", status="招聘中", level="A", hiring_count=3, work_location="北京", description="核心岗位")
            position = Position(name="Java高级开发工程师", urgency="高", hiring_count=3, salary_min=30000, salary_max=45000, location="北京", status="紧急")
            candidate = Candidate(name="张三", phone="13811111111", email="zhangsan@example.com", current_title="Java开发工程师", city="北京", status="未锁定", source="手动创建", locked=False)
            recommendation = Recommendation(recommender="admin", status="已推荐", feedback="种子推荐")
            delivery = Delivery(delivered_by="admin", channel="系统交付", note="种子交付")
            candidate.recommendations.append(recommendation)
            recommendation.deliveries.append(delivery)
            position.recommendations.append(recommendation)
            project.positions.append(position)
            company.projects.append(project)
            db.add(company)
            db.add(candidate)
            db.flush()
        # 查询已生成的主键 ID，防范序列不为 1 导致的约束冲突
        cand = db.query(Candidate).filter(Candidate.name == "张三").first()
        if not cand:
            cand = db.query(Candidate).first()
        pos = db.query(Position).filter(Position.name == "Java高级开发工程师").first()
        if not pos:
            pos = db.query(Position).first()
        recom = db.query(Recommendation).first()

        cand_id = cand.id if cand else 1
        pos_id = pos.id if pos else 1
        recom_id = recom.id if recom else 1

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
        }
        existing_scopes = {item.scope for item in db.query(WarrantyRule).all()}
        for scope, (months, remind_days, auto_expire) in warranty_defaults.items():
            if scope not in existing_scopes:
                db.add(WarrantyRule(scope=scope, months=months, remind_days=remind_days, auto_expire=auto_expire))
        if not db.query(Evaluation).count():
            db.add(Evaluation(candidate_id=cand_id, position_id=pos_id, evaluator="admin", round_name="第1轮", grade="优秀", score=5, content="种子评价"))
        if not db.query(Notification).count():
            db.add(Notification(user="admin", title="系统已初始化", type="系统通知", read=False, target_path="/src/pages/dashboard.html"))
        if not db.query(SystemConfig).count():
            db.add_all([
                SystemConfig(key="site_name", value="招聘管理平台", description="系统名称"),
                SystemConfig(key="watermark", value="招聘管理系统", description="水印模板"),
                SystemConfig(key="log_retention_days", value="90", description="日志保留天数"),
                SystemConfig(key="responsive_breakpoint", value="1280", description="响应式断点"),
            ])
        if not db.query(EmailConfig).count():
            db.add(EmailConfig(host="smtp.example.com", port=25, sender="noreply@example.com", username="", password="", use_tls=False, enabled=False))
        if not db.query(AiTask).count():
            db.add_all([
                AiTask(task_type="resume_parse", input_text="张三 简历", output_text="RESULT<resume_parse>:张三 简历", status="完成"),
                AiTask(task_type="jd_generate", input_text="Java高级开发工程师", output_text="RESULT<jd_generate>:Java高级开发工程师", status="完成"),
            ])
        if not db.query(CandidateTrackingEvent).count():
            db.add(CandidateTrackingEvent(candidate_id=cand_id, event_type="recommend", status="已推荐", summary="种子推荐事件", operator="system", position_id=pos_id, recommendation_id=recom_id))
        if not db.query(InterviewRecord).count():
            db.add(InterviewRecord(candidate_id=cand_id, round_name="第1轮", result="通过", interviewer="system", note="种子面试"))
        if not db.query(SalaryRecord).count():
            db.add(SalaryRecord(candidate_id=cand_id, expected_salary="20k", offered_salary="22k", service_status="进行中", note="种子薪资"))
        if not db.query(EmploymentRecord).count():
            db.add(EmploymentRecord(candidate_id=cand_id, status="未入职", company_name="科技有限公司A", position_name="Java高级开发工程师", note="种子入职"))
        if not db.query(ExportRecord).count():
            db.add(ExportRecord(candidate_id=cand_id, candidate_name="张三", company_name="科技有限公司A", project_name="2026核心招聘", position_name="Java高级开发工程师", format="PDF", watermarked=True, exported_by="system", file_name="张三-Java高级开发工程师.pdf", file_path="/exports/zhangsan.pdf"))
        if not db.query(ImportRecord).count():
            db.add(ImportRecord(file_name="seed-resume.pdf", imported_by="system", imported_count=1, failed_count=0, status="成功", note="种子导入记录"))
        if not db.query(AuditLog).count():
            db.add(AuditLog(actor="system", module="系统", action="初始化种子数据", target_type="seed", target_id="0", result="成功", detail="seed"))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
