# 首页数据看板 UI 视觉重构设计

**日期：** 2026-07-15  
**状态：** 已确认（用户选择路径 A 并批准开工）

## 目标

对 `dashboard.html` 做专业级视觉重构：**只改样式与渲染模板结构，不改数据获取、状态管理、API 与业务计算**。

## 技术路径

在现有静态栈落地（`styles.css` + `dashboard.html` 模板字符串 + 内联 SVG），不引入 Tailwind / React / lucide-react。

## 设计要点

1. Tokens：品牌蓝 `#2563EB`；背景 `#F8FAFC`；边框 `#E2E8F0`；文字 `#0F172A` / `#64748B`；圆角 12/8；轻阴影；间距 24 / 内边距 20–24。
2. KPI：去左侧彩条；标题→大数字→辅助说明；右上淡色圆底图标；hover 上浮 + 边框品牌色。
3. 日历：无数据弱化；有数据用蓝点+徽标；选中为描边+浅蓝底；非本月降透明度；chip 浅色 pill。
4. 月度卡：与 KPI 同风格；空状态居中图标+主/次文案。
5. 顶栏：保持面包屑→标题→副标题层级；通知徽标小红点精确对齐；补 hover/focus。

## 明确不动

- `loadDashboardData`、`getMonthlyMetrics`、`getCalendarEvents` 等口径与计算
- 点击筛选、跳转链接、API 调用

## 实现文件

- `styles.css`
- `src/pages/dashboard.html`（仅 markup / class）
- 必要时微调 `app.js` 顶栏铃铛徽标样式钩子（不改未读计数逻辑）
