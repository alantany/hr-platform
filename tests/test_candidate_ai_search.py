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
def test_candidate_ai_search_returns_top5_by_match_rank(mock_match):
    mock_match.return_value = {
        "matches": [],
        "candidate": None,
        "reason": "",
        "match_method": "ai",
        "examined_count": 0,
    }

    with TestClient(app) as client:
        headers = auth_headers(client)
        suffix = uuid4().hex[:8]
        created = []
        for idx, title in enumerate(["数据开发", "Java后端", "招聘顾问", "产品经理", "测试工程师", "运维工程师"], start=1):
            created.append(
                client.post(
                    "/api/candidates",
                    json={
                        "name": f"AI候选{idx}-{suffix}",
                        "phone": f"138{suffix[:4]}{idx:04d}"[:11],
                        "current_title": title,
                        "education": "本科",
                        "experience_years": idx,
                        "work_history": f"负责{title}",
                        "job_intention": title,
                    },
                    headers=headers,
                ).json()
            )

        # 模拟大模型按匹配度排序返回前 5 名（故意打乱创建顺序）
        ordered = [created[1], created[3], created[0], created[4], created[2]]
        mock_match.return_value = {
            "matches": [
                {"candidate": SimpleNamespace(**item), "reason": f"匹配度第{i}", "rank": i}
                for i, item in enumerate(ordered, start=1)
            ],
            "candidate": SimpleNamespace(**ordered[0]),
            "reason": "匹配度第1",
            "match_method": "ai",
            "examined_count": len(created),
        }

        response = client.post(
            "/api/candidates/ai-search",
            json={
                "job_description": "负责招聘管理平台的后端架构设计，要求熟悉招聘系统、Java后端、项目管理和中台开发。",
                "record_keys": [f"candidate:{c['id']}" for c in created],
            },
            headers=headers,
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload["match_method"] == "ai"
        assert payload["examined_count"] == len(created)
        assert len(payload["matches"]) == 5
        assert [row["rank"] for row in payload["matches"]] == [1, 2, 3, 4, 5]
        assert [row["candidate"]["id"] for row in payload["matches"]] == [c["id"] for c in ordered]
        assert payload["candidate"]["id"] == ordered[0]["id"]
        assert payload["reason"] == "匹配度第1"
        assert payload["matches"][0]["reason"] == "匹配度第1"
