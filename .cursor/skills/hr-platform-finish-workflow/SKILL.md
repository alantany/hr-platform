---
name: hr-platform-finish-workflow
description: >-
  Finish hr-plateform tasks by updating task_plan.md, findings.md, progress.md,
  then git commit and push. Use after any code or doc change in this repo unless
  the user explicitly says not to commit or push.
---

# hr-plateform 任务收尾流程

完成任意实际开发或文档修改后，**默认必须**执行本流程（用户明确说不要提交/推送时除外）。

## 1. 更新三份 MD（项目根目录）

| 文件 | 写什么 |
|------|--------|
| `findings.md` | 新确认的业务规则、技术结论、约束（顶部追加 dated 小节） |
| `progress.md` | 本次做了什么、验证结果（顶部追加 dated 小节） |
| `task_plan.md` | 更新 `Current Phase`；大任务补/完成 Phase 条目 |

小改动也要至少更新 `progress.md`；有结构性判断时同步 `findings.md`。

## 2. Git 提交

```bash
git status
git diff --stat
```

- 只 stage 与本次任务相关的文件
- **不要**提交 `exports/`、Office 临时文件（`~$*.docx`）、`.env`、密钥
- 提交信息：1–2 句，说明 why

```bash
git add <相关文件>
git commit -m "$(cat <<'EOF'
<type>: 简短说明

EOF
)"
```

## 3. 推送到 GitHub

```bash
git push -u origin HEAD
git status
```

## 4. 回复用户时说明

- commit hash 与 message
- 是否已 push
- 三份 MD 更新了哪些要点

## 例外

- 用户明确说「不要提交」「不要推送」→ 只更新 MD 或仅改代码，不 commit
- 纯问答、无文件改动 → 跳过本流程
