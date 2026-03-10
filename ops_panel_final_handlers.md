# ops_panel_final handlers（在 v2.1 基础上整理优化，不推倒重来）

## 1) 稳定 action key 映射（兼容 v2.1）

> 原有能力保留，主路由继续由 `actionKey -> panel_dispatcher action` 承接。

| UI actionKey | dispatcher action | 说明 |
|---|---|---|
| `ops.quota.all` | `quota.all` | 全部模型额度 |
| `ops.quota.provider` | `quota.provider` | 平台单项额度（OpenAI/Anthropic/Google/Groq/DeepSeek） |
| `ops.codex.history` | `codex.sessions.history` | Codex 历史会话 |
| `ops.codex.refresh` | `codex.sessions.refresh` | 刷新 Codex 缓存 |
| `ops.usage.channel_model` | `usage.channel_models` | 频道/帖子模型聚合（UI key 兼容旧版命名） |
| `ops.sessions.active.channel` | `sessions.active` | 按频道查询活跃会话 |
| `ops.health.snapshot` | `health.snapshot` | 本机健康快照 |
| `ops.model.switch.channel.preview` | `ops.model.switch.channel.preview` | 选频道后回显当前模型 |
| `ops.model.switch.prepare` | `ops.model.switch.prepare` | 模型切换参数预检 |
| `ops.model.switch.commit` | `ops.model.switch.commit` | 模型切换执行 |
| `ops.model.switch.bulk.prepare` | `ops.model.switch.bulk.prepare` | 批量切换准备（双确认） |
| `ops.model.switch.bulk.commit` | `ops.model.switch.bulk.commit` | 批量切换确认（双确认） |
| `ops.danger.restart.request` | `danger.gateway_restart.prepare` | 危险操作：重启网关申请 |
| `ops.danger.restart.confirm` | `danger.gateway_restart.commit` | 危险操作：重启网关确认 |
| `ops.danger.channel_delete.request` | `danger.channel_delete.prepare` | 危险操作：删频道申请 |
| `ops.danger.channel_delete.confirm` | `danger.channel_delete.commit` | 危险操作：删频道确认 |

---

## 2) 分区后的交互流程（Final）

### 2.1 查询区
- 纯查询，不改配置。
- `ops.quota.provider` 建议主 handler 将选项值映射成 `provider=openai/anthropic/google/groq/deepseek` 传给 dispatcher。

### 2.2 会话区
- `ops.sessions.active.channel` 建议默认 `minutes=1440`（24h），高噪声/低活跃场景支持 `minutes=10080`（7d）。
- 推荐回帖展示：`channelId + activeCount + top session keys`。

### 2.3 模型切换区
- **闭环 1：频道选择后回显当前模型**
  - 触发：`ops.model.switch.channel.preview`
  - 输出：`channel_id / session_key / current_model / updated_at`
- **闭环 2：current_session 路径可执行**
  - `commit(scope=current_session)` 内部优先使用：
    1) sessions_list 解析 `key -> UUID sessionId`
    2) `openclaw agent --session-id <uuid> --message "/model <alias>"`
    3) 失败再回退 legacy `--session-id <session_key>`
- `channel_default` 暂无官方每频道持久默认模型入口，保持 `partial=true + nextAction` 引导。

### 2.4 危险操作区
- 保留双确认：`operator + TTL(300s) + confirm_code`。
- 删除频道仍执行三重一致性校验：`targetChannelId == confirm channel_id == channel_id_again`。

---

## 3) 统一错误文案模板（已落地到 panel_dispatcher）

当 `ok=false` 时，dispatcher 自动补充：
- `errorCode`
- `userMessage`

错误分类：
- `PARAM_MISSING_OR_INVALID`
- `NO_SESSION_OR_CONFIRMATION`
- `PERMISSION_DENIED`
- `OPERATION_FAILED`

建议主 handler 直接回帖 `userMessage`，并附 `nextAction` 作为操作提示。

---

## 4) 关键 action 示例命令（>=6，含成功/失败）

> 以下均在 `/home/baiiy1/.openclaw/workspace` 下执行。

### A. 成功样例

```bash
# 1) 选频道后回显当前模型（成功）
python3 scripts/ops/panel_dispatcher.py --action ops.model.switch.channel.preview --params '{"channel_id":"1480620479722295316"}'

# 2) 活跃会话查询（成功，24h）
python3 scripts/ops/panel_dispatcher.py --action sessions.active --params '{"channel":"1480620479722295316","minutes":1440,"limit":1000}'

# 3) 模型切换预检（成功）
python3 scripts/ops/panel_dispatcher.py --action ops.model.switch.prepare --params '{"scope":"current_session","session_key":"agent:main:discord:channel:1480620479722295316","channel_id":"1480620479722295316","model":"codex5.2-main"}'
```

### B. 失败样例

```bash
# 4) 模型切换预检失败：缺 session_key
python3 scripts/ops/panel_dispatcher.py --action ops.model.switch.prepare --params '{"scope":"current_session","channel_id":"1480620479722295316","model":"codex5.2-main"}'

# 5) 批量确认失败：缺 prepare 记录
python3 scripts/ops/panel_dispatcher.py --action ops.model.switch.bulk.commit --params '{"operator":"u_ops_1","channel_id":"1480620479722295316","model":"miaomiao","confirm_code":"BADCODE"}'

# 6) 危险操作确认失败：operator 不一致（先 prepare 后换人 commit）
python3 scripts/ops/panel_dispatcher.py --action danger.gateway_restart.commit --params '{"operator":"other_user","confirm_code":"XXXX"}'
```

---

## 5) 实跑结果摘要（3 条）

> 以本次环境实跑为准，完整输出可在终端复现。

1. `ops.model.switch.channel.preview`（channel 1480620479722295316）
```json
{"ok": true, "partial": false, "details": {"channel_id": "1480620479722295316", "session_key": "agent:main:discord:channel:1480620479722295316", "current_model": "gpt-5.3-codex"}}
```

2. `sessions.active`（24h）
```json
{"ok": true, "partial": false, "windowMinutes": 1440, "channels": [{"channelId": "1480620479722295316", "activeSessionCount": 2}]}
```

3. `ops.model.switch.prepare`（current_session）
```json
{"ok": true, "partial": false, "details": {"scope": "current_session", "validated": true, "model": "codex5.2-main"}}
```

---

## 6) 主 handler 接入注意点（最小变更）

1. 继续沿用 v2.1 actionKey；无需重写 UI 事件总线。
2. `ops.model.switch.channel` 选择后，立即触发 `ops.model.switch.channel.preview` 回显。
3. 会话查询默认 minutes=1440，并在 UI 提示支持 10080。
4. 对 `ok=false` 的结果，优先回帖 `userMessage`，其次 `nextAction`。
5. 危险操作 request/confirm 参数必须透传 `operator` 与 `confirm_code`。
