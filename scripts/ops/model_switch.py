#!/usr/bin/env python3
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path('/home/baiiy1/.openclaw/workspace')
STATE = ROOT / '.cache' / 'ops_panel_confirm_state.json'
SESSIONS_DIR = Path(os.path.expanduser('~/.openclaw/agents/main/sessions'))
TTL_SECONDS = 300
CHANNEL_RE = re.compile(r'^\d{17,22}$')

MODEL_WHITELIST = {
    'codex5.2-main': 'codex5.2-main',
    'codex5.2-backup': 'codex5.2-backup',
    'miaomiao': 'miaomiao',
    'kimi for coding': 'Kimi for Coding',
    'kimi-for-coding': 'Kimi for Coding',
    'kimi': 'Kimi for Coding',
}


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00', 'Z')


def out(ok: bool, partial: bool = False, reason: str | None = None, next_action: str | None = None, details: Any = None, **extra: Any) -> Dict[str, Any]:
    d: Dict[str, Any] = {
        'ok': ok,
        'partial': partial,
        'generatedAt': iso_now(),
        'details': details if details is not None else {},
    }
    if reason:
        d['reason'] = reason
    if next_action:
        d['nextAction'] = next_action
    d.update(extra)
    return d


def normalize_model(raw: str | None) -> str | None:
    if not raw:
        return None
    return MODEL_WHITELIST.get(raw.strip().lower())


def validate_channel_id(channel_id: str | None) -> bool:
    return bool(channel_id and CHANNEL_RE.fullmatch(str(channel_id)))


def load_state() -> Dict[str, Any]:
    if not STATE.exists():
        return {'pending': {}}
    try:
        return json.loads(STATE.read_text(encoding='utf-8'))
    except Exception:
        return {'pending': {}}


def save_state(st: Dict[str, Any]) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding='utf-8')


def make_code(slot: str, operator: str, channel_id: str, model: str) -> str:
    seed = f'{slot}|{operator}|{channel_id}|{model}|{int(dt.datetime.now().timestamp())}'
    return hashlib.sha1(seed.encode()).hexdigest()[:8].upper()


def run_cmd(cmd: List[str], max_chars: int = 2000) -> Dict[str, Any]:
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return {
        'rc': p.returncode,
        'stdout': (p.stdout or '').strip()[:max_chars],
        'stderr': (p.stderr or '').strip()[:max_chars],
        'cmd': cmd,
    }


def list_sessions(limit: int = 500) -> List[Dict[str, Any]]:
    r = run_cmd(['openclaw', 'sessions', '--json'], max_chars=500000)
    if r['rc'] != 0:
        return []
    try:
        obj = json.loads(r['stdout'] or '{}')
        rows = obj.get('sessions', []) if isinstance(obj, dict) else []
        if not isinstance(rows, list):
            return []
        return rows[:max(1, min(limit, 5000))]
    except Exception:
        return []


def find_session_by_key(session_key: str) -> Optional[Dict[str, Any]]:
    for s in list_sessions(limit=2000):
        if str(s.get('key', '')) == session_key:
            return s
    return None


def apply_model_to_session(session_key: str, model: str) -> Dict[str, Any]:
    payload = f'/model {model}'
    details: Dict[str, Any] = {
        'sessionKey': session_key,
        'model': model,
        'ok': False,
        'rc': 1,
        'stdout': '',
        'stderr': '',
        'strategy': '',
        'attempts': [],
    }

    # Strategy 1 (preferred): sessions_send equivalent path
    # 先从 sessions_list 解析 session key -> UUID sessionId，再向该会话发送 /model 指令
    ss = find_session_by_key(session_key)
    if ss and ss.get('sessionId'):
        sid = str(ss.get('sessionId'))
        r1 = run_cmd(['openclaw', 'agent', '--session-id', sid, '--message', payload, '--json'])
        details['attempts'].append({
            'strategy': 'sessions_list.resolve_key_to_sessionId -> openclaw agent --session-id <uuid> --message "/model <model>"',
            'sessionId': sid,
            'rc': r1['rc'],
            'stdout': r1['stdout'],
            'stderr': r1['stderr'],
        })
        if r1['rc'] == 0:
            details.update({'ok': True, 'rc': 0, 'stdout': r1['stdout'], 'stderr': r1['stderr'], 'strategy': 'resolved_session_id'})
            return details

    # Strategy 2 (fallback): legacy direct session-id param (兼容原链路)
    r2 = run_cmd(['openclaw', 'agent', '--session-id', session_key, '--message', payload, '--json'])
    details['attempts'].append({
        'strategy': 'legacy_direct_session_key -> openclaw agent --session-id <session_key> --message "/model <model>"',
        'rc': r2['rc'],
        'stdout': r2['stdout'],
        'stderr': r2['stderr'],
    })
    details.update({
        'ok': (r2['rc'] == 0),
        'rc': r2['rc'],
        'stdout': r2['stdout'],
        'stderr': r2['stderr'],
        'strategy': 'legacy_direct_session_key',
    })
    return details


def list_active_sessions_by_channel(channel_id: str, minutes: int = 1440, limit: int = 200) -> List[str]:
    if not SESSIONS_DIR.exists():
        return []
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=max(1, minutes))
    found: List[str] = []
    pat = re.compile(r'topic-(\d{17,22})')
    for p in sorted(SESSIONS_DIR.glob('*.jsonl'), key=lambda x: x.stat().st_mtime, reverse=True):
        m = pat.search(p.name)
        if not m or m.group(1) != channel_id:
            continue
        mtime = dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc)
        if mtime < cutoff:
            continue
        found.append(p.stem)
        if len(found) >= limit:
            break
    return found


def do_channel_preview(params: Dict[str, Any]) -> Dict[str, Any]:
    channel_id = str(params.get('channel_id', ''))
    if not validate_channel_id(channel_id):
        return out(False, partial=True, reason='invalid channel_id format', next_action='use discord snowflake id', details={'channel_id': channel_id})

    target_key = f'agent:main:discord:channel:{channel_id}'
    ss = find_session_by_key(target_key)
    if not ss:
        return out(
            False,
            partial=True,
            reason='no session found for channel',
            next_action='send a message in this channel to create/refresh session, then retry preview',
            details={'channel_id': channel_id, 'session_key': None, 'current_model': None, 'updated_at': None},
            strategy='sessions_list.by_channel_key',
        )

    return out(
        True,
        details={
            'channel_id': channel_id,
            'session_key': ss.get('key'),
            'current_model': ss.get('model') or ss.get('modelOverride'),
            'updated_at': ss.get('updatedAt'),
        },
        strategy='sessions_list.by_channel_key',
    )


def do_prepare(params: Dict[str, Any]) -> Dict[str, Any]:
    scope = str(params.get('scope', 'current_session'))
    channel_id = str(params.get('channel_id', ''))
    session_key = str(params.get('session_key', ''))
    model = normalize_model(params.get('model'))

    if not model:
        return out(False, reason='invalid model alias', next_action='use whitelist model alias', details={'allowedModels': ['codex5.2-main', 'codex5.2-backup', 'miaomiao', 'Kimi for Coding']})
    if scope not in {'current_session', 'channel_default', 'channel_active_bulk'}:
        return out(False, reason='invalid scope', next_action='scope must be current_session/channel_default/channel_active_bulk')
    if channel_id and not validate_channel_id(channel_id):
        return out(False, reason='invalid channel_id format', next_action='use discord snowflake id')
    if scope == 'current_session' and not session_key:
        return out(False, reason='missing session_key', next_action='pass session_key for current_session')
    if scope != 'current_session' and not channel_id:
        return out(False, reason='missing channel_id', next_action='pass channel_id')

    details = {
        'scope': scope,
        'channelId': channel_id or None,
        'sessionKey': session_key or None,
        'model': model,
        'validated': True,
    }
    return out(True, details=details, nextAction='call ops.model.switch.commit with same params')


def do_commit(params: Dict[str, Any]) -> Dict[str, Any]:
    scope = str(params.get('scope', 'current_session'))
    channel_id = str(params.get('channel_id', ''))
    session_key = str(params.get('session_key', ''))
    model = normalize_model(params.get('model'))

    if not model:
        return out(False, reason='invalid model alias', next_action='use whitelist model alias')

    if scope == 'current_session':
        if not session_key:
            return out(False, reason='missing session_key', next_action='pass session_key')
        r = apply_model_to_session(session_key, model)
        return out(
            r['ok'],
            partial=not r['ok'],
            reason=None if r['ok'] else 'session switch command failed',
            next_action='check stderr/stdout and session permissions',
            details=r,
            strategy=r.get('strategy', 'unknown'),
        )

    if scope == 'channel_default':
        if not validate_channel_id(channel_id):
            return out(False, reason='invalid channel_id format', next_action='use discord snowflake id')
        # 当前无官方“频道持久默认模型”入口：降级方案
        fallback_cmd = f'openclaw models set --agent main "{model}"'
        return out(
            False,
            partial=True,
            reason='no official persistent per-channel default model API found',
            next_action='use global default fallback or pin this model in channel runbook; optionally apply per active session with bulk flow',
            details={
                'scope': scope,
                'channelId': channel_id,
                'requestedModel': model,
                'fallbackGlobalDefaultCommand': fallback_cmd,
                'recommended': 'run ops.model.switch.bulk.prepare + bulk.commit for active sessions in this channel',
            },
        )

    if scope == 'channel_active_bulk':
        if not validate_channel_id(channel_id):
            return out(False, reason='invalid channel_id format', next_action='use discord snowflake id')
        sids = list_active_sessions_by_channel(channel_id, minutes=int(params.get('minutes', 1440)), limit=int(params.get('limit', 200)))
        if not sids:
            return out(False, partial=True, reason='no active sessions found in channel window', next_action='increase minutes window or wait for activity', details={'channelId': channel_id})
        ok_list, fail_list = [], []
        for sid in sids:
            r = apply_model_to_session(sid, model)
            (ok_list if r['ok'] else fail_list).append(r)
        return out(
            len(fail_list) == 0,
            partial=len(fail_list) > 0,
            reason='some sessions failed to switch' if fail_list else None,
            next_action='retry failed sessions individually' if fail_list else None,
            details={
                'channelId': channel_id,
                'model': model,
                'total': len(sids),
                'success': len(ok_list),
                'failed': len(fail_list),
                'successList': [{'sessionKey': x['sessionKey']} for x in ok_list],
                'failedList': [{'sessionKey': x['sessionKey'], 'rc': x['rc'], 'stderr': x['stderr'][:200]} for x in fail_list],
            },
        )

    return out(False, reason='invalid scope', next_action='use supported scope')


def do_bulk_prepare(params: Dict[str, Any]) -> Dict[str, Any]:
    operator = str(params.get('operator', ''))
    channel_id = str(params.get('channel_id', ''))
    model = normalize_model(params.get('model'))
    if not operator:
        return out(False, reason='missing operator', next_action='pass operator id')
    if not validate_channel_id(channel_id):
        return out(False, reason='invalid channel_id format', next_action='use discord snowflake id')
    if not model:
        return out(False, reason='invalid model alias', next_action='use whitelist model alias')

    sids = list_active_sessions_by_channel(channel_id, minutes=int(params.get('minutes', 1440)), limit=int(params.get('limit', 200)))
    slot = f'model_switch_bulk:{channel_id}'
    confirm_code = make_code(slot, operator, channel_id, model)
    expires = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=TTL_SECONDS)).isoformat().replace('+00:00', 'Z')

    st = load_state()
    st.setdefault('pending', {})[slot] = {
        'operator': operator,
        'channelId': channel_id,
        'model': model,
        'confirmCode': confirm_code,
        'expiresAt': expires,
    }
    save_state(st)

    return out(True, details={
        'slot': slot,
        'operator': operator,
        'channelId': channel_id,
        'model': model,
        'confirmCode': confirm_code,
        'ttlSeconds': TTL_SECONDS,
        'expiresAt': expires,
        'previewActiveSessionCount': len(sids),
        'previewSessionKeys': sids[:20],
    }, nextAction='call ops.model.switch.bulk.commit with operator/channel_id/model/confirm_code')


def do_bulk_commit(params: Dict[str, Any]) -> Dict[str, Any]:
    operator = str(params.get('operator', ''))
    channel_id = str(params.get('channel_id', ''))
    model = normalize_model(params.get('model'))
    confirm_code = str(params.get('confirm_code', ''))
    if not operator or not confirm_code:
        return out(False, reason='missing operator or confirm_code', next_action='pass both fields')
    if not validate_channel_id(channel_id):
        return out(False, reason='invalid channel_id format', next_action='use discord snowflake id')
    if not model:
        return out(False, reason='invalid model alias', next_action='use whitelist model alias')

    slot = f'model_switch_bulk:{channel_id}'
    st = load_state()
    rec = st.get('pending', {}).get(slot)
    if not rec:
        return out(False, reason='no pending bulk confirmation', next_action='run bulk.prepare first')

    now = dt.datetime.now(dt.timezone.utc)
    exp = dt.datetime.fromisoformat(rec['expiresAt'].replace('Z', '+00:00'))
    if now > exp:
        return out(False, reason='bulk confirmation expired', next_action='run bulk.prepare again')
    if rec.get('operator') != operator:
        return out(False, reason='operator mismatch', next_action='same operator must commit')
    if rec.get('model') != model or rec.get('channelId') != channel_id:
        return out(False, reason='model/channel mismatch with prepared record', next_action='use exactly prepared params')
    if rec.get('confirmCode') != confirm_code:
        return out(False, reason='confirm_code mismatch', next_action='use generated confirmCode from bulk.prepare')

    sids = list_active_sessions_by_channel(channel_id, minutes=int(params.get('minutes', 1440)), limit=int(params.get('limit', 200)))
    ok_list, fail_list = [], []
    for sid in sids:
        r = apply_model_to_session(sid, model)
        (ok_list if r['ok'] else fail_list).append(r)

    st.get('pending', {}).pop(slot, None)
    save_state(st)

    return out(
        len(fail_list) == 0,
        partial=len(fail_list) > 0,
        reason='some sessions failed to switch' if fail_list else None,
        next_action='retry failed sessions individually' if fail_list else None,
        details={
            'channelId': channel_id,
            'model': model,
            'total': len(sids),
            'success': len(ok_list),
            'failed': len(fail_list),
            'successList': [{'sessionKey': x['sessionKey']} for x in ok_list],
            'failedList': [{'sessionKey': x['sessionKey'], 'rc': x['rc'], 'stderr': x['stderr'][:200]} for x in fail_list],
        },
    )


def main() -> int:
    ap = argparse.ArgumentParser(description='Ops model switch dispatcher helper')
    ap.add_argument('--action', required=True)
    ap.add_argument('--params', default='{}')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    try:
        params = json.loads(args.params)
        if not isinstance(params, dict):
            raise ValueError('params must be object')
    except Exception as e:
        res = out(False, reason=f'invalid params json: {e}', next_action='fix --params JSON object')
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 1

    action = args.action.strip()
    if action == 'ops.model.switch.channel.preview':
        res = do_channel_preview(params)
    elif action == 'ops.model.switch.prepare':
        res = do_prepare(params)
    elif action == 'ops.model.switch.commit':
        res = do_commit(params)
    elif action == 'ops.model.switch.bulk.prepare':
        res = do_bulk_prepare(params)
    elif action == 'ops.model.switch.bulk.commit':
        res = do_bulk_commit(params)
    else:
        res = out(False, reason=f'unknown action: {action}', next_action='use ops.model.switch.* action keys')

    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res.get('ok') else 1


if __name__ == '__main__':
    raise SystemExit(main())
