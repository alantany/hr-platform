from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.main import app


def auth_headers(client: TestClient):
    token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@patch("backend.app.main.ai_match_candidate")
def test_candidate_ai_search_returns_best_match(mock_match):
    mock_match.return_value = {
        "candidate": None,
        "reason": "",
        "match_method": "ai",
        "examined_count": 0,
    }

    with TestClient(app) as client:
        headers = auth_headers(client)
        suffix = uuid4().hex[:8]
        c1 = client.post(
            "/api/candidates",
            json={
                "name": f"AI候选A-{suffix}",
                "phone": f"1380000{suffix[:4]}",
                "current_title": "数据开发工程师",
                "education": "本科",
                "experience_years": 5,
                "work_history": "负责数据平台开发",
                "project_history": "数据治理项目",
                "core_value": "稳定交付",
                "job_intention": "Java后端",
            },
            headers=headers,
        ).json()
        c2 = client.post(
            "/api/candidates",
            json={
                "name": f"AI候选B-{suffix}",
                "phone": f"1390000{suffix[:4]}",
                "current_title": "Java后端工程师",
                "education": "本科",
                "experience_years": 8,
                "work_history": "负责招聘系统与中台架构",
                "project_history": "猎头招聘管理平台",
                "core_value": "懂招聘业务",
                "job_intention": "招聘系统",
            },
            headers=headers,
        ).json()

        mock_match.return_value = {
            "candidate": SimpleNamespace(**c2),
            "reason": "岗位经历与项目背景高度匹配",
            "match_method": "ai",
            "examined_count": 2,
        }

        response = client.post(
            "/api/candidates/ai-search",
            json={
                "job_description": "负责招聘管理平台的后端架构设计，要求熟悉招聘系统、Java后端、项目管理和中台开发。",
                "record_keys": [f"candidate:{c1['id']}", f"candidate:{c2['id']}"],
            },
            headers=headers,
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload["candidate"]["id"] == c2["id"]
        assert payload["candidate"]["name"] == c2["name"]
        assert payload["reason"] == "岗位经历与项目背景高度匹配"
        assert payload["match_method"] == "ai"
        assert payload["examined_count"] == 2
