"""验证候选人列表中关联显示 recruit.job_postings 岗位名称。"""
from pathlib import Path
import sys
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app import crud


def test_list_candidates_includes_job_posting_name():
    # 模拟 RecruitJobPosting 列表
    jp1 = MagicMock()
    jp1.id = 101
    jp1.job_title = "高级Java工程师"

    jp2 = MagicMock()
    jp2.id = 102
    jp2.job_title = "资深前端专家"

    # 模拟 RecruitResumeDownload 记录
    d1 = MagicMock()
    d1.id = 1001
    d1.job_posting_id = 101
    d1.candidate_agent_id = "agent_001"
    d1.candidate_name = "张三"
    d1.job_title = "Java开发"
    d1.file_path = "resumes/zhangsan.pdf"
    d1.created_at = "2026-07-27 10:00:00"

    # 模拟 Candidate 记录
    c1 = MagicMock()
    c1.id = 1
    c1.name = "张三"
    c1.candidate_agent_id = "agent_001"
    c1.current_title = "Java开发"
    c1.city = "北京"
    c1.status = "未锁定"
    c1.delivery_status = "未推荐"
    c1.candidate_warranty_status = ""
    c1.source = "简历库"
    c1.locked = False
    c1.gender = "男"
    c1.age = 30
    c1.education = "本科"
    c1.experience_years = 5
    c1.expected_salary = "25k"
    c1.id_number = ""
    c1.tags = ""
    c1.birth_date = ""
    c1.hukou_location = ""
    c1.onboard_cycle = ""
    c1.education_detail = ""
    c1.certificates = ""
    c1.comprehensive_evaluation = ""
    c1.work_history = ""
    c1.core_value = ""
    c1.job_status = ""
    c1.family_status = ""
    c1.salary_structure = ""
    c1.job_intention = "Java工程师"
    c1.project_history = ""
    c1.created_at = None
    c1.file_path = "resumes/zhangsan.pdf"

    # Mock Session
    db = MagicMock()
    
    # 模拟 query 返回
    def mock_query(*args, **kwargs):
        q = MagicMock()
        model_str = str(args)
        if "RecruitJobPosting" in model_str:
            q.all.return_value = [jp1, jp2]
        elif "Candidate" in model_str and len(args) == 1:
            q.filter.return_value.all.return_value = []
        else:
            q.outerjoin.return_value.all.return_value = [(d1, c1)]
        return q

    db.query.side_effect = mock_query

    results = crud.list_candidates(db)
    assert len(results) == 1
    candidate_item = results[0]
    assert candidate_item["job_posting_name"] == "高级Java工程师"
