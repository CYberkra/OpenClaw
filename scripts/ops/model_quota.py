#!/usr/bin/env python3
"""Model quota inspector for Discord ops panel.

Data source priority:
1) Parse `openclaw status` real output for runtime/session token quota hints.
2) Detect provider credential/config presence from environment and OpenClaw config files.
3) Billing APIs are not called; providers are marked unavailable with reason.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROVIDERS = ["openai", "anthropic", "google", "groq", "deepseek"]

PROVIDER_ENV_KEYS = {
    "openai": ["OPENAI_API_KEY"],
    "anthropic": ["ANTHROPIC_API_KEY"],
    "google": ["GOOGLE_API_KEY", "GEMINI_API_KEY"],
    "groq": ["GROQ_API_KEY"],
    "deepseek": ["DEEPSEEK_API_KEY"],
}

PROVIDER_CONFIG_PATTERNS = {
    "openai": [r"\bopenai\b", r"OPENAI_API_KEY"],
    "anthropic": [r"\banthropic\b", r"ANTHROPIC_API_KEY"],
    "google": [r"\bgoogle\b", r"\bgemini\b", r"GOOGLE_API_KEY", r"GEMINI_API_KEY"],
    "groq": [r"\bgroq\b", r"GROQ_API_KEY"],
    "deepseek": [r"\bdeepseek\b", r"DEEPSEEK_API_KEY"],
}


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def run_openclaw_status() -> Tuple[Optional[str], Optional[str]]:
    try:
        proc = subprocess.run(
            ["openclaw", "status"],
            check=False,
            capture_output=True,
            text=True,
        )
        out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        if proc.returncode != 0 and not out.strip():
            return None, f"openclaw status failed with code {proc.returncode}"
        return out, None
    except FileNotFoundError:
        return None, "openclaw command not found"
    except Exception as exc:
        return None, f"openclaw status error: {exc}"


def parse_sessions(lines: List[str]) -> Dict[str, Any]:
    items: List[Dict[str, Any]] = []
    for line in lines:
        # Example: │ ... │ ... │ ... │ gpt-5.3-codex │ 39k/272k (14%) · 🗄️ 99% cached │
        m = re.search(r"\│\s*([^│]+?)\s*\│\s*([^│]+?)\s*\│\s*([^│]+?)\s*\│\s*([^│]+?)\s*\│\s*([^│]+?)\s*\│", line)
        if not m:
            continue
        key, kind, age, model, tokens = [x.strip() for x in m.groups()]
        if key.lower() == "key" or "/" not in tokens:
            continue

        tm = re.search(r"(unknown|\d+[kKmM]?)\s*/\s*(\d+[kKmM]?)(?:\s*\(([^)]+)\))?", tokens)
        if not tm:
            continue

        used_raw, limit_raw, pct = tm.groups()
        used = parse_count(used_raw) if used_raw.lower() != "unknown" else None
        limit = parse_count(limit_raw)
        remaining = (limit - used) if (used is not None and limit is not None) else None

        items.append(
            {
                "key": key,
                "kind": kind,
                "age": age,
                "model": model,
                "used": used,
                "limit": limit,
                "remaining": remaining,
                "usagePct": pct,
                "source": "openclaw status sessions table",
            }
        )

    runtime: Dict[str, Any] = {
        "source": "openclaw status",
        "available": bool(items),
        "reason": None if items else "No parseable session token quota found in openclaw status",
        "sessions": items,
    }

    if items:
        # runtime quota: choose newest line's limit as active context cap hint
        runtime["activeSession"] = items[0]
        limits = [i["limit"] for i in items if isinstance(i.get("limit"), int)]
        if limits:
            runtime["maxObservedLimit"] = max(limits)

    return runtime


def parse_count(v: str) -> Optional[int]:
    v = v.strip().lower()
    m = re.match(r"^(\d+(?:\.\d+)?)([km]?)$", v)
    if not m:
        return None
    n = float(m.group(1))
    unit = m.group(2)
    if unit == "k":
        n *= 1000
    elif unit == "m":
        n *= 1_000_000
    return int(n)


def detect_provider_config(provider: str) -> Dict[str, Any]:
    env_hits = [k for k in PROVIDER_ENV_KEYS.get(provider, []) if os.getenv(k)]

    cfg_paths = [
        Path.home() / ".openclaw" / "openclaw.json",
        Path.home() / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json",
    ]

    file_hits: List[str] = []
    patterns = [re.compile(pat, re.IGNORECASE) for pat in PROVIDER_CONFIG_PATTERNS[provider]]
    for p in cfg_paths:
        try:
            if not p.exists() or p.stat().st_size > 2_000_000:
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            if any(rx.search(text) for rx in patterns):
                file_hits.append(str(p))
        except Exception:
            continue

    hints: List[str] = []
    if env_hits:
        hints.append(f"env:{','.join(env_hits)}")
    if file_hits:
        hints.append("config:" + ",".join(file_hits))

    available = False
    reason = (
        "Billing/usage API not queried by this script; only runtime quota and credential/config presence can be detected"
    )

    return {
        "name": provider,
        "available": available,
        "reason": reason,
        "usage": None,
        "resetAt": None,
        "detectedConfig": bool(hints),
        "configSource": hints if hints else [],
    }


def build_result(provider: Optional[str]) -> Dict[str, Any]:
    status_out, status_err = run_openclaw_status()
    runtime = {
        "source": "openclaw status",
        "available": False,
        "reason": status_err or "openclaw status output unavailable",
        "sessions": [],
    }
    if status_out:
        runtime = parse_sessions(status_out.splitlines())

    names = [provider] if provider else PROVIDERS
    providers = [detect_provider_config(p) for p in names]

    return {
        "ok": True,
        "generatedAt": now_iso(),
        "runtime": runtime,
        "providers": providers,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Query runtime/provider model quota info")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Return all providers")
    group.add_argument("--provider", choices=PROVIDERS, help="Return single provider")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    result = build_result(args.provider)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Use --json for structured output")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
