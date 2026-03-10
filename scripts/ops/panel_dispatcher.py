#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime as dt, json, subprocess, hashlib
from pathlib import Path
from typing import Any, Dict

ROOT = Path('/home/baiiy1/.openclaw/workspace')
SCRIPTS = ROOT / 'scripts' / 'ops'
STATE = ROOT / '.cache' / 'ops_panel_confirm_state.json'
TTL_SECONDS = 300

def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00','Z')

def j(ok: bool, partial: bool=False, reason: str|None=None, next_action: str|None=None, **extra: Any) -> Dict[str, Any]:
    d = {"ok": ok, "partial": partial, "generatedAt": iso_now()}
    if reason: d['reason'] = reason
    if next_action: d['nextAction'] = next_action
    d.update(extra)
    return d

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
        print(json.dumps(j(False, reason=f'invalid params json: {e}'), ensure_ascii=False, indent=2))
        return 1
    res = dispatch(args.action, params)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res.get('ok') else 1

if __name__ == '__main__':
    raise SystemExit(main())
