# PRD 文档索引

本目录由产品最终 DOCX 拆分而来，服务于后续多 agent 并行开发。主入口为仓库根目录 `PRD.md`。

## 使用方式

1. 所有 agent 先读 `PRD.md`，确认产品范围、权威来源、角色、全局流程和开发切片。
2. 负责具体模块的 agent 再读下表对应模块分册。模块分册已经包含任务目标、边界、依赖、数据对象、功能拆解、接口建议、测试建议和产品原始规格。
3. 所有 agent 必须同时读 `90-data-fields.md` 与 `91-permission-matrix.md`，避免字段和权限各自发明。

## 权威规则

- 权威来源：`招聘管理系统_功能详细清单_v3.0.docx`。
- 旧原型理解、历史讨论和现有页面只作背景；凡冲突以产品最终 DOCX 为准。
- 模块分册保留原 DOCX 的功能规格，并增加独立开发包结构。

## 模块分册

| 编号 | 模块 | 文档 | 功能点数 | 原始表格数 | 建议 agent 入口 |
|---|---|---|---:|---:|---|
| 01 | 首页-数据看板 | [01-dashboard.md](01-dashboard.md) | 3 | 0 | 读本分册的 `Agent 任务包` 与 `功能拆解` |
| 02 | 求职者数据池 | [02-candidate-pool.md](02-candidate-pool.md) | 15 | 15 | 读本分册的 `Agent 任务包` 与 `功能拆解` |
| 03 | 简历导入 | [03-resume-import.md](03-resume-import.md) | 3 | 3 | 读本分册的 `Agent 任务包` 与 `功能拆解` |
| 04 | 客户公司管理 | [04-customer-company.md](04-customer-company.md) | 10 | 10 | 读本分册的 `Agent 任务包` 与 `功能拆解` |
| 05 | 项目管理 | [05-project-management.md](05-project-management.md) | 6 | 6 | 读本分册的 `Agent 任务包` 与 `功能拆解` |
| 06 | 候选人跟踪与管理 | [06-candidate-tracking.md](06-candidate-tracking.md) | 3 | 3 | 读本分册的 `Agent 任务包` 与 `功能拆解` |
| 07 | 推荐与交付管理 | [07-recommendation-delivery.md](07-recommendation-delivery.md) | 5 | 5 | 读本分册的 `Agent 任务包` 与 `功能拆解` |
| 08 | 评价体系 | [08-evaluation.md](08-evaluation.md) | 4 | 2 | 读本分册的 `Agent 任务包` 与 `功能拆解` |
| 09 | 统计与分析 | [09-analytics.md](09-analytics.md) | 11 | 11 | 读本分册的 `Agent 任务包` 与 `功能拆解` |
| 10 | 通知提醒 | [10-notifications.md](10-notifications.md) | 7 | 7 | 读本分册的 `Agent 任务包` 与 `功能拆解` |
| 11 | 权限管理体系 | [11-permissions.md](11-permissions.md) | 12 | 0 | 读本分册的 `Agent 任务包` 与 `功能拆解` |
| 12 | 标签字典管理 | [12-tag-dictionary.md](12-tag-dictionary.md) | 4 | 4 | 读本分册的 `Agent 任务包` 与 `功能拆解` |
| 13 | 质保期管理 | [13-warranty.md](13-warranty.md) | 7 | 6 | 读本分册的 `Agent 任务包` 与 `功能拆解` |
| 14 | AI能力中心 | [14-ai-center.md](14-ai-center.md) | 5 | 4 | 读本分册的 `Agent 任务包` 与 `功能拆解` |
| 15 | 系统管理 | [15-system-management.md](15-system-management.md) | 3 | 3 | 读本分册的 `Agent 任务包` 与 `功能拆解` |

## 横切分册

- [90-data-fields.md](90-data-fields.md)：简历、客户公司、项目、岗位的全局字段。
- [91-permission-matrix.md](91-permission-matrix.md)：功能权限、数据权限和菜单可见性矩阵。
- [_source-map.md](_source-map.md)：产品 DOCX 到分册的映射。
