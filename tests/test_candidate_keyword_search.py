"""简历池关键词：岗位相关字段分层匹配 + 期望岗位优先排序。"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app import crud


def test_parse_search_keyword_groups_and_or():
    assert crud._parse_search_keyword_groups("Java,Spring 后端") == [["java", "spring"], ["后端"]]
    assert crud._parse_search_keyword_groups("A|B，C") == [["a", "b", "c"]]


def test_search_text_excludes_name_phone_city():
    item = {
        "name": "张三",
        "phone": "13800138000",
        "city": "北京",
        "job_intention": "Java后端",
        "current_title": "高级工程师",
        "work_history": "做过 Spring 项目",
        "hukou_location": "河北",
        "email": "a@b.com",
    }
    text = crud._candidate_search_text(item)
    assert "张三" not in text
    assert "13800138000" not in text
    assert "北京" not in text
    assert "河北" not in text
    assert "java后端" in text
    assert "高级工程师" in text
    assert "spring" in text


def test_l1_hit_ranks_above_l2_only():
    keyword = "Java"
    l1_hit = {
        "id": 1,
        "job_intention": "Java后端开发",
        "current_title": "产品经理",
        "work_history": "",
        "created_at": "2026-01-01 10:00:00",
    }
    l2_only = {
        "id": 2,
        "job_intention": "产品经理",
        "current_title": "Java工程师",
        "work_history": "负责 Java 服务",
        "created_at": "2026-06-01 10:00:00",
    }
    assert crud._matches_search_keyword(crud._candidate_search_text(l1_hit), keyword)
    assert crud._matches_search_keyword(crud._candidate_search_text(l2_only), keyword)
    assert crud._score_candidate_keyword_match(l1_hit, keyword)[0] == 1
    assert crud._score_candidate_keyword_match(l2_only, keyword)[0] == 0
    assert crud._score_candidate_keyword_match(l2_only, keyword)[1] >= 1
    # L1 分更高，即使创建时间更早也应排前
    assert crud._score_candidate_keyword_match(l1_hit, keyword) > crud._score_candidate_keyword_match(
        l2_only, keyword
    )


def test_name_only_match_no_longer_hits():
    item = {
        "name": "Java张",
        "job_intention": "销售",
        "current_title": "销售经理",
        "work_history": "负责大客户",
    }
    assert not crud._matches_search_keyword(crud._candidate_search_text(item), "Java")


def test_and_or_still_works_on_job_fields():
    item = {
        "job_intention": "后端开发",
        "current_title": "工程师",
        "work_history": "熟悉 Spring Boot",
        "project_history": "",
        "core_value": "",
        "certificates": "",
    }
    text = crud._candidate_search_text(item)
    assert crud._matches_search_keyword(text, "Spring,Django 后端")
    assert not crud._matches_search_keyword(text, "Spring Django")
