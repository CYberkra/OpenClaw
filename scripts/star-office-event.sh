#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_SCRIPT="$ROOT_DIR/scripts/star-office-state.sh"

usage() {
  cat >&2 <<'EOF'
Usage:
  star-office-event.sh task_start [text]      # -> reviewing
  star-office-event.sh task_done [text]       # -> idle
  star-office-event.sh subagent_spawn [text]  # -> reviewing
  star-office-event.sh subagent_done [text]   # -> idle
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi

event="$1"
shift || true
text="${*:-}"

if [[ ! -x "$STATE_SCRIPT" ]]; then
  echo "[fail] 缺少可执行脚本: $STATE_SCRIPT" >&2
  exit 1
fi

case "$event" in
  task_start)
    "$STATE_SCRIPT" reviewing "${text:-task started}"
    ;;
  task_done)
    "$STATE_SCRIPT" idle "${text:-task done}"
    ;;
  subagent_spawn)
    "$STATE_SCRIPT" reviewing "${text:-subagent spawned}"
    ;;
  subagent_done)
    "$STATE_SCRIPT" idle "${text:-subagent done}"
    ;;
  -h|--help|help)
    usage
    exit 0
    ;;
  *)
    echo "[fail] 非法事件: $event" >&2
    usage
    exit 2
    ;;
esac
