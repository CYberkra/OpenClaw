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
  local cmd_ok=0

  if out="$(openclaw sessions list --kinds spawn --limit 50 2>/dev/null)"; then
    cmd_ok=1
  elif out="$(openclaw subagents list 2>/dev/null)"; then
    cmd_ok=1
  fi

  if [[ $cmd_ok -ne 1 ]]; then
    echo "ERR"
    return
  fi

  python3 - <<'PY' "$out"
import json, re, sys
raw = sys.argv[1].strip()
if not raw:
    print(0)
    raise SystemExit

# 优先按 JSON 解析
try:
    data = json.loads(raw)
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for k in ("items", "sessions", "data", "results"):
            v = data.get(k)
            if isinstance(v, list):
                items = v
                break
    cnt = 0
    for it in items:
        if not isinstance(it, dict):
            continue
        kind = str(it.get("kind", "")).lower()
        status = str(it.get("status", "")).lower()
        is_spawn = (kind == "spawn") or ("spawn" in kind)
        active = status in {"running", "active", "in_progress", "working", "pending"} or status == ""
        if is_spawn and active:
            cnt += 1
    print(cnt)
    raise SystemExit
except Exception:
    pass

# 表格/文本输出兜底：去掉头部，统计看起来“活跃”的 spawn 行
lines = [ln for ln in raw.splitlines() if ln.strip()]
filtered = []
for ln in lines:
    l = ln.strip().lower()
    if any(h in l for h in ("session", "id", "status", "kind")) and ("spawn" in l or "kinds" in l):
        continue
    if l.startswith("-") or l.startswith("="):
        continue
    filtered.append(ln)

active_re = re.compile(r"\b(running|active|in[_ -]?progress|working|pending)\b", re.I)
spawn_re = re.compile(r"\bspawn\b", re.I)
count = 0
for ln in filtered:
    if spawn_re.search(ln) and active_re.search(ln):
        count += 1

# 若没有显式状态列，且都是 spawn 列表，则按非空行计数
if count == 0 and filtered and all(spawn_re.search(ln) for ln in filtered):
    count = len(filtered)

print(count)
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
