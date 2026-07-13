from uuid import uuid4

from datetime import datetime, timezone

from fastapi.testclient import TestClient

from backend.app.database import SessionLocal
from backend.app.main import app
from backend.app.models import Candidate, Company, Position, Project, Recommendation, User
from backend.app.security import hash_password
from tests.auth_helpers import login_headers


client = TestClient(app)


def headers(username: str) -> dict[str, str]:
    return login_headers(client, username)


def test_recommendation_calendar_uses_recommended_status_and_user_hierarchy():
    suffix = uuid4().hex[:8]
    db = SessionLocal()
    try:
        leader = User(
            username=f"temp_calendar_leader_{suffix}",
            full_name="日历组长",
            password_hash=hash_password("test"),
            role="组长",
            is_active=True,
        )
        outsider = User(
            username=f"temp_calendar_outsider_{suffix}",
            full_name="外组操作员",
            password_hash=hash_password("test"),
            role="操作员",
            is_active=True,
        )
        db.add_all([leader, outsider])
        db.flush()
        operator = User(
            username=f"temp_calendar_operator_{suffix}",
            full_name="直属操作员",
            password_hash=hash_password("test"),
            role="操作员",
            is_active=True,
            manager_user_id=leader.id,
        )
        db.add(operator)
        db.flush()
        company = Company(name=f"推荐日历客户-{suffix}", owner_user_id=leader.id)
        db.add(company)
        db.flush()
        project = Project(company_id=company.id, name=f"推荐日历项目-{suffix}", owner_user_id=leader.id)
        db.add(project)
        db.flush()
        position = Position(project_id=project.id, name=f"推荐日历岗位-{suffix}", owner_user_id=leader.id)
        db.add(position)
        db.flush()
        candidates = [
            Candidate(name=f"组长推荐-{suffix}", owner_user_id=leader.id),
            Candidate(name=f"组员推荐-{suffix}", owner_user_id=operator.id),
            Candidate(name=f"组员待推荐-{suffix}", owner_user_id=operator.id),
            Candidate(name=f"外组推荐-{suffix}", owner_user_id=outsider.id),
        ]
        db.add_all(candidates)
        db.flush()
        db.add_all([
            Recommendation(candidate_id=candidates[0].id, position_id=position.id, recommender=leader.username, recommender_user_id=leader.id, status="已推荐", recommended_at=datetime.now(timezone.utc)),
            Recommendation(candidate_id=candidates[1].id, position_id=position.id, recommender=operator.username, recommender_user_id=operator.id, status="已推荐", recommended_at=datetime.now(timezone.utc)),
            Recommendation(candidate_id=candidates[2].id, position_id=position.id, recommender=operator.username, recommender_user_id=operator.id, status="待推荐"),
            Recommendation(candidate_id=candidates[3].id, position_id=position.id, recommender=outsider.username, recommender_user_id=outsider.id, status="已推荐", recommended_at=datetime.now(timezone.utc)),
        ])
        db.commit()
        leader_username = leader.username
        operator_username = operator.username
        outsider_username = outsider.username
    finally:
        db.close()

    leader_rows = client.get("/api/dashboard/recommendation-calendar", headers=headers(leader_username)).json()
    operator_rows = client.get("/api/dashboard/recommendation-calendar", headers=headers(operator_username)).json()
    outsider_rows = client.get("/api/dashboard/recommendation-calendar", headers=headers(outsider_username)).json()

    assert {row["operator"] for row in leader_rows} == {"日历组长", "直属操作员"}
    assert {row["group_leader"] for row in leader_rows} == {"日历组长"}
    assert [row["operator"] for row in operator_rows] == ["直属操作员"]
    assert [row["group_leader"] for row in operator_rows] == ["日历组长"]
    assert [row["operator"] for row in outsider_rows] == ["外组操作员"]
    assert [row["group_leader"] for row in outsider_rows] == ["未分组"]


def test_recommendation_calendar_admin_recommender_is_ungrouped() -> None:
    """超级管理员推荐不单独成组，统计单位仅为组长。"""
    suffix = uuid4().hex[:8]
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        assert admin is not None
        admin_label = admin.full_name or admin.username
        company = Company(name=f"超管推荐客户-{suffix}", owner_user_id=admin.id)
        db.add(company)
        db.flush()
        project = Project(company_id=company.id, name=f"超管推荐项目-{suffix}", owner_user_id=admin.id)
        db.add(project)
        db.flush()
        position = Position(project_id=project.id, name=f"超管推荐岗位-{suffix}", owner_user_id=admin.id)
        db.add(position)
        db.flush()
        candidate = Candidate(name=f"超管推荐候选人-{suffix}", owner_user_id=admin.id)
        db.add(candidate)
        db.flush()
        db.add(
            Recommendation(
                candidate_id=candidate.id,
                position_id=position.id,
                recommender=admin.username,
                recommender_user_id=admin.id,
                status="已推荐",
                recommended_at=datetime.now(timezone.utc),
            )
        )
        db.commit()
    finally:
        db.close()

    rows = client.get("/api/dashboard/recommendation-calendar", headers=headers("admin")).json()
    matched = [row for row in rows if row.get("operator") == admin_label]
    assert matched, f"expected admin recommendation in calendar, operators={[r.get('operator') for r in rows]}"
    assert all(row.get("group_leader") == "未分组" for row in matched)


def test_recommendation_calendar_includes_rows_without_recommender_user() -> None:
    """无 recommender_user_id 的已推荐记录也应进入日历（与月度 recommended_at 口径一致）。"""
    suffix = uuid4().hex[:8]
    db = SessionLocal()
    try:
        company = Company(name=f"无推荐人客户-{suffix}")
        db.add(company)
        db.flush()
        project = Project(company_id=company.id, name=f"无推荐人项目-{suffix}")
        db.add(project)
        db.flush()
        position = Position(project_id=project.id, name=f"无推荐人岗位-{suffix}")
        db.add(position)
        db.flush()
        candidate = Candidate(name=f"无推荐人候选人-{suffix}")
        db.add(candidate)
        db.flush()
        db.add(
            Recommendation(
                candidate_id=candidate.id,
                position_id=position.id,
                recommender="legacy-operator",
                recommender_user_id=None,
                status="已推荐",
                recommended_at=datetime.now(timezone.utc),
            )
        )
        db.commit()
    finally:
        db.close()

    admin = login_headers(client, "admin")
    rows = client.get("/api/dashboard/recommendation-calendar", headers=admin).json()
    matched = [row for row in rows if row.get("operator") == "legacy-operator"]
    assert matched
    assert all(row.get("group_leader") == "未分组" for row in matched)
