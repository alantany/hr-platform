import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal
from backend.app.models import RecruitParseKeyword
from tests.auth_helpers import login_headers

client = TestClient(app)

def test_recruit_parse_keywords_crud_and_dynamic_jd_parse():
    headers = login_headers(client, "admin")
    created_ids = []
    
    try:
        # 1. 创建技能关键词
        res1 = client.post(
            "/api/recruit/parse-keywords",
            json={"category": "skills", "keyword": "Python后端开发", "is_active": True},
            headers=headers
        )
        assert res1.status_code == 200, res1.text
        kw1 = res1.json()["keyword"]
        created_ids.append(kw1["id"])
        assert kw1["keyword"] == "Python后端开发"
        assert kw1["category"] == "skills"

        # 2. 创建证书门槛关键词
        res2 = client.post(
            "/api/recruit/parse-keywords",
            json={"category": "licenses", "keyword": "高压电工证", "is_active": True},
            headers=headers
        )
        assert res2.status_code == 200, res2.text
        kw2 = res2.json()["keyword"]
        created_ids.append(kw2["id"])

        # 3. 查询关键词列表
        list_res = client.get("/api/recruit/parse-keywords", headers=headers)
        assert list_res.status_code == 200
        keywords = list_res.json()["keywords"]
        assert any(k["id"] == kw1["id"] for k in keywords)

        # 4. 用包含配置关键词的 JD 文本测试解析 API
        sample_jd = """
        职位描述：
        1. 负责 Python后端开发 与数据接口维护；
        2. 现场维护需持高压电工证上岗；
        3. 年龄 25-38岁，大专及以上学历。
        """
        parse_res = client.post(
            "/api/recruit/jobs/parse-jd",
            json={"jd_text": sample_jd, "job_title": "Python工程师"},
            headers=headers
        )
        assert parse_res.status_code == 200
        profile = parse_res.json()["profile"]

        # 校验硬性门槛与技能中包含了用户刚才配置的真实关键词
        assert profile["hard_requirements"]["education"] == "大专及以上"
        assert bool(profile["hard_requirements"]["special_licenses"])
        assert any("Python" in tag for tag in profile["priority_requirements"]["skills"]["tags"])

    finally:
        # 清理现场
        db = SessionLocal()
        try:
            if created_ids:
                db.query(RecruitParseKeyword).filter(RecruitParseKeyword.id.in_(created_ids)).delete(synchronize_session=False)
                db.commit()
        finally:
            db.close()
