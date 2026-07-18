# 列表页顶部 KPI 对齐首页 Soft 浮卡

日期：2026-07-19  
状态：已批准（方案 1）  
范围：客户管理 / 项目管理 / 候选人简历池 **仅最上方数字看板**

## 目标

三页顶部 `metric-card` 视觉对齐首页 `dashboard-kanban-card`：单层白卡、软阴影、压扁条状、无图标、无彩条、大数字黑色。

## 决策

- 路径：页面作用域 CSS 覆盖（保留现有 markup、数据绑定、项目管理筛选点击）
- 不改下方筛选、表格、列表
- 不抽公共组件 class（YAGNI）

## 视觉规格

- 白底、圆角约 14px、无描边、多层软阴影
- padding 约 `12px 16px 10px`
- 隐藏 `.metric-icon` 与左侧 `::before` 彩条
- 标题/说明灰字；大数字 `#0F172A`（含 tone / is-urgent / is-zero）
- hover：轻微上浮 + 阴影加深
- 项目管理 `is-filter-active`：淡蓝描边软阴影；去掉角标 `::after` 圆点

## 改动文件

- `styles.css`：三页 `.metrics .metric-card` 作用域样式
- 三页 HTML：仅 bump 缓存参数
- 契约测试：断言关键 CSS 规则存在

## 不改

- 指标计算 / API / 筛选 JS
- 其他仍用 `metric-card` 的页面（日志、通知、岗位列表等）
