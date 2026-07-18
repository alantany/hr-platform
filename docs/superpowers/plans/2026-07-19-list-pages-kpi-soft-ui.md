# 列表页顶部 KPI Soft 浮卡 — 实现计划

> **For agentic workers:** 按任务顺序执行；每步保留小范围改动。

**Goal:** 客户/项目/候选人三页顶部数字看板视觉对齐首页 KPI。

**Architecture:** 在 `styles.css` 末尾增加高优先级作用域规则；三页 HTML 只 bump 缓存。

**Tech Stack:** 纯 CSS + 现有 HTML class。

---

### Task 1: CSS 契约测试

**Files:**
- Create: `tests/test_list_pages_kpi_soft_ui_css.py`

断言：
- `.customers-page .metrics .metric-card`（或共享选择器）含 `border: none` / 软阴影 / `#0F172A`
- `.metric-icon` 在三页作用域为 `display: none`

### Task 2: 写入 Soft KPI 覆盖样式

**Files:**
- Modify: `styles.css`（文件末尾追加共享规则；必要时弱化三页旧 metric 规则中冲突项）

共享选择器覆盖 customers / projects / candidates 的 `.metrics .metric-card`。

### Task 3: 缓存 bump + 文档收尾

**Files:**
- `src/pages/customers.html` / `projects.html` / `candidates.html` 缓存参数
- `progress.md` / `findings.md` / `task_plan.md`
- commit + push
