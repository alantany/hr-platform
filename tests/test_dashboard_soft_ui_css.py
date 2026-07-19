from pathlib import Path

CSS = Path(__file__).resolve().parents[1] / "styles.css"


def _css() -> str:
    return CSS.read_text(encoding="utf-8")


def _block(start_marker: str, end_marker: str | None = None) -> str:
    text = _css()
    start = text.index(start_marker)
    if end_marker is None:
        return text[start : start + 800]
    end = text.index(end_marker, start)
    return text[start:end]


def test_dashboard_redesign_has_soft_background_tokens():
    css = _css()
    assert "body:has(.dashboard-redesign)" in css
    assert "#ffffff" in css.lower() or "#fff" in css.lower()
    assert "linear-gradient(180deg, #EEF5FF" not in css


def test_dashboard_cards_use_solid_3d_thickness():
    css = _css()
    assert "linear-gradient(180deg, #ffffff 40%, #f3f8fd 100%)" in css
    assert "border: 1px solid #c2def8" in css
    assert "-1px 2px 0px #b0cfe1" in css
    assert "1px 2px 0px #b0cfe1" in css
    assert "0px 3px 0px #a4c7dc" in css
    assert "0px 6px 12px rgba(130, 170, 210, 0.45)" in css
    assert "#003fa3" in css


def test_dashboard_calendar_selected_is_solid_blue():
    block = _block(".dashboard-calendar-cell.is-selected {", ".dashboard-calendar-cell.has-data")
    assert "#3B82F6" in block or "#3b82f6" in block.lower()
    assert "color: #fff" in block or "color: #ffffff" in block.lower()


def test_dashboard_no_chart_empty_state_copy_still_in_page():
    html = (Path(__file__).resolve().parents[1] / "src" / "pages" / "dashboard.html").read_text(encoding="utf-8")
    assert "选择指标或日期查看明细" in html
    assert "dashboard-kanban-bottom" in html
