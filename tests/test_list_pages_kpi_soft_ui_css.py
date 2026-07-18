from pathlib import Path

CSS = Path(__file__).resolve().parents[1] / "styles.css"

SOFT_KPI_PAGES = (
    "customers-page",
    "projects-page",
    "candidates-page",
    "notices-page",
    "job-publish-page",
    "recruit-job-list-page",
    "daily-tasks-page",
)


def _css() -> str:
    return CSS.read_text(encoding="utf-8")


def _soft_block() -> str:
    marker = "/* list-pages soft KPI — align homepage kanban */"
    css = _css()
    assert marker in css
    return css[css.index(marker) :]


def test_list_pages_kpi_share_soft_float_card_rules():
    block = _soft_block()
    for page in SOFT_KPI_PAGES:
        assert f".{page} .metrics .metric-card" in block
    assert "0 10px 24px rgba(37, 99, 235" in block
    assert "#0F172A" in block or "#0f172a" in block.lower()


def test_list_pages_kpi_hide_icons():
    block = _soft_block()
    for page in SOFT_KPI_PAGES:
        assert f".{page} .metrics .metric-icon" in block
    assert "display: none" in block
