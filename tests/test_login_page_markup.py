from pathlib import Path

LOGIN_HTML = Path(__file__).resolve().parents[1] / "src" / "pages" / "login.html"


def _html() -> str:
    return LOGIN_HTML.read_text(encoding="utf-8")


def test_login_page_has_hexagon_xl_logo():
    html = _html()
    assert 'class="login-logo"' in html
    assert "<svg" in html
    assert ">XL<" in html or ">XL</" in html


def test_login_page_brand_copy_and_pills():
    html = _html()
    assert "AI招聘管理平台" in html
    assert "人力资源管理系统 v3.0" in html
    assert "AI简历筛选" in html
    assert "JD自动匹配" in html
    assert "候选状态跟踪" in html
    assert "招聘交付闭环" in html


def test_login_page_keeps_auth_hooks():
    html = _html()
    assert 'data-login-form' in html
    assert 'data-login-username' in html
    assert 'data-login-password' in html
    assert 'data-login-submit' in html
    assert 'data-login-message' in html
    assert 'value="admin"' in html
    assert 'value="admin123"' in html
    assert "reason=kicked" in html or "reason === 'kicked'" in html


def test_login_page_drops_old_blue_panel_mark():
    html = _html()
    assert 'class="login-mark"' not in html
    assert "login-footnote" not in html
