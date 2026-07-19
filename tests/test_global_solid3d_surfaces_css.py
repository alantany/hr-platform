from pathlib import Path

CSS = Path(__file__).resolve().parents[1] / "styles.css"


def test_global_solid3d_excludes_statistics_and_login():
    css = CSS.read_text(encoding="utf-8")
    assert "Global solid-3d surfaces" in css
    assert 'body:not(:has([data-page-owned-style="statistics.html"]))' in css
    assert "login-stage" in css
    assert "linear-gradient(180deg, #ffffff 40%, #f3f8fd 100%)" in css
    assert "-1px 2px 0px #b0cfe1" in css


def test_dashboard_candidate_panel_uses_solid3d():
    css = CSS.read_text(encoding="utf-8")
    idx = css.index(".dashboard-candidate-panel {")
    block = css[idx : idx + 500]
    assert "#c2def8" in block
    assert "linear-gradient(180deg, #ffffff 40%, #f3f8fd 100%)" in block
