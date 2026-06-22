# Task Plan

## Goal

以产品最终提供的 `招聘管理系统_功能详细清单_v3.0.docx` 为唯一权威需求来源，形成足够详细、可指导后续开发和多 agent 并行拆分的 PRD 文档体系。

## Authority Rule

- 最终需求以 `招聘管理系统_功能详细清单_v3.0.docx` 为准。
- 既有原型理解、历史讨论、页面原型和旧文档只能作为背景材料。
- 若旧文档/原型/记忆与 DOCX 冲突，一律以 DOCX 为准，并在 PRD 中标记为“以产品最终需求为准”。

## Current Phase

Completed search toolbar clean-up, province-city cascading dropdown implementation, and checkbox-based export logic.

## Phases

### Phase 1 - Extract and normalize final product requirements

- [x] 读取 DOCX 元信息、正文、标题层级和表格
- [x] 形成可追溯的需求摘录文件
- [x] 记录权威来源和冲突处理原则
- **Status:** complete

### Phase 2 - Decide PRD document structure

- [x] 判断采用单一 `PRD.md` 还是 `docs/prd/` 拆分文档
- [x] 设计适合多 agent 并行开发的模块边界
- [x] 明确主 PRD 与分模块 PRD 的引用关系
- **Status:** complete

### Phase 3 - Draft PRD documents

- [x] 编写主 `PRD.md`
- [x] 必要时编写分模块 PRD 文档
- [x] 覆盖业务对象、角色权限、流程、功能清单、状态、数据、验收标准和开发切片
- **Status:** complete

### Phase 4 - Review and align

- [x] 对照 DOCX 摘录检查遗漏
- [x] 对照项目规则检查文档位置和命名
- [x] 更新 `findings.md` 与 `progress.md`
- **Status:** complete

### Phase 5 - Delivery

- [x] 汇总交付文件
- [x] 说明文档结构决策
- [x] 告知验证方式和后续建议
- **Status:** complete

### Phase 6 - Phase 0 engineering foundation

- [x] Create backend project skeleton and local configuration
- [x] Implement core models, seed data, login, audit log, and base APIs
- [x] Add Alembic migration and local SQLite dev database
- [x] Wire static dashboard to local API
- [x] Verify service startup, migration, browser rendering, and CRUD smoke
- **Status:** complete

### Phase 7 - Phase 1 P0 main flow

- [x] Customer company, project, position, candidate pool, import, recommendation, delivery, permission filtering, audit logs
- [x] Connect existing HTML pages to API/mock API for Phase 1
- [x] End-to-end smoke for create customer -> project -> position -> candidate -> recommendation -> delivery -> audit logs
- **Status:** complete

### Phase 8 - Phase 2 support modules

- [x] Evaluation, analytics, notifications, tag dictionary, warranty
- [x] Connect support-module pages or local mock views
- [x] End-to-end smoke for tag, evaluation, warranty, notification, statistics
- **Status:** complete

### Phase 9 - Phase 3 enhancement modules

- [x] Dashboard enhancements, AI center mock/adapter, system management
- [x] Connect dashboard and system pages to local API/mock
- [x] End-to-end smoke for dashboard, AI, email config, responsive config
- **Status:** complete

## Key Questions

1. DOCX 中的功能是否足够大，是否需要按模块拆成多个 PRD？
2. 哪些模块可以作为后续多 agent 并行开发边界？
3. PRD 需要保留哪些字段级、状态级、权限级细节，才能指导后续实现？

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| 以 DOCX 为唯一权威需求来源 | 用户明确说明旧文档都是基于原型推测，最终文档必须以产品给的 PRD 为准 |
| 采用主 PRD + 模块分册 + 横切分册 | DOCX 覆盖 15 个模块、95 个功能点、86 张表，拆分后更适合多 agent 并行开发 |
| 将模块分册增强为独立 agent 任务包 | 用户反馈分模块内容不够独立；后续多 agent 并行需要每个分册直接包含目标、边界、依赖、功能拆解、接口建议、测试建议和完成定义 |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| `create_goal` 失败，提示已有未完成 goal | 1 | 不重复创建 goal，按用户当前 `/goal` 目标继续执行 |

### Phase 10 - Final acceptance closeout

- [x] DOCX audit matrix completed
- [x] End-to-end business workflow verified
- [x] Regression tests rerun and passing
- [x] Findings and progress updated
- **Status:** complete

### Phase 11 - 持续维护与 Bug 修复（进行中）

- [x] 候选人列表增加翻页功能，支持显示全部简历池数据
- [x] 修复 Recruit 候选人（字符串 ID）在详情弹窗中所有操作失效（`Number(id)` → NaN）
- [x] 修复薪资/入职/随访/邮件记录保存时 `candidate_id` 类型校验失败（`int | str` + `ensure_local_candidate`）
- [x] 修复 `crud.py` 中 `list_candidates` 遗漏候选人扩展字段（户口、出生日期等）导致详情页显示空白的问题
- [x] 前端增加入职、身份证、手机号等字段的实时失焦（focusout）合规校验交互
- **Status:** in progress

## Key Constraints (持续有效)

- 新增任何候选人写入接口，后端 handler 必须先调用 `ensure_local_candidate` 做 ID 解析
- 前端操作候选人 ID 时，保持字符串格式，不做 `Number()` 强转
- 每次完成代码修改，必须同步更新 `progress.md`；有新约束时更新 `findings.md`；有阶段变化时更新 `task_plan.md`
- 迁移 PostgreSQL 时，数据库操作必须严格采用标准 SQL 语法，不使用 PG 独有方言以保留可移植性

### Phase 12 - 数据库迁移至 PostgreSQL 并配置 Schema 隔离（已完成）

- [x] 启动本地 postgresql@14 服务，并创建 `hr_platform` 数据库、`recruit` schema
- [x] 编写 pg schema 和权限脚本，创建 user_recruit 和 user_delivery，授予只读/读写最小权限
- [x] 修改 `backend/app/config.py` 和 `database.py` 支持 PostgreSQL 连接，保留默认 SQLite 兼容回退
- [x] 在 `models.py` 中为 `candidate_profiles`、`resume_downloads` 等表声明所属 `recruit` 命名空间
- [x] 运行 Alembic / 数据库表自动生成，校验两套表在 PG 中的创建情况
- [x] 运行 Pytest 烟测脚本，校验标准 SQL 兼容性，确保业务功能正常
- **Status:** complete
- [x] 优化候选人列表 UI：去掉多余的基本信息、时间、来源标签，头像内置精确到状态的 SVG 锁图标。
- [x] 修改前端候选人“编辑”表单下拉框和状态判断逻辑，彻底收拢并只保留“锁定/未锁定”二元状态。
- [x] 清理后端代码中冗余的“新入库”、“激活”状态默认值，统一替换为“未锁定”。
- [x] 深度重置环境，成功清除数据库 public schema 下的所有业务测试脏数据，并确保底层表结构依然完好。

### Phase 13 - AI 简历自动化解析与入库流水线（已完成）

- [x] 创建 `resume_parse_tasks` 任务缓冲表，连接外部 `recruit.resume_downloads` 数据源与内部业务模型。
- [x] 编写 `resume_parser_worker.py`，实现基于 OpenRouter 大模型的非结构化简历批量解析。
- [x] 实现健壮的候选人 Upsert 逻辑（优先使用 `candidate_agent_id`，降级匹配手机、邮箱、姓名）。
- [x] 升级 Worker 为守护进程（Daemon），利用 `NOT IN` 差集排查法实现 24 小时无遗漏新数据同步拉取。
- [x] 修复 `crud.py` 候选人列表接口：更正外部关联表为 `resume_downloads`，并加入名字/ID 级业务防重墙，彻底解决 UI 大量冗余记录问题。
- [x] 解除“数据库资源探针”前后端的 Pagination 限制，支持大表全量透视诊断。
- **Status:** complete
