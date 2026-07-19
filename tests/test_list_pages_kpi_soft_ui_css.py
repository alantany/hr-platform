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
    "logs-page",
)


def _css() -> str:
    return CSS.read_text(encoding="utf-8")


def _soft_block() -> str:
    marker = "/* list-pages KPI — align homepage solid-3d cards */"
    css = _css()
    assert marker in css
    return css[css.index(marker) :]


def test_list_pages_kpi_share_solid3d_card_rules():
    block = _soft_block()
    for page in SOFT_KPI_PAGES:
        assert f".{page} .metrics .metric-card" in block
    assert "linear-gradient(180deg, #ffffff 40%, #f3f8fd 100%)" in block
    assert "-1px 2px 0px #b0cfe1" in block
    assert "height: 93px" in block
    assert "#003fa3" in block


def test_list_pages_kpi_hide_icons_and_labels():
    block = _soft_block()
    for page in SOFT_KPI_PAGES:
        assert f".{page} .metrics .metric-icon" in block
        assert f".{page} .metrics .metric-label" in block
    assert "display: none !important;" in block
