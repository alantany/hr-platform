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
    block = _block(".dashboard-redesign {", ".dashboard-main-row {")
    assert "#EEF5FF" in block or "#eef5ff" in block.lower()
    assert "#F7FAFF" in block or "#f7faff" in block.lower()


def test_dashboard_cards_use_soft_radius_and_shadow():
    css = _css()
    assert "border-radius: 18px" in css
    assert "0 10px 30px rgba(59, 130, 246" in css or "0 10px 28px rgba(15, 23, 42" in css


def test_dashboard_calendar_selected_is_solid_blue():
    block = _block(".dashboard-calendar-cell.is-selected {", ".dashboard-calendar-cell.has-data")
    assert "#3B82F6" in block or "#3b82f6" in block.lower()
    assert "color: #fff" in block or "color: #ffffff" in block.lower()


def test_dashboard_no_chart_empty_state_copy_still_in_page():
    html = (Path(__file__).resolve().parents[1] / "src" / "pages" / "dashboard.html").read_text(encoding="utf-8")
    assert "选择指标或日期查看明细" in html
