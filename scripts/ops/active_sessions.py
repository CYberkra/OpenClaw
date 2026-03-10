#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime as dt, json, os, re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

SESSIONS_DIR = Path(os.path.expanduser("~/.openclaw/agents/main/sessions"))

def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00','Z')

def out(ok: bool, partial: bool=False, reason: str|None=None, next_action: str|None=None, **extra: Any) -> Dict[str, Any]:
    d = {"ok": ok, "partial": partial, "generatedAt": iso_now()}
    if reason: d["reason"] = reason
    if next_action: d["nextAction"] = next_action
    d.update(extra)
    return d

def collect(channel: str|None, minutes: int, limit: int) -> Dict[str, Any]:
    if not SESSIONS_DIR.exists():
        return out(False, reason=f"sessions dir not found: {SESSIONS_DIR}", next_action="check OpenClaw runtime path")

    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=minutes)
    by_channel: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    scanned = 0

    for p in sorted(SESSIONS_DIR.glob("*.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True):
        scanned += 1
        m = re.search(r"topic-(\d{17,22})", p.name)
        channel_id = m.group(1) if m else "unknown"
        if channel and channel_id != channel:
            continue

        mtime = dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc)
        if mtime < cutoff:
            continue

        sid = p.stem
        by_channel[channel_id].append({
            "sessionId": sid,
            "updatedAt": mtime.isoformat().replace('+00:00','Z'),
            "file": str(p),
        })
        if scanned >= limit:
            break

    channels = []
    for cid, sess in sorted(by_channel.items(), key=lambda kv: len(kv[1]), reverse=True):
        channels.append({
            "channelId": cid,
            "activeSessionCount": len(sess),
            "latestActiveAt": max(s["updatedAt"] for s in sess),
            "topSessionIds": [s["sessionId"] for s in sess[:5]],
        })

    partial = any(c["channelId"] == "unknown" for c in channels)
    return out(True, partial=partial, reason="some sessions not bound to topic channel" if partial else None, windowMinutes=minutes, scannedFiles=scanned, channels=channels)


def main() -> int:
    ap = argparse.ArgumentParser(description="List active sessions by channel")
    ap.add_argument("--channel", default=None)
    ap.add_argument("--minutes", type=int, default=1440)
    ap.add_argument("--limit", type=int, default=1000)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    data = collect(args.channel, max(1,args.minutes), max(1,args.limit))
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0 if data.get("ok") else 1

if __name__ == "__main__":
    raise SystemExit(main())
