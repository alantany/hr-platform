from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.main import app, normalize_jd_parse_result
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
        mock_llm.assert_called_once_with(SAMPLE_JD.strip())


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


def test_normalize_jd_parse_result_maps_enums_and_defaults():
    raw = {
        "name": " 产品经理 ",
        "urgency": "高",  # 别名 → 紧急
        "hiring_count": "3",
        "salary_min": "15.0",
        "salary_max": "none",
        "location": "北京",
        "age_requirement": "30到40",
        "gender_requirement": "男性",
        "education_requirement": "本科及以上",
        "experience_requirement": "五年以上",
        "job_status_requirement": "随便",
    }
    out = normalize_jd_parse_result(raw, "原文JD")
    assert out["name"] == "产品经理"
    assert out["description"] == "原文JD"
    assert out["urgency"] == "紧急"
    assert out["hiring_count"] == 3
    assert out["salary_min"] == 15
    assert out["salary_max"] is None
    assert out["location"] == "北京"
    assert out["age_requirement"] == "30-40岁"
    assert out["gender_requirement"] == "男"
    assert out["education_requirement"] == "本科"
    assert out["experience_requirement"] == "5年以上"
    assert out["job_status_requirement"] == "不限"


def test_normalize_jd_parse_result_detects_unusable():
    out = normalize_jd_parse_result(
        {
            "name": "",
            "urgency": "正常",
            "hiring_count": None,
            "salary_min": None,
            "salary_max": None,
            "location": "",
            "age_requirement": "不限",
            "gender_requirement": "不限",
            "education_requirement": "不限",
            "experience_requirement": "不限",
            "job_status_requirement": "不限",
        },
        "只有一段无法抽取的废话",
    )
    assert out.get("_unusable") is True


@patch("backend.app.main.call_llm_for_jd_parse")
def test_parse_jd_unusable_returns_422(mock_llm):
    mock_llm.return_value = {
        "name": "",
        "urgency": "正常",
        "hiring_count": None,
        "salary_min": None,
        "salary_max": None,
        "location": "",
        "age_requirement": "不限",
        "gender_requirement": "不限",
        "education_requirement": "不限",
        "experience_requirement": "不限",
        "job_status_requirement": "不限",
    }
    with TestClient(app) as client:
        headers = login_headers(client, "admin")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": "无法解析的内容"},
            headers=headers,
        )
        assert res.status_code == 422
        assert "未能从 JD 中解析出可用字段" in res.text


@patch("backend.app.main.call_llm_for_jd_parse")
def test_parse_jd_empty_name_but_other_fields_ok(mock_llm):
    mock_llm.return_value = {
        "name": "",
        "urgency": "紧急",
        "hiring_count": 2,
        "salary_min": 20,
        "salary_max": 30,
        "location": "深圳",
        "age_requirement": "不限",
        "gender_requirement": "不限",
        "education_requirement": "本科",
        "experience_requirement": "3-5年",
        "job_status_requirement": "不限",
    }
    with TestClient(app) as client:
        headers = login_headers(client, "admin")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": "深圳本科 20-30K 招2人"},
            headers=headers,
        )
        assert res.status_code == 200, res.text
        assert res.json()["name"] == ""
        assert res.json()["location"] == "深圳"


@patch("backend.app.main.call_llm_for_jd_parse")
def test_parse_jd_success_as_admin(mock_llm):
    mock_llm.return_value = {
        "name": "测试岗",
        "urgency": "正常",
        "hiring_count": 1,
        "salary_min": None,
        "salary_max": None,
        "location": "杭州",
        "age_requirement": "不限",
        "gender_requirement": "不限",
        "education_requirement": "不限",
        "experience_requirement": "不限",
        "job_status_requirement": "不限",
    }
    with TestClient(app) as client:
        headers = login_headers(client, "admin")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": "岗位：测试岗\n地点：杭州"},
            headers=headers,
        )
        assert res.status_code == 200
        assert res.json()["location"] == "杭州"


def test_parse_jd_too_long_returns_400():
    with TestClient(app) as client:
        headers = login_headers(client, "admin")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": "A" * 20001},
            headers=headers,
        )
        assert res.status_code == 400
        assert "20000" in res.text
