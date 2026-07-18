# 首页看板 Soft UI 改版 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将首页数据看板视觉改为截图 1 的 Soft UI（浅蓝底、白卡软阴影、更大圆角、日历实心选中），不改功能与数据逻辑，空态不加折线图。

**Architecture:** 仅在 `.dashboard-redesign` 作用域内升级 `styles.css` 看板样式；必要时 bump `dashboard.html` 缓存参数。用 CSS 文本契约测试锁定关键 token（圆角、阴影、选中色、背景）。不改 `loadDashboardData`、筛选与日历事件逻辑。

**Tech Stack:** 静态 HTML + `styles.css`；pytest 做 CSS 契约断言。

## Global Constraints

- 路径：作用域样式升级（`.dashboard-redesign`），不改全局 token 影响其他页
- 内容区背景：约 `#EEF5FF` → `#F7FAFF`
- 卡片：白底、圆角约 `18px`、软阴影；弱化灰描边
- 主色：约 `#3B82F6`
- 日历选中日：实心蓝圆角块（白字）
- 空态保留「选择指标或日期查看明细」，不加折线图
- 不改 API、指标计算、日历事件、筛选/明细逻辑
- 完成后更新 `progress.md` / `findings.md` / `task_plan.md`，再 commit 并 push

---

## File Structure

| 文件 | 职责 |
|------|------|
| `tests/test_dashboard_soft_ui_css.py` | 断言 Soft UI 关键 CSS token 存在于 `styles.css` |
| `styles.css` | `.dashboard-redesign` 及相关看板样式升级 |
| `src/pages/dashboard.html` | 仅 bump `styles.css` / `app.js` 缓存 query（如有） |
| `progress.md` / `findings.md` / `task_plan.md` | 收尾记录 |

---

### Task 1: Soft UI CSS 契约测试

**Files:**
- Create: `tests/test_dashboard_soft_ui_css.py`
- Test: `tests/test_dashboard_soft_ui_css.py`

**Interfaces:**
- Consumes: `styles.css` 文本
- Produces: RED 契约，驱动 Task 2 样式改写

- [ ] **Step 1: 写入失败测试**

```python
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
```

- [ ] **Step 2: 跑测试确认失败**

Run: `python -m pytest tests/test_dashboard_soft_ui_css.py -v`

Expected: FAIL（当前仍是 12px 圆角、描边选中、无 Soft 背景 token）

- [ ] **Step 3: Commit**

```bash
git add tests/test_dashboard_soft_ui_css.py
git commit -m "$(cat <<'EOF'
test: 增加首页看板 Soft UI CSS 契约

EOF
)"
```

---

### Task 2: 升级 styles.css 看板 Soft UI

**Files:**
- Modify: `styles.css`（约 1093–1720 看板相关规则）
- Test: `tests/test_dashboard_soft_ui_css.py`

**Interfaces:**
- Consumes: Task 1 契约（背景 token、18px、软阴影、选中实心蓝）
- Produces: Soft UI 视觉；功能 class 名不变

- [ ] **Step 1: 更新 `.dashboard-redesign` 与卡片/日历/空态样式**

在 `styles.css` 中按下列要点改写（保留现有 class 名与布局 grid）：

```css
.dashboard-redesign {
  display: grid;
  gap: 24px;
  padding: 4px 2px 8px;
  background: linear-gradient(180deg, #EEF5FF 0%, #F7FAFF 55%, #FFFFFF 100%);
  border-radius: 20px;
}

.dashboard-kanban-card,
.dashboard-month-card,
.dashboard-candidate-panel {
  border-radius: 18px;
  border: 1px solid rgba(226, 232, 240, 0.55);
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
}

.dashboard-calendar-panel,
.dashboard-month-panel {
  border-radius: 18px;
  border: 1px solid rgba(226, 232, 240, 0.55);
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
  background: #fff;
}

.dashboard-kanban-card.is-filter-active,
.dashboard-month-card.is-filter-active {
  border-color: rgba(59, 130, 246, 0.45);
  box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.18), 0 10px 28px rgba(59, 130, 246, 0.12);
  background: #f8fbff;
}

.dashboard-summary-chip {
  background: #EFF6FF;
  border: 1px solid rgba(191, 219, 254, 0.8);
  color: #64748b;
}

.dashboard-calendar-cell {
  border-radius: 12px;
  border: 1px solid rgba(226, 232, 240, 0.7);
}

.dashboard-calendar-cell.is-selected {
  border-color: #3B82F6;
  background: #3B82F6;
  color: #fff;
  box-shadow: 0 8px 18px rgba(59, 130, 246, 0.28);
}

.dashboard-calendar-cell.is-selected .dashboard-calendar-date {
  color: #fff;
}

.dashboard-calendar-cell.is-selected .dashboard-calendar-count,
.dashboard-calendar-cell.is-selected .dashboard-calendar-badge {
  color: #3B82F6;
  background: #fff;
}

.dashboard-calendar-detail {
  border-radius: 14px;
  border: 0;
  background: #F8FBFF;
}

.dashboard-detail-empty-icon {
  background: #EFF6FF;
  color: #3B82F6;
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.12);
}

.dashboard-kanban-icon,
.dashboard-month-card-icon {
  background: #EFF6FF;
  color: #3B82F6;
}
```

若 `.dashboard-kanban-card.is-filter-active` 尚不存在，在 `.dashboard-kanban-card:hover` 规则后新增上述选中样式。

确保 `.panel` 通用规则不压扁日历/月度面板：在 `.dashboard-calendar-panel.panel` / `.dashboard-month-panel.panel` 上显式设置白底与软阴影（可用与上相同的 shadow/radius）。

主色数字强调可继续用 `#3B82F6`（`.dashboard-kanban-note-num` 等）。

- [ ] **Step 2: 跑契约测试**

Run: `python -m pytest tests/test_dashboard_soft_ui_css.py -v`

Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add styles.css
git commit -m "$(cat <<'EOF'
style: 首页看板改为 Soft UI 浮卡风格

EOF
)"
```

---

### Task 3: 缓存 bump、目视验收与收尾

**Files:**
- Modify: `src/pages/dashboard.html`（stylesheet / script `?v=` 参数）
- Modify: `progress.md` / `findings.md` / `task_plan.md`
- Test: `tests/test_dashboard_soft_ui_css.py`（回归）

**Interfaces:**
- Consumes: Task 2 已落地的 Soft UI CSS
- Produces: 浏览器可拿到新 CSS；任务记录完整；已 push

- [ ] **Step 1: bump 缓存参数**

将 `dashboard.html` 中：

```html
<link rel="stylesheet" href="../../styles.css?v=20260715-dashboard-ui" />
<script defer src="../../app.js?v=20260715-dashboard-ui"></script>
```

改为：

```html
<link rel="stylesheet" href="../../styles.css?v=20260718-dashboard-soft-ui" />
<script defer src="../../app.js?v=20260718-dashboard-soft-ui"></script>
```

（若 `app.js` 未改，仍 bump 以统一版本号即可。）

- [ ] **Step 2: 目视验收**

1. 用本地 HTTP 打开 `src/pages/dashboard.html`（或经登录进仪表盘）
2. 确认：浅蓝底、白卡软阴影、约 18px 圆角
3. 确认：日历选中为实心蓝；KPI/月度卡点击筛选仍可用
4. 确认：空态仍为「选择指标或日期查看明细」，无折线图
5. 窄屏不崩版

- [ ] **Step 3: 更新三份 MD 并提交推送**

```bash
git add src/pages/dashboard.html progress.md findings.md task_plan.md
git commit -m "$(cat <<'EOF'
style: 刷新看板 Soft UI 缓存并完成收尾记录

EOF
)"
git push -u origin HEAD
```

若 push 因网络失败：本地 commit 保留，在报告中注明，稍后重试。

---

## Spec Coverage Check

| Spec 要求 | Task |
|-----------|------|
| 浅蓝底 Soft UI | Task 2 |
| 白卡软阴影 / 18px 圆角 | Task 1 + 2 |
| KPI 选中柔和蓝描边 | Task 2 |
| 日历实心蓝选中 | Task 1 + 2 |
| 空态保留、无折线图 | Task 1 + 3 |
| 不改业务逻辑 | 全局约束 |
| MD + commit + push | Task 3 |

## Placeholder Scan

无 TBD / TODO / “类似 Task N” 占位。
