#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
progress_file="${repo_root}/progress.md"
task_plan_file="${repo_root}/task_plan.md"

event_name="${CODEX_HOOK_EVENT:-unknown}"
timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
today="${timestamp%% *}"

payload="$(cat 2>/dev/null || true)"

read_json_field() {
  python3 - "$1" "$payload" <<'PY'
import json, sys

key = sys.argv[1]
raw = sys.argv[2]
if not raw.strip():
    raise SystemExit(0)

try:
    data = json.loads(raw)
except Exception:
    raise SystemExit(0)

value = data
for part in key.split("."):
    if isinstance(value, dict) and part in value:
        value = value[part]
    else:
        raise SystemExit(0)

if value is None:
    raise SystemExit(0)
print(value)
PY
}

turn_type="$(read_json_field event.type || true)"
tool_name="$(read_json_field tool.name || true)"

entry="Task finalized by Codex hook (${event_name}"
if [ -n "$turn_type" ]; then
  entry="${entry}, event=${turn_type}"
fi
if [ -n "$tool_name" ]; then
  entry="${entry}, tool=${tool_name}"
fi
entry="${entry}) at ${timestamp}"

python3 - "$progress_file" "$task_plan_file" "$today" "$entry" <<'PY'
from pathlib import Path
import sys

progress_path = Path(sys.argv[1])
task_plan_path = Path(sys.argv[2])
today = sys.argv[3]
entry = sys.argv[4]

if not progress_path.exists():
    progress_path.write_text("# Progress\n\n", encoding="utf-8")

content = progress_path.read_text(encoding="utf-8")
lines = content.splitlines()
date_heading = f"## {today}"

if date_heading not in content:
    if content and not content.endswith("\n"):
        content += "\n"
    if content and not content.endswith("\n\n"):
        content += "\n"
    content += f"{date_heading}\n\n- {entry}\n"
else:
    idx = next(i for i, line in enumerate(lines) if line.strip() == date_heading)
    insert_at = idx + 1
    while insert_at < len(lines) and lines[insert_at].strip() == "":
        insert_at += 1
    while insert_at < len(lines) and lines[insert_at].startswith("- "):
        insert_at += 1
    lines.insert(insert_at, f"- {entry}")
    content = "\n".join(lines)
    if not content.endswith("\n"):
        content += "\n"

progress_path.write_text(content, encoding="utf-8")

if task_plan_path.exists():
    plan = task_plan_path.read_text(encoding="utf-8")
    marker = "## Phase 3 - Verify and close"
    if marker in plan and "codex-finalize-task.sh" not in plan:
        plan = plan.rstrip() + "\n\n- `scripts/codex-finalize-task.sh` is the hook-friendly task finalizer used to record progress at turn end.\n"
        task_plan_path.write_text(plan, encoding="utf-8")
PY

printf 'Codex task finalizer wrote %s\n' "$progress_file"
