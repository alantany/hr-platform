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
- [x] Add Alembic migration and PostgreSQL dev database
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
- [x] 候选人详情页增加推荐项目情况面板和一键级联“推荐至岗位”交互及接口打通
- [x] 修复 pytest 回归测试（手机掩码断言、批量导入坏文件 400 失败），解除测试对外部 LLM 接口依赖
- [x] 候选人详情页增加备注信息展示面板与添加备注弹窗，支持多次备注并连通后端 `candidate_notes` 表
- [x] 优化“数据库资源探针”，移除硬编码的 table_name 白名单限制，改为从数据库动态反射发现，并提供原生 SQL fallback 查询以支持未映射物理表的数据预览
- [x] 候选人详情页增加“候选人跟踪表”与“添加面试记录”交互弹窗，支持面试记录添加和初筛微标圆圈展现
- [x] 优化面试记录操作栏为并列 SVG 圆圈图标按钮（发送邮件/编辑/删除），并支持面试记录修改和二次确认物理删除
- [x] 为所有回归测试增加全局数据库清理 fixture，测试结束后自动回收新增数据并回写 `admin` / 质保 / 系统配置 / 邮箱配置默认值
- **Status:** in progress

## Key Constraints (持续有效)

- 新增任何候选人写入接口，后端 handler 必须先调用 `ensure_local_candidate` 做 ID 解析
- 前端操作候选人 ID 时，保持字符串格式，不做 `Number()` 强转
- 每次完成代码修改，必须同步更新 `progress.md`；有新约束时更新 `findings.md`；有阶段变化时更新 `task_plan.md`
- 迁移 PostgreSQL 时，数据库操作必须严格采用标准 SQL 语法，不使用 PG 独有方言以保留可移植性
- 数据库物理表数据探针不应使用硬编码的白名单过滤表名，需保持全量且免过滤呈现
- 候选人面试跟踪记录写入时，须执行 `ensure_local_candidate` 外部 ID 入库转换，并为“初筛”选项结果进行强制校验约束

### Phase 12 - 数据库迁移至 PostgreSQL 并配置 Schema 隔离（已完成）

- [x] 启动本地 postgresql@14 服务，并创建 `hr_platform` 数据库、`recruit` schema
- [x] 编写 pg schema 和权限脚本，创建 user_recruit 和 user_delivery，授予只读/读写最小权限
- [x] 修改 `backend/app/config.py` 和 `database.py` 统一使用 PostgreSQL 连接
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
- [x] 升级数据库资源探针：解除了 Pagination 限制，支持大表全量透视诊断。
- **Status:** complete

### Phase 14 - 薪资福利入职跟踪表与相关优化（已完成）

- [x] 在 `models.py` 的 `SalaryRecord` 类中补齐新增 8 个字段
- [x] 修改 `main.py` 的 `ensure_schema()` 支持新增字段的 DDL 自愈式自动迁移
- [x] 修改后端 API，支持多条薪资记录新增，支持操作员动态匹配与 PATCH 面试轮次只读校验，新增 DELETE 物理删除
- [x] 重构前端 `candidates.html` 增加“💰 薪资/福利/入职条件跟踪表”独立面板，及高保真黄色说明说明弹窗
- [x] 重构 `app.js` 中的逻辑，添加弹窗动态填充轮次、只读控制、接受/不接受选择及 confirm 防呆删除
- [x] 优化“客户公司”输入框，采用 `<datalist>` 支持从 `companies` 表自动联想和按名字输入过滤搜索
- [x] 编写 `tests/test_salary_tracking.py` 自动化测试全量覆盖并通过
- **Status:** complete

### Phase 15 - 候选人入职状态双模联动与质保校验（已完成）

- [x] 配置 `WarrantyRule` 质保种子数据，新增默认“入职质保期”为 2 个月（60 天）。
- [x] 后端在保存入职记录时，联动更新最新一条 `CandidateTrackingEvent` 的 `employment_status`（已入职/未入职），并联动更新候选人自身的 status 状态（“已录用”/“未锁定”）。
- [x] 将独立的入职 Modal 弹窗删除，重构为直接常驻嵌入详情弹窗 `data-candidate-detail-modal` 底部的面板。
- [x] 引入 Toggle 开关进行“已入职”与“未入职”模式的即时状态切换。
- [x] 滑到“已入职”直接触发后台保存生效，显示绿底继承信息，无确认入职按钮；滑到“未入职”先显示编辑框，点击“确认未入职”保存后按钮隐退，直接显示已确认备注文本。
- [x] 根据“入职时间”与当前日期差异，结合后端的“入职质保期”规则天数，动态计算并展示质保状态（“质保在职” / “超过质保期”），并已优化支持未来入职日期的防溢出判断。
- [x] 每次状态保存和初始化时，自动通过 `window.fetchCandidatePanels` 对候选人生命周期进行局部动态重载，未入职显示灰色“入职”及原因，已入职显示绿色“入职”及岗位公司。
- [x] 编写 `tests/test_employment_onboarding.py` 自动化测试并通过 pytest 回归验证。
- **Status:** complete

### Phase 16 - 候选人高保真 PDF 简历导出功能（已完成）

- [x] 新建 `pdf_generator.py` 后端生成模块，利用 ReportLab + `'STHeiti'` 渲染高保真简历排版
- [x] 实现顶栏合同/项目元数据，双列灰底信息网格与左侧蓝色装饰条小标题
- [x] 使用 NumberedCanvas 处理多页流式排版并显示“第 X 页 / 共 Y 页”专业页脚
- [x] 修改 `POST /api/export-records` 将物理 PDF 存储至 `exports/` 目录，回填相对路径并支持覆盖兼容
- [x] 修改前端 `app.js` 的导出保存动作，API 返回成功后如果是 PDF 格式，自动触发浏览器下载
- [x] 编写 `tests/test_pdf_export.py` 自动化测试并通过 pytest 全量回归验证
- **Status:** complete

### Customer Management - 删除链路与页面收口（已完成）

- [x] 确认客户页数据来源为数据库 API，而不是前端硬编码或测试假数据。
- [x] 将客户列表主区域改为 `data-company-list`，去掉 `console.log` 和只渲染前三条的死代码。
- [x] 修正客户状态文案为 `失效 / 恢复`，不再混入项目页的 `招聘完毕 / 完结` 状态。
- [x] 在后端补齐公司/项目删除的依赖清理顺序，覆盖推荐、反馈、交付、跟踪和评价等下游表。
- [x] 新增回归测试 `tests/test_company_delete_cascade.py` 并通过。
- **Status:** complete

### Test Cleanup - 公共收尾脚本（已完成）

- [x] 抽出 `backend/test_cleanup.py` 复用 pytest 收尾逻辑。
- [x] 新增 `scripts/cleanup_test_data.py`，支持一键全量清理与 `--dry-run` 预览。
- [x] 补上 `resume_parse_tasks` 的清理，避免测试结束后残留解析任务。
- [x] 避免触碰当前账号无权限的 `recruit.*` 外部表，保证脚本可稳定执行。
- **Status:** complete

### Phase 17 - 权限系统 RBAC 与数据权限收口（已完成）

- [x] 将用户、角色、功能权限、数据权限、操作日志接口收口为超级管理员后端强校验。
- [x] 将数据权限范围收口为 PRD 要求的 `company / project / position`，后端拒绝旧的 `team / personal` 范围。
- [x] 为客户、项目、岗位、候选人列表和详情补上角色数据范围过滤。
- [x] 新增候选人归属字段与候选人转派审批记录表，锁定候选人时记录归属，释放时清空归属。
- [x] 新增 `tests/test_permissions_rbac.py` 覆盖非管理员 403、岗位授权候选人可见性、候选人转派审批。
- [x] 更新权限相关页面和公共测试清理脚本，确保新表测试结束后不残留脏数据。
- **Status:** complete

### Phase 18 - 权限系统登录认证与横切权限闭环（已完成）

- [x] 新增真实登录页和前端登录/退出/token 持久化流程，未登录访问受保护页面会跳转登录页。
- [x] 后端登录改为按用户密码校验并签发用户身份 token，不再把所有登录都当作管理员。
- [x] `/api/me` 返回角色启用的功能权限，前端菜单优先按 `role_permissions` 渲染。
- [x] 用户创建、编辑、重置密码改为写入哈希密码，测试收尾和 seed 会恢复 admin/leader/operator 默认登录密码。
- [x] 推荐、反馈、交付、导出、统计、通知和 AI 任务接口补齐同一套数据权限过滤。
- [x] AI 任务新增 `created_by` 字段和启动自愈迁移，普通用户只能看到自己创建的 AI 任务。
- [x] 新增权限回归测试覆盖未登录 401、leader/operator 登录身份、退出审计、横切数据权限过滤。
- [x] 验证通过：Python 编译检查、前端 JS 检查、权限/Phase1/Phase2/Phase3 回归测试、权限页面 smoke 静态检查。
- **Status:** complete

### Phase 19 - 团队归属权限模型（已完成）

- [x] 新增 `users.manager_user_id`，支持配置“组长 -> 组员”的直属关系。
- [x] 客户、项目、岗位新增 `owner_user_id`，创建时默认归属当前操作用户。
- [x] 数据权限判断升级为：操作员看自己归属数据；组长看自己和直属组员归属数据；其他组长互相隔离；超级管理员看全部。
- [x] 用户管理页新增“直属组长ID”创建/编辑字段，便于配置李四、王五归属张三这类团队关系。
- [x] 新增回归测试覆盖张三/孙二/李四/王五场景：李四王五互相不可见，张三可见下属项目，孙二不可见张三组项目。
- **Status:** complete

### Phase 20 - 异步按钮即时反馈（已完成）

- [x] 盘点按钮异步入口，确认高频操作主要集中在 `app.js` 的全局 `button[data-action]` 委托。
- [x] 新增共享按钮忙碌态，异步开始前立即显示 loading、禁用和 `aria-busy`，完成后恢复。
- [x] 简历导出补上弹窗加载空态和批量导出 `N/M` 进度反馈。
- [x] 用 Playwright 延迟接口验证导出、AI 检索和日志刷新三个代表性异步按钮的即时反馈。
- [x] 跑通 `node --check app.js`、`git diff --check -- app.js styles.css` 和 `tests/test_pdf_export.py`。
- **Status:** complete
