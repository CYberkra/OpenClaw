#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime as dt, json, subprocess, hashlib
from pathlib import Path
from typing import Any, Dict

GPR_KEYWORD = 'gpr'

ROOT = Path('/home/baiiy1/.openclaw/workspace')
SCRIPTS = ROOT / 'scripts' / 'ops'
STATE = ROOT / '.cache' / 'ops_panel_confirm_state.json'
TTL_SECONDS = 300

def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00','Z')

def j(ok: bool, partial: bool=False, reason: str|None=None, next_action: str|None=None, details: Any=None, **extra: Any) -> Dict[str, Any]:
    d = {"ok": ok, "partial": partial, "generatedAt": iso_now(), "details": details if details is not None else {}}
    if reason: d['reason'] = reason
    if next_action: d['nextAction'] = next_action
    d.update(extra)
    return d

def _safe_iso_mtime(path: Path) -> str:
    try:
        return dt.datetime.fromtimestamp(path.stat().st_mtime, tz=dt.timezone.utc).isoformat().replace('+00:00', 'Z')
    except Exception:
        return ''


def _latest_gpr_reports(limit: int = 5) -> list[Dict[str, str]]:
    reports_dir = ROOT / 'reports'
    if not reports_dir.exists():
        return []
    items: list[tuple[float, Path]] = []
    for p in reports_dir.rglob('*'):
        if not p.is_file():
            continue
        if GPR_KEYWORD in p.name.lower():
            try:
                items.append((p.stat().st_mtime, p))
            except Exception:
                continue
    items.sort(key=lambda x: x[0], reverse=True)
    out = []
    for _, p in items[:limit]:
        out.append({"path": str(p.relative_to(ROOT)), "mtime": _safe_iso_mtime(p)})
    return out


def _latest_gpr_memory_notes(limit: int = 5) -> list[str]:
    memory_dir = ROOT / 'memory'
    if not memory_dir.exists():
        return []
    files = sorted(memory_dir.glob('*.md'), key=lambda p: p.stat().st_mtime, reverse=True)
    notes: list[str] = []
    for f in files:
        try:
            lines = f.read_text(encoding='utf-8', errors='ignore').splitlines()
        except Exception:
            continue
        for line in lines:
            s = line.strip()
            if not s:
                continue
            if GPR_KEYWORD in s.lower():
                notes.append(f"{f.name}: {s[:180]}")
                if len(notes) >= limit:
                    return notes
    return notes


def _gpr_isolation_status() -> Dict[str, Any]:
    d = ROOT / 'isolated' / 'GPR_GUI_evolve'
    if not d.exists() or not d.is_dir():
        return {
            "exists": False,
            "lastUpdated": None,
            "note": "isolated/GPR_GUI_evolve/ 不存在，无法检查近期变更"
        }
    last_mtime = 0.0
    last_path: Path | None = None
    for p in d.rglob('*'):
        if not p.exists():
            continue
        try:
            m = p.stat().st_mtime
        except Exception:
            continue
        if m > last_mtime:
            last_mtime = m
            last_path = p
    note = "已检查目录近期变更"
    if last_path is not None:
        rel = str(last_path.relative_to(ROOT))
        note = f"最近变更: {rel}"
    return {
        "exists": True,
        "lastUpdated": dt.datetime.fromtimestamp(last_mtime, tz=dt.timezone.utc).isoformat().replace('+00:00', 'Z') if last_mtime else None,
        "note": note,
    }


def gpr_progress() -> Dict[str, Any]:
    latest_reports = _latest_gpr_reports(limit=5)
    latest_notes = _latest_gpr_memory_notes(limit=5)
    isolation = _gpr_isolation_status()

    partial = False
    summary_lines = []
    if latest_reports:
        summary_lines.append(f"reports 命中 {len(latest_reports)} 条最新 GPR 报告")
    else:
        partial = True
        summary_lines.append("reports 未命中 GPR 报告文件")

    if latest_notes:
        summary_lines.append(f"memory 命中 {len(latest_notes)} 条 GPR 相关笔记")
    else:
        partial = True
        summary_lines.append("memory 未命中 GPR 关键词条目")

    if isolation.get('exists'):
        summary_lines.append(f"隔离目录存在，lastUpdated={isolation.get('lastUpdated')}")
    else:
        partial = True
        summary_lines.append("隔离目录不存在")

    return {
        "ok": True,
        "partial": partial,
        "generatedAt": iso_now(),
        "summary": "\n".join(summary_lines[:3]),
        "latestReports": latest_reports,
        "latestMemoryNotes": latest_notes,
        "isolationStatus": isolation,
        "details": {},
    }


def call_py(script: str, args: list[str]) -> Dict[str, Any]:
    p = subprocess.run(['python3', str(SCRIPTS / script), *args, '--json'], capture_output=True, text=True, check=False)
    raw = (p.stdout or '').strip() or (p.stderr or '').strip()
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            obj.setdefault('dispatcherRc', p.returncode)
            return obj
    except Exception:
        pass
    return j(False, partial=True, reason='script output is not valid JSON', next_action='check script stderr', script=script, rc=p.returncode, raw=raw[:1000])

def load_state() -> Dict[str, Any]:
    if not STATE.exists():
        return {"pending": {}}
    try:
        return json.loads(STATE.read_text(encoding='utf-8'))
    except Exception:
        return {"pending": {}}

def save_state(st: Dict[str, Any]) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding='utf-8')

def slot_of(action: str) -> str:
    if 'gateway_restart' in action:
        return 'gateway_restart'
    if 'channel_delete' in action:
        return 'channel_delete'
    return action

def make_code(slot: str, operator: str, target: str) -> str:
    seed = f'{slot}|{operator}|{target}|{int(dt.datetime.now().timestamp())}'
    return hashlib.sha1(seed.encode()).hexdigest()[:8].upper()

def prepare(action: str, operator: str, target: str) -> Dict[str, Any]:
    if not operator:
        return j(False, reason='missing operator', next_action='pass operator id in params')
    st = load_state()
    slot = slot_of(action)
    code = make_code(slot, operator, target)
    exp = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=TTL_SECONDS)).isoformat().replace('+00:00','Z')
    st['pending'][slot] = {"operator": operator, "target": target, "confirmCode": code, "expiresAt": exp}
    save_state(st)
    return j(True, action=action, slot=slot, phase='prepare', operator=operator, target=target, confirmCode=code, ttlSeconds=TTL_SECONDS, expiresAt=exp)

def commit(action: str, operator: str, target: str, confirm_code: str, channel_id_again: str|None=None) -> Dict[str, Any]:
    st = load_state()
    slot = slot_of(action)
    rec = st.get('pending', {}).get(slot)
    if not rec:
        return j(False, reason='no pending confirmation', next_action='run prepare action first')
    now = dt.datetime.now(dt.timezone.utc)
    exp = dt.datetime.fromisoformat(rec['expiresAt'].replace('Z','+00:00'))
    if now > exp:
        return j(False, reason='confirmation expired', next_action='restart prepare step')
    if rec['operator'] != operator:
        return j(False, reason='operator mismatch', next_action='same operator must commit')
    if rec['target'] != target:
        return j(False, reason='target mismatch', next_action='commit with same target')
    if rec['confirmCode'] != confirm_code:
        return j(False, reason='confirm_code mismatch', next_action='use generated confirmCode')
    if slot == 'channel_delete' and (channel_id_again or '') != target:
        return j(False, reason='channel_id_again mismatch', next_action='input exact selected channel id')

    if slot == 'gateway_restart':
        p1 = subprocess.run(['openclaw','gateway','restart'], capture_output=True, text=True, check=False)
        p2 = subprocess.run(['openclaw','gateway','status'], capture_output=True, text=True, check=False)
        res = j(p1.returncode == 0, partial=p2.returncode != 0, action=action, restartRc=p1.returncode, restartOut=(p1.stdout or p1.stderr).strip()[:500], statusRc=p2.returncode, statusOut=(p2.stdout or p2.stderr).strip()[:500])
    else:
        res = j(True, partial=True, action=action, reason='validated only; delete must be executed by main process via message.channel-delete', next_action='call message.channel-delete with validated target', validatedTarget=target)

    st.get('pending', {}).pop(slot, None)
    save_state(st)
    return res

def dispatch(action: str, params: Dict[str, Any]) -> Dict[str, Any]:
    if action == 'quota.all':
        return call_py('model_quota.py', ['--all'])
    if action == 'ops.gpr.progress':
        return gpr_progress()
    if action == 'quota.provider':
        provider = params.get('provider')
        if not provider:
            return j(False, reason='missing provider')
        return call_py('model_quota.py', ['--provider', str(provider)])
    if action == 'codex.sessions.history':
        return call_py('codex_sessions.py', ['--history', '--limit', str(params.get('limit', 20))])
    if action == 'codex.sessions.refresh':
        return call_py('codex_sessions.py', ['--refresh'])
    if action == 'usage.channel_models':
        args = ['--limit', str(params.get('limit', 500))]
        if params.get('guild'): args += ['--guild', str(params['guild'])]
        if params.get('channel'): args += ['--channel', str(params['channel'])]
        return call_py('channel_model_usage.py', args)
    if action == 'sessions.active':
        args = ['--minutes', str(params.get('minutes', 1440)), '--limit', str(params.get('limit', 1000))]
        if params.get('channel'): args += ['--channel', str(params['channel'])]
        return call_py('active_sessions.py', args)
    if action == 'health.snapshot':
        return call_py('health_snapshot.py', [])

    if action in {'ops.model.switch.channel.preview', 'ops.model.switch.prepare', 'ops.model.switch.commit', 'ops.model.switch.bulk.prepare', 'ops.model.switch.bulk.commit'}:
        return call_py('model_switch.py', ['--action', action, '--params', json.dumps(params, ensure_ascii=False)])

    if action == 'danger.gateway_restart.prepare':
        return prepare(action, str(params.get('operator','')), 'gateway')
    if action == 'danger.gateway_restart.commit':
        return commit(action, str(params.get('operator','')), 'gateway', str(params.get('confirm_code','')))
    if action == 'danger.channel_delete.prepare':
        ch = str(params.get('channel_id',''))
        if not ch:
            return j(False, reason='missing channel_id')
        return prepare(action, str(params.get('operator','')), ch)
    if action == 'danger.channel_delete.commit':
        ch = str(params.get('channel_id',''))
        if not ch:
            return j(False, reason='missing channel_id')
        return commit(action, str(params.get('operator','')), ch, str(params.get('confirm_code','')), str(params.get('channel_id_again','')))

    return j(False, reason=f'unknown action: {action}', next_action='check ops_panel_v2_handlers.md')

def classify_error(reason: str) -> str:
    r = (reason or '').lower()
    if any(k in r for k in ['missing', 'invalid', 'mismatch', 'params', 'scope', 'model alias', 'channel_id']):
        return 'PARAM_MISSING_OR_INVALID'
    if any(k in r for k in ['no session', 'no active sessions', 'no pending', 'expired']):
        return 'NO_SESSION_OR_CONFIRMATION'
    if any(k in r for k in ['permission', 'forbidden', 'denied', 'operator mismatch']):
        return 'PERMISSION_DENIED'
    return 'OPERATION_FAILED'


def attach_error_template(res: Dict[str, Any]) -> Dict[str, Any]:
    if res.get('ok'):
        return res
    reason = str(res.get('reason', 'operation failed'))
    code = classify_error(reason)
    templates = {
        'PARAM_MISSING_OR_INVALID': '❌ 参数不完整或不合法：{reason}。请按面板提示补齐后重试。',
        'NO_SESSION_OR_CONFIRMATION': '⚠️ 未找到有效会话/确认记录：{reason}。请先执行查询或重新发起 prepare。',
        'PERMISSION_DENIED': '⛔ 权限校验未通过：{reason}。请使用同一操作者或确认权限后重试。',
        'OPERATION_FAILED': '❌ 操作失败：{reason}。可根据 nextAction 继续处理。',
    }
    res['errorCode'] = code
    res['userMessage'] = templates.get(code, templates['OPERATION_FAILED']).format(reason=reason)
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description='Ops panel dispatcher')
    ap.add_argument('--action', required=True)
    ap.add_argument('--params', default='{}')
    args = ap.parse_args()
    try:
        params = json.loads(args.params)
        if not isinstance(params, dict):
            raise ValueError('params must be object')
    except Exception as e:
        print(json.dumps(attach_error_template(j(False, reason=f'invalid params json: {e}')), ensure_ascii=False, indent=2))
        return 1
    res = attach_error_template(dispatch(args.action, params))
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res.get('ok') else 1

if __name__ == '__main__':
    raise SystemExit(main())
