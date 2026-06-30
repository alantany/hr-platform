from pathlib import Path
import sys
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal
from backend.app.models import User, Candidate, Recommendation, Company, Project, Position

client = TestClient(app)

def test_data_permission_sharing_and_isolation():
    db = SessionLocal()
    suffix = uuid4().hex[:8]
    comp = None
    proj = None
    pos = None
    user_a = None
    user_b = None
    cand_a = None
    cand_b = None
    rec_a = None
    rec_b = None
    
    try:
        # 0. 准备关联环境
        comp = Company(name=f"测试隔离公司-{suffix}", contact_name="A", contact_phone="1")
        db.add(comp)
        db.commit()
        db.refresh(comp)

        proj = Project(company_id=comp.id, name=f"测试隔离项目-{suffix}", work_location="上海")
        db.add(proj)
        db.commit()
        db.refresh(proj)

        pos = Position(project_id=proj.id, name=f"测试隔离岗位-{suffix}", urgency="高")
        db.add(pos)
        db.commit()
        db.refresh(pos)

        # 1. 准备测试用户
        user_a = User(username=f"op_a_{suffix}", full_name="顾问A", role="操作员", password_hash="hash")
        user_b = User(username=f"op_b_{suffix}", full_name="顾问B", role="操作员", password_hash="hash")
        db.add_all([user_a, user_b])
        db.commit()
        db.refresh(user_a)
        db.refresh(user_b)

        # 2. 创建候选人
        cand_a = Candidate(name=f"共享候选人A-{suffix}", phone="13812345678", email="candidatea@example.com", owner_user_id=user_a.id)
        cand_b = Candidate(name=f"共享候选人B-{suffix}", phone="13987654321", email="candidateb@example.com", owner_user_id=user_b.id)
        db.add_all([cand_a, cand_b])
        db.commit()
        db.refresh(cand_a)
        db.refresh(cand_b)

        headers_a = {"Authorization": f"Bearer user:op_a_{suffix}"}

        # 3. 验证共享候选人池 ── 顾问 A 能看到 B 录入的候选人
        resp = client.get("/api/candidates", headers=headers_a)
        assert resp.status_code == 200
        names = [c["name"] for c in resp.json()]
        assert f"共享候选人A-{suffix}" in names
        assert f"共享候选人B-{suffix}" in names

        # 4. 验证查看明文共享 ── A 看到 B 的候选人 B，手机和邮箱为完整明文
        resp_peer = client.get(f"/api/candidates/{cand_b.id}", headers=headers_a)
        assert resp_peer.status_code == 200
        assert resp_peer.json()["phone"] == "13987654321"
        assert resp_peer.json()["email"] == "candidateb@example.com"

        # 5. 顾问 A 和 B 的推荐
        rec_a = Recommendation(candidate_id=cand_a.id, position_id=pos.id, status="待推荐", recommender=user_a.username, recommender_user_id=user_a.id)
        rec_b = Recommendation(candidate_id=cand_b.id, position_id=pos.id, status="待推荐", recommender=user_b.username, recommender_user_id=user_b.id)
        db.add_all([rec_a, rec_b])
        db.commit()
        db.refresh(rec_a)
        db.refresh(rec_b)

        # 6. 验证同级推荐数据隔离 ── A 只能拉取到 A 的推荐，不能拉取到 B 的
        resp_rec = client.get("/api/recommendations", headers=headers_a)
        assert resp_rec.status_code == 200
        rec_ids = [r["id"] for r in resp_rec.json()]
        assert rec_a.id in rec_ids
        assert rec_b.id not in rec_ids

    finally:
        # 清理数据
        if cand_a or cand_b:
            db.query(Recommendation).filter(Recommendation.candidate_id.in_([c.id for c in [cand_a, cand_b] if c])).delete()
        if cand_a:
            db.delete(cand_a)
        if cand_b:
            db.delete(cand_b)
        if user_a:
            db.delete(user_a)
        if user_b:
            db.delete(user_b)
        if pos:
            db.delete(pos)
        if proj:
            db.delete(proj)
        if comp:
            db.delete(comp)
        db.commit()
        db.close()
