#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") <state> [message]" >&2
}

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi

input_state="$1"
shift || true
text="${*:-}"

case "$input_state" in
  coding|debugging|reviewing|idle)
    state="$input_state"
    ;;
  *)
    state="reviewing"
    ;;
esac

BASE_URL="${STAR_OFFICE_BASE_URL:-http://127.0.0.1:19000}"
URL="${BASE_URL%/}/set_state"

payload="$(python3 - "$state" "$text" <<'PY'
import json
import sys
state = sys.argv[1]
text = sys.argv[2]
print(json.dumps({"state": state, "text": text}, ensure_ascii=False))
PY
)"

http_code="$(curl -sS -o /tmp/star-office-state.resp -w "%{http_code}" \
  -X POST "$URL" \
  -H "Content-Type: application/json" \
  --data "$payload" || true)"

if [[ "$http_code" =~ ^2[0-9][0-9]$ ]]; then
  echo "[ok] state=$state text=${text:-<empty>}"
  exit 0
fi

echo "[fail] state=$state code=${http_code:-curl_error} url=$URL" >&2
if [[ -s /tmp/star-office-state.resp ]]; then
  head -c 300 /tmp/star-office-state.resp >&2 || true
  echo >&2
fi
exit 1
