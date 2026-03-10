#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime as dt, json, os, re, subprocess
from pathlib import Path
from typing import Any, Dict, List

SESSIONS_DIR = Path(os.path.expanduser("~/.openclaw/agents/main/sessions"))
CACHE_PATH = Path("/home/baiiy1/.openclaw/workspace/scripts/ops/.codex_sessions_cache.json")


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00','Z')


def make_result(ok: bool, partial: bool=False, reason: str|None=None, next_action: str|None=None, **extra: Any) -> Dict[str, Any]:
    out: Dict[str, Any] = {"ok": ok, "partial": partial, "generatedAt": iso_now()}
    if reason:
        out["reason"] = reason
    if next_action:
        out["nextAction"] = next_action
    out.update(extra)
    return out


def list_history(limit: int) -> Dict[str, Any]:
    if not SESSIONS_DIR.exists():
        return make_result(False, reason=f"sessions dir not found: {SESSIONS_DIR}", next_action="check OpenClaw agent path")

    items: List[Dict[str, Any]] = []
    for p in sorted(SESSIONS_DIR.glob("*.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True):
        sid = p.stem
        m = re.search(r"topic-(\d{17,22})", p.name)
        channel_id = m.group(1) if m else None
        model = None
        started = None
        try:
            with p.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    o = json.loads(line)
                    t = o.get("type")
                    if t == "session" and not started:
                        started = o.get("timestamp")
                    if t == "model_change":
                        model = o.get("modelId") or model
        except Exception:
            pass
        items.append({
            "sessionId": sid,
            "channelId": channel_id,
            "model": model,
            "startedAt": started,
            "updatedAt": dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc).isoformat().replace('+00:00','Z'),
            "file": str(p),
        })
        if len(items) >= limit:
            break

    return make_result(True, count=len(items), sessions=items)


def refresh_cache() -> Dict[str, Any]:
    status_out = ""
    status_err = None
    try:
        proc = subprocess.run(["openclaw", "status"], capture_output=True, text=True, check=False)
        status_out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        if proc.returncode != 0:
            status_err = f"openclaw status exit={proc.returncode}"
    except FileNotFoundError:
        status_err = "openclaw command not found"

    parsed_rows: List[Dict[str, Any]] = []
    for line in status_out.splitlines():
        m = re.search(r"\│\s*([^│]+?)\s*\│\s*([^│]+?)\s*\│\s*([^│]+?)\s*\│\s*([^│]+?)\s*\│\s*([^│]+?)\s*\│", line)
        if not m:
            continue
        key, kind, age, model, token = [x.strip() for x in m.groups()]
        if key.lower() == "key":
            continue
        parsed_rows.append({"key": key, "kind": kind, "age": age, "model": model, "token": token})

    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"generatedAt": iso_now(), "rows": parsed_rows, "statusError": status_err}
    CACHE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if status_err and not parsed_rows:
        return make_result(False, partial=True, reason=status_err, next_action="ensure openclaw in PATH", cachePath=str(CACHE_PATH), refreshed=0)
    return make_result(True, partial=bool(status_err), reason=status_err, cachePath=str(CACHE_PATH), refreshed=len(parsed_rows))


def main() -> int:
    ap = argparse.ArgumentParser(description="Codex sessions history/refresh for ops panel")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--history", action="store_true")
    g.add_argument("--refresh", action="store_true")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.history:
        out = list_history(max(1, args.limit))
    else:
        out = refresh_cache()

    print(json.dumps(out, ensure_ascii=False, indent=2) if args.json or True else out)
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
