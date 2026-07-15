# UI 全局设计系统（多页面美化共用）

**日期：** 2026-07-15  
**状态：** 已确认（后续页面美化一律按此执行，不再重复粘贴）

## 技术约束

- 技术栈不变：纯 HTML + `styles.css` + 页面内 `<script>` JS
- 禁止引入框架 / 构建工具 / UI 库
- **只改样式与结构类名**；不改数据逻辑、接口调用、JS 业务函数行为
- 颜色、圆角、阴影、间距统一用 `styles.css` `:root` tokens

## Design Tokens（canonical）

| Token | 值 | 用途 |
|-------|-----|------|
| `--color-bg` | `#F8FAFC` | 页面背景 |
| `--color-surface` | `#FFFFFF` | 卡片背景 |
| `--color-border` | `#E2E8F0` | 边框 |
| `--color-text` | `#0F172A` | 主文字 |
| `--color-text-muted` | `#64748B` | 次要文字 |
| `--color-primary` | `#2563EB` | 品牌蓝（唯一主强调色） |
| `--color-primary-soft` | `#EFF4FF` | 品牌蓝浅底 |
| `--color-success` | `#16A34A` | 语义成功（仅状态） |
| `--color-warning` | `#D97706` | 语义预警（仅状态） |
| `--color-danger` | `#DC2626` | 语义危险（仅状态） |
| `--radius-card` | `12px` | 卡片圆角 |
| `--radius-control` | `8px` | 控件圆角 |
| `--radius-pill` | `999px` | 徽标/pill |
| `--shadow-card` | 极轻双层阴影 | 卡片阴影 |
| `--space` | `4px` | 间距基准（实际用 8/16/24） |

旧变量（`--background`、`--primary` 等）已别名到上述 tokens，兼容存量页面。

## 全局规则（11 条）

1. 去掉 KPI 左侧彩条 → 白底 + 1px 细边框 + 极轻阴影  
2. 主色只用品牌蓝；绿/橙/红仅状态徽标/趋势；禁止紫色  
3. KPI 数字深色加粗约 32px；标题 13px 灰；辅助 12–13px 灰  
4. 右上图标：内联 SVG 20px，装在 `--color-primary-soft` 圆底里  
5. 徽标：pill；浅底 + 同色系深字（招聘中绿 / 待确认橙 / 紧急红 / 默认灰）  
6. 卡片内边距 20–24px；模块间距 24px；用 flex/grid + `gap`  
7. 可交互元素有 hover + `:focus-visible`；主按钮实心蓝、次按钮白底描边  
8. 表格：表头浅灰、行 1px 分隔、hover 浅蓝；空状态=居中图标+说明  
9. 顶栏：面包屑(12–13灰) → H1(24–28粗) → 副标题(14灰)  
10. 通知铃铛：小红点徽标，绝对定位右上  
11. WCAG AA；KPI 窄屏自动换行/堆叠  

## 页面落地约定

每页美化时：优先改该页 class / 局部 CSS，复用全局 tokens；不动 API、状态、业务计算与点击行为。
