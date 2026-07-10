from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.main import app
from tests.auth_helpers import login_headers


SAMPLE_JD = """
岗位名称：高级 Java 工程师
工作地点：上海
薪资：20-35K
学历：本科
经验：5年以上
紧急招聘 2 人
"""


@patch("backend.app.main.call_llm_for_jd_parse")
def test_parse_jd_success_as_leader(mock_llm):
    mock_llm.return_value = {
        "name": "高级 Java 工程师",
        "urgency": "紧急",
        "hiring_count": 2,
        "salary_min": 20,
        "salary_max": 35,
        "location": "上海",
        "age_requirement": "不限",
        "gender_requirement": "不限",
        "education_requirement": "本科",
        "experience_requirement": "5年以上",
        "job_status_requirement": "不限",
    }
    with TestClient(app) as client:
        headers = login_headers(client, "leader")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": SAMPLE_JD},
            headers=headers,
        )
        assert res.status_code == 200, res.text
        data = res.json()
        assert data["name"] == "高级 Java 工程师"
        assert data["urgency"] == "紧急"
        assert data["hiring_count"] == 2
        assert data["salary_min"] == 20
        assert data["salary_max"] == 35
        assert data["location"] == "上海"
        assert data["education_requirement"] == "本科"
        assert data["experience_requirement"] == "5年以上"
        assert data["description"] == SAMPLE_JD.strip()
        mock_llm.assert_called_once()


def test_parse_jd_empty_text_returns_400():
    with TestClient(app) as client:
        headers = login_headers(client, "admin")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": "   \n\t  "},
            headers=headers,
        )
        assert res.status_code == 400
        assert "请先粘贴 JD" in res.text


def test_parse_jd_operator_forbidden():
    with TestClient(app) as client:
        headers = login_headers(client, "operator")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": SAMPLE_JD},
            headers=headers,
        )
        assert res.status_code == 403


@patch("backend.app.main.call_llm_for_jd_parse")
def test_parse_jd_llm_failure_returns_502(mock_llm):
    mock_llm.side_effect = RuntimeError("timeout")
    with TestClient(app) as client:
        headers = login_headers(client, "admin")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": SAMPLE_JD},
            headers=headers,
        )
        assert res.status_code == 502
        assert "JD 解析失败" in res.text
