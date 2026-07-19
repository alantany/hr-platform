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
    assert "#F5F7FA" in css or "#f5f7fa" in css.lower()
    assert "linear-gradient(180deg, #EEF5FF" not in css


def test_dashboard_cards_use_soft_radius_and_shadow():
    css = _css()
    assert "border-radius: 16px" in css
    assert "0 10px 30px -8px rgba(15, 23, 42, 0.12)" in css
    assert "rgba(15, 23, 42, 0.04)" in css


def test_dashboard_calendar_selected_is_solid_blue():
    block = _block(".dashboard-calendar-cell.is-selected {", ".dashboard-calendar-cell.has-data")
    assert "#3B82F6" in block or "#3b82f6" in block.lower()
    assert "color: #fff" in block or "color: #ffffff" in block.lower()


def test_dashboard_no_chart_empty_state_copy_still_in_page():
    html = (Path(__file__).resolve().parents[1] / "src" / "pages" / "dashboard.html").read_text(encoding="utf-8")
    assert "选择指标或日期查看明细" in html
    assert "dashboard-kanban-main" in html
