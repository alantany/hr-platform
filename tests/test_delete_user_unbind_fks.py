from __future__ import annotations

from pathlib import Path
from uuid import uuid4
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.database import SessionLocal
from backend.app.main import app
from backend.app.models import (
    Candidate,
    Company,
    EmploymentRecord,
    InterviewRecord,
    Position,
    Project,
    Recommendation,
    SalaryRecord,
    User,
)
from backend.app.security import hash_password
from tests.auth_helpers import login_headers

client = TestClient(app)


def test_delete_user_with_recommendation_unbinds_nullable_fks():
    """有推荐等业务记录的用户删除应成功，历史记录保留且 user FK 置空。"""
    db = SessionLocal()
    suffix = uuid4().hex[:8]
    target = None
    company = None
    project = None
    position = None
    candidate = None
    recommendation = None
    interview = None
    salary = None
    employment = None

    try:
        target = User(
            username=f"del_user_{suffix}",
            full_name="待删用户",
            role="操作员",
            password_hash=hash_password("test"),
            is_active=True,
        )
        db.add(target)
        db.commit()
        db.refresh(target)

        company = Company(name=f"删用户客户-{suffix}", contact_name="A", contact_phone="1")
        db.add(company)
        db.commit()
        db.refresh(company)

        project = Project(company_id=company.id, name=f"删用户项目-{suffix}", work_location="深圳")
        db.add(project)
        db.commit()
        db.refresh(project)

        position = Position(project_id=project.id, name=f"删用户岗位-{suffix}", urgency="高")
        db.add(position)
        db.commit()
        db.refresh(position)

        candidate = Candidate(name=f"删用户候选人-{suffix}", phone=f"139{suffix[:8]}", city="深圳")
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        recommendation = Recommendation(
            candidate_id=candidate.id,
            position_id=position.id,
            recommender=target.username,
            recommender_user_id=target.id,
            status="已推荐",
        )
        interview = InterviewRecord(
            candidate_id=candidate.id,
            round_name="第1轮",
            creator_user_id=target.id,
        )
        salary = SalaryRecord(
            candidate_id=candidate.id,
            position_id=position.id,
            operator=target.username,
            operator_user_id=target.id,
        )
        employment = EmploymentRecord(
            candidate_id=candidate.id,
            status="未入职",
            operator_user_id=target.id,
        )
        db.add_all([recommendation, interview, salary, employment])
        db.commit()
        db.refresh(recommendation)
        db.refresh(interview)
        db.refresh(salary)
        db.refresh(employment)

        rec_id = recommendation.id
        interview_id = interview.id
        salary_id = salary.id
        employment_id = employment.id
        user_id = target.id

        headers = login_headers(client, "admin")
        res = client.delete(f"/api/users/{user_id}", headers=headers)
        assert res.status_code == 200, res.text
        assert res.json() == {"ok": True}

        db.expire_all()
        assert db.get(User, user_id) is None
        assert db.get(Recommendation, rec_id).recommender_user_id is None
        assert db.get(InterviewRecord, interview_id).creator_user_id is None
        assert db.get(SalaryRecord, salary_id).operator_user_id is None
        assert db.get(EmploymentRecord, employment_id).operator_user_id is None
        # 文案字段保留，便于历史追溯
        assert db.get(Recommendation, rec_id).recommender == f"del_user_{suffix}"
    finally:
        db.close()
