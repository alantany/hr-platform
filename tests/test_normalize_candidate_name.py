import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app.security import normalize_candidate_name


def test_normalize_candidate_name_collapses_consecutive_duplicates():
    assert normalize_candidate_name("袁袁太太兴兴") == "袁太兴"
    assert normalize_candidate_name("  张三  ") == "张三"
    assert normalize_candidate_name("") == ""
    assert normalize_candidate_name(None) == ""
