#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_SCRIPT="$ROOT_DIR/scripts/star-office-state.sh"
INTERVAL=30
ONCE=0

if [[ "${1:-}" == "--once" ]]; then
  ONCE=1
fi

if ! command -v openclaw >/dev/null 2>&1; then
  echo "[warn] openclaw CLI 不可用；无法自动统计 subagents。可手动调用: $STATE_SCRIPT reviewing \"manual mode\"" >&2
  exit 2
fi

if [[ ! -x "$STATE_SCRIPT" ]]; then
  echo "[fail] 状态脚本不存在或不可执行: $STATE_SCRIPT" >&2
  exit 1
fi

get_active_count() {
  local out

  # 兼容当前 OpenClaw CLI：读取最近活跃会话，按 key 包含 :subagent: 计数
  if ! out="$(openclaw sessions --json --active 10 2>/dev/null)"; then
    echo "ERR"
    return
  fi

  python3 - <<'PY' "$out"
import json, sys
raw = sys.argv[1].strip()
if not raw:
    print(0)
    raise SystemExit

try:
    data = json.loads(raw)
except Exception:
    print("ERR")
    raise SystemExit

sessions = []
if isinstance(data, dict):
    v = data.get("sessions")
    if isinstance(v, list):
        sessions = v
elif isinstance(data, list):
    sessions = data

cnt = 0
for s in sessions:
    if not isinstance(s, dict):
        continue
    key = str(s.get("key", ""))
    if ":subagent:" in key:
        cnt += 1

print(cnt)
PY
}

run_once() {
  local count
  count="$(get_active_count)"
  if [[ "$count" == "ERR" ]]; then
    echo "[warn] 无法读取 subagents 列表，跳过本轮" >&2
    return 1
  fi

  if [[ "$count" =~ ^[0-9]+$ ]] && (( count > 0 )); then
    "$STATE_SCRIPT" reviewing "subagents active: $count"
  else
    "$STATE_SCRIPT" idle "no active subagents"
  fi
}

while true; do
  run_once || true
  [[ $ONCE -eq 1 ]] && break
  sleep "$INTERVAL"
done
