#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
from typing import Any, Dict


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def result(ok: bool, data: Dict[str, Any] | None = None, *, partial: bool = False, reason: str = "", next_action: str = "") -> Dict[str, Any]:
    out: Dict[str, Any] = {"ok": ok, "partial": partial, "generatedAt": now_iso()}
    if data:
        out.update(data)
    if reason:
        out["reason"] = reason
    if next_action:
        out["nextAction"] = next_action
    return out


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def snapshot() -> Dict[str, Any]:
    data: Dict[str, Any] = {"host": os.uname().nodename}
    partial = False
    reasons = []

    # cpu load
    try:
        l1, l5, l15 = os.getloadavg()
        data["cpuLoad"] = {"1m": l1, "5m": l5, "15m": l15}
    except Exception as exc:
        partial = True
        reasons.append(f"cpu load unavailable: {exc}")

    # memory
    code, out, _ = run(["free", "-m"])
    if code == 0 and out:
        lines = [x for x in out.splitlines() if x.lower().startswith("mem:")]
        if lines:
            p = lines[0].split()
            data["memoryMB"] = {"total": int(p[1]), "used": int(p[2]), "free": int(p[3])}
    else:
        partial = True
        reasons.append("free command unavailable")

    # disk
    du = shutil.disk_usage("/")
    data["diskRootGB"] = {"total": round(du.total / (1024**3), 2), "used": round(du.used / (1024**3), 2), "free": round(du.free / (1024**3), 2)}

    # network
    code, out, _ = run(["bash", "-lc", "ip -brief address | head -n 5"])
    if code == 0:
        data["network"] = out.splitlines()
    else:
        partial = True
        reasons.append("ip command unavailable")

    # openclaw gateway status
    code, out, err = run(["openclaw", "gateway", "status"])
    if code == 0:
        data["openclawGateway"] = out
    else:
        partial = True
        reasons.append(f"gateway status failed: {err or out or code}")

    if partial:
        return result(True, data, partial=True, reason="; ".join(reasons), next_action="Install missing commands or run with higher privileges if needed")
    return result(True, data)


def main() -> int:
    ap = argparse.ArgumentParser(description="Local health snapshot")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = snapshot()
    print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else json.dumps(out, ensure_ascii=False))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
