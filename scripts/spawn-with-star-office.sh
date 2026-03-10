#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EVENT_SCRIPT="$ROOT_DIR/scripts/star-office-event.sh"

usage() {
  cat >&2 <<'EOF'
Usage:
  spawn-with-star-office.sh "任务描述" "label-name" [command ...]

说明:
  1) 派发前自动上报 reviewing（subagent_spawn）
  2) 若提供 command，则执行该命令，并在结束后尽力上报 idle（subagent_done）
  3) 若未提供 command，则降级为“仅上报开始 + 打印提示”，请任务完成后手动执行:
     scripts/star-office-event.sh subagent_done "<label>: done"
EOF
}

if [[ $# -lt 2 ]]; then
  usage
  exit 2
fi

task_desc="$1"
label="$2"
shift 2 || true

if [[ ! -x "$EVENT_SCRIPT" ]]; then
  echo "[fail] 缺少可执行脚本: $EVENT_SCRIPT" >&2
  exit 1
fi

"$EVENT_SCRIPT" subagent_spawn "$label: $task_desc" || true

if [[ $# -eq 0 ]]; then
  echo "[info] 未提供可等待的派发命令，已完成开始上报。" >&2
  echo "[next] 子任务完成后请执行: scripts/star-office-event.sh subagent_done \"$label: done\"" >&2
  exit 0
fi

cleanup() {
  local code=$?
  if [[ $code -eq 0 ]]; then
    "$EVENT_SCRIPT" subagent_done "$label: done" || true
  else
    "$EVENT_SCRIPT" subagent_done "$label: failed($code)" || true
  fi
}
trap cleanup EXIT

"$@"
