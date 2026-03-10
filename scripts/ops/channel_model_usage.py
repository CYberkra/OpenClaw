#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime as dt, json, os, re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict

SESSIONS_DIR = Path(os.path.expanduser("~/.openclaw/agents/main/sessions"))

def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00','Z')

def result(ok: bool, partial: bool=False, reason: str|None=None, next_action: str|None=None, **extra: Any) -> Dict[str, Any]:
    d = {"ok": ok, "partial": partial, "generatedAt": iso_now()}
    if reason: d["reason"] = reason
    if next_action: d["nextAction"] = next_action
    d.update(extra)
    return d

def parse_model_usage(guild: str|None, channel: str|None, limit: int) -> Dict[str, Any]:
    if not SESSIONS_DIR.exists():
        return result(False, reason=f"sessions dir not found: {SESSIONS_DIR}", next_action="check OpenClaw runtime data path")

    usage = defaultdict(Counter)
    scanned = 0
    for p in sorted(SESSIONS_DIR.glob("*.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True):
        scanned += 1
        m = re.search(r"topic-(\d{17,22})", p.name)
        channel_id = m.group(1) if m else "unknown"
        if channel and channel_id != channel:
            continue

        models = set()
        try:
            with p.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    o = json.loads(line)
                    if o.get("type") == "model_change":
                        mid = o.get("modelId") or "unknown"
                        models.add(mid)
        except Exception:
            models.add("parse_error")

        for mid in models:
            usage[channel_id][mid] += 1

        if scanned >= limit:
            break

    rows = []
    for cid, counter in sorted(usage.items(), key=lambda kv: sum(kv[1].values()), reverse=True):
        rows.append({"channelId": cid, "totalSessions": int(sum(counter.values())), "models": dict(counter)})

    partial = any(r["channelId"] == "unknown" for r in rows)
    return result(True, partial=partial, reason="some sessions are not mapped to topic channel" if partial else None, guildId=guild, scannedFiles=scanned, channels=rows)


def main() -> int:
    ap = argparse.ArgumentParser(description="Aggregate model usage by channel/thread from local OpenClaw sessions")
    ap.add_argument("--guild", default=None)
    ap.add_argument("--channel", default=None)
    ap.add_argument("--limit", type=int, default=500)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    out = parse_model_usage(args.guild, args.channel, max(1,args.limit))
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("ok") else 1

if __name__ == "__main__":
    raise SystemExit(main())
