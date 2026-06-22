# AI 简历解析流水线 - 数据关联机制

在整个猎头招聘交付系统中，由于简历数据的产生、解析和落库跨越了外部系统和内部系统的多个阶段，因此需要建立一套严密的外键 ID 绑定机制。

核心流转过程依赖以下三张表的关键 ID 进行关联：

1. `recruit.resume_downloads` (外部数据接收表)
2. `resume_parse_tasks` (中间任务调度缓冲表)
3. `candidates` (内部核心候选人业务表)

---

## 核心 ID 角色说明

### 1. `candidate_agent_id`：贯穿始终的“全局护照”
- **来源**：最早由外部爬虫（如 Boss 直聘、猎聘的数据采集系统）在获取候选人数据时生成。
- **存储位置**：在抓取落盘时保存在 `recruit.resume_downloads` 表中；在 AI 解析成功落库时同步存储在 `candidates` 表中。
- **作用**：它是候选人在整个大系统架构下的绝对唯一标识符，也是后续执行 Upsert（更新或插入）操作时**最优先匹配**的关键凭证，彻底避免了同名、同手机号带来的数据污染问题。

### 2. `resume_download_id`：中间任务表的“起始锚点”
- **来源**：它是 `recruit.resume_downloads` 表在 PostgreSQL 数据库中自增生成的主键 `id`。
- **存储位置**：写入并保存在 `resume_parse_tasks` 表中。
- **作用**：当后台 `resume_parser_worker.py` 被唤醒时，会拿着这个 ID 去溯源并找到该任务对应的物理文件路径（如 PDF 简历路径）和全局 `candidate_agent_id`，为 AI 大模型读取文本提供入口坐标。

### 3. `candidate_id`：中间任务表的“终点锚点”
- **来源**：当大模型完成 JSON 数据提取后，由 SQLAlchemy 框架执行 `db.flush()` 瞬间触发数据库生成的主键自增 `id`。
- **存储位置**：保存在 `candidates`（候选人业务表）中作为主键，同时反向记录在 `resume_parse_tasks` 表中。
- **作用**：标记当前外部文件解析生命周期的终结，同时宣告该业务实体正式进入业务流转环节（比如安排面试、交付推荐等）。任务表通过记录它，可以实现从“业务库的人”一键追溯回“他最早的那份 PDF 原件”的完整闭环。

---

## 数据流转时序图

1. **[数据采集]** 外部系统将简历插入 `recruit.resume_downloads`，生成记录主键，并附带外部 `candidate_agent_id`。
2. **[排队入列]** 调度脚本将 `resume_downloads.id` 作为 `resume_download_id` 推入 `resume_parse_tasks` 任务队列表，状态设为 `PENDING`。
3. **[AI 解析]** Worker 开始处理任务，通过 `resume_download_id` 找到文件并读取文本喂给大模型提取 JSON 结构数据。
4. **[落库匹配]**
   - 优先通过提取出的 `candidate_agent_id` 查询 `candidates` 表是否存在匹配人选。
   - 若无，则降级使用解析出的 `phone` -> `email` -> `name` 尝试寻找。
5. **[Upsert 结转]**
   - 若匹配到记录，则进行更新（Update），补全或刷新该候选人的字段。
   - 若未匹配，则插入（Insert）一条新的候选人记录，并获得返回的 `candidate_id`。
6. **[状态闭环]** Worker 将获得的 `candidate_id` 写回 `resume_parse_tasks` 任务表，并将任务状态更新为 `SUCCESS`。
