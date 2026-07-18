from pathlib import Path

CSS = Path(__file__).resolve().parents[1] / "styles.css"


def _css() -> str:
    return CSS.read_text(encoding="utf-8")


def test_list_pages_kpi_share_soft_float_card_rules():
    css = _css()
    assert ".customers-page .metrics .metric-card" in css
    assert ".projects-page .metrics .metric-card" in css
    assert ".candidates-page .metrics .metric-card" in css
    assert "0 10px 24px rgba(37, 99, 235" in css
    assert "#0F172A" in css or "#0f172a" in css.lower()


def test_list_pages_kpi_hide_icons():
    css = _css()
    assert ".customers-page .metrics .metric-icon" in css
    assert ".projects-page .metrics .metric-icon" in css
    assert ".candidates-page .metrics .metric-icon" in css
    # icon rules near list-page soft KPI should hide icons
    marker = "/* list-pages soft KPI — align homepage kanban */"
    assert marker in css
    block = css[css.index(marker) : css.index(marker) + 2500]
    assert "display: none" in block
