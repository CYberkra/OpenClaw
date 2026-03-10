#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/baiiy1/.openclaw/workspace/research/star-office-ui"
BASE_URL="${STAR_OFFICE_BASE_URL:-http://127.0.0.1:19000}"

echo "[1/6] 检查项目目录"
if [[ ! -d "$ROOT" ]]; then
  echo "❌ 未找到 $ROOT"
  echo "请先执行: git clone https://github.com/ringhyacinth/Star-Office-UI.git $ROOT"
  exit 1
fi

cd "$ROOT"

echo "[2/6] 检查依赖命令"
command -v python3 >/dev/null || { echo "❌ python3 未安装"; exit 1; }
command -v curl >/dev/null || { echo "❌ curl 未安装"; exit 1; }

echo "[3/6] 检查 Python 版本 >=3.10"
python3 - <<'PY'
import sys
v=sys.version_info
ok=(v.major==3 and v.minor>=10) or (v.major>3)
print(f"Python version: {v.major}.{v.minor}.{v.micro}")
raise SystemExit(0 if ok else 1)
PY

echo "[4/6] 安装/校验依赖"
python3 -m pip install -r backend/requirements.txt >/dev/null

if [[ ! -f state.json ]]; then
  echo "[info] state.json 不存在，正在从模板创建"
  cp state.sample.json state.json
fi

echo "[5/6] 关键变量提示（按需）"
echo "  - STAR_OFFICE_STATE_FILE: 自定义状态文件路径"
echo "  - JOIN_KEY / AGENT_NAME / OFFICE_URL: 访客接入办公室必填"
echo "  - STAR_OFFICE_BASE_URL: 覆盖默认 $BASE_URL"

PID=""
cleanup() {
  if [[ -n "$PID" ]] && kill -0 "$PID" 2>/dev/null; then
    kill "$PID" >/dev/null 2>&1 || true
    wait "$PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

echo "[6/6] 启动临时后端并执行 smoke test"
python3 backend/app.py >/tmp/star-office-smoke.log 2>&1 &
PID=$!

for _ in {1..25}; do
  if curl -fsS "$BASE_URL/health" >/dev/null 2>&1; then
    break
  fi
  sleep 0.4
done

if ! curl -fsS "$BASE_URL/health" >/dev/null 2>&1; then
  echo "❌ 后端未在 $BASE_URL 就绪"
  echo "--- backend log ---"
  tail -n 80 /tmp/star-office-smoke.log || true
  exit 1
fi

python3 scripts/smoke_test.py --base-url "$BASE_URL"
echo "✅ smoke test 通过（本地最小部署可用）"
