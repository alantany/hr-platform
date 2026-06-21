#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
progress_file="${repo_root}/progress.md"
task_plan_file="${repo_root}/task_plan.md"

timestamp="$(date '+%Y-%m-%d %H:%M:%S')"

if [ ! -f "$progress_file" ]; then
  cat > "$progress_file" <<'EOF'
# Progress

## 2026-06-14

- 
EOF
fi

python3 - "$progress_file" "$task_plan_file" "$timestamp" <<'PY'
from pathlib import Path
import sys

progress_path = Path(sys.argv[1])
task_plan_path = Path(sys.argv[2])
timestamp = sys.argv[3]

progress = progress_path.read_text(encoding="utf-8")
marker = f"## {timestamp[:10]}"
entry = f"- Task completed at {timestamp}. Update the summary with the latest finished work.\n"

if marker not in progress:
    if not progress.endswith("\n"):
        progress += "\n"
    progress += f"\n{marker}\n\n{entry}"
else:
    lines = progress.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == marker:
            insert_at = i + 2
            while insert_at < len(lines) and lines[insert_at].startswith("- "):
                insert_at += 1
            lines.insert(insert_at, entry.rstrip("\n"))
            break
    progress = "\n".join(lines) + "\n"

progress_path.write_text(progress, encoding="utf-8")

if task_plan_path.exists():
    text = task_plan_path.read_text(encoding="utf-8")
    if "## Notes" in text and "progress.md" not in text:
        task_plan_path.write_text(text.rstrip() + "\n\n- Progress is recorded in progress.md after each completed task.\n", encoding="utf-8")
PY

printf 'Updated %s\n' "$progress_file"
