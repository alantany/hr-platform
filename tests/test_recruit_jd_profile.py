import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import get_db
from backend.app.models import RecruitJobPosting, RecruitJobProfile
from tests.auth_helpers import login_headers

client = TestClient(app)

def test_recruit_jd_parse_and_profile_flow():
    headers = login_headers(client, "admin")
    created_job_id = None
    try:
        # 1. 测试 JD 文本解析 API (/api/recruit/jobs/parse-jd)
        sample_jd = """
        工作职责：
        1、负责风力发电机组的现场调试和运行维护；
        2、负责分析、整理现场运行记录，进行现场风电机组的运行研究；
        岗位要求：
        1、熟练掌握办公软件的使用，具备良好文字编辑能力；
        2、必须有大专及以上学历；
        3、年龄必须在40岁以内，具有特种作业证书；
        """
        parse_res = client.post(
            "/api/recruit/jobs/parse-jd",
            json={"jd_text": sample_jd, "job_title": "风电运维工程师"},
            headers=headers
        )
        assert parse_res.status_code == 200, parse_res.text
        profile = parse_res.json()["profile"]
        
        assert profile["hard_requirements"]["education"] == "大专及以上"
        assert bool(profile["hard_requirements"]["special_licenses"])
        assert any("办公软件" in tag for tag in profile["priority_requirements"]["skills"]["tags"])
        assert profile["priority_requirements"]["skills"]["weight"] == 30.0
        assert profile["priority_requirements"]["job_category"]["weight"] == 20.0

        # 2. 测试创建带岗位画像的 Recruit Job Posting
        headers = login_headers(client, "admin")
        create_res = client.post(
            "/api/recruit/job-postings",
            json={
                "job_title": "测试风电运维岗位",
                "work_location": "长春",
                "age_min": 18,
                "age_max": 40,
                "education": "college",
                "candidate_activity": "1m",
                "daily_greet_limit": 20,
                "raw_jd_text": sample_jd,
                "job_profile": profile
            },
            headers=headers
        )
        assert create_res.status_code == 200, create_res.text
        job_data = create_res.json()["job"]
        created_job_id = job_data["id"]
        
        assert job_data["job_profile"] is not None
        assert job_data["job_profile"]["raw_jd_text"] == sample_jd.strip()
        assert job_data["job_profile"]["use_portrait_weights"] is True

        # 3. 列表查询核对
        list_res = client.get("/api/recruit/job-postings", headers=headers)
        assert list_res.status_code == 200
        jobs = list_res.json()["jobs"]
        matched_job = next((j for j in jobs if j["id"] == created_job_id), None)
        assert matched_job is not None
        assert matched_job["job_profile"] is not None

    finally:
        # 清理测试脏数据
        if created_job_id:
            db = next(get_db())
            try:
                db.query(RecruitJobProfile).filter(RecruitJobProfile.job_posting_id == created_job_id).delete()
                db.query(RecruitJobPosting).filter(RecruitJobPosting.id == created_job_id).delete()
                db.commit()
            except Exception:
                db.rollback()
            finally:
                db.close()
