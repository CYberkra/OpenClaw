# ops_panel_v2 handlers（Discord Components v2 自我迭代版）

## 1) 统一交互路由规范（稳定 action key）

> 不再仅依赖按钮文案，主路由统一收敛到 `actionKey -> panel_dispatcher action`。

| UI actionKey | dispatcher action | 说明 |
|---|---|---|
| `ops.quota.all` | `quota.all` | 全部模型额度 |
| `ops.codex.history` | `codex.sessions.history` | Codex 历史会话 |
| `ops.codex.refresh` | `codex.sessions.refresh` | 刷新 Codex 缓存 |
| `ops.usage.channel_model` | `usage.channel_model` | 频道/帖子模型聚合 |
| `ops.health.snapshot` | `health.snapshot` | 本机健康快照 |
| `ops.quota.provider` + `quota_openai/...` | `quota.provider` | 平台单项额度 |
| `ops.sessions.active.channel` | `sessions.active` | 按频道活跃会话 |
| `ops.danger.restart.request` | `danger.restart.request` | 危险动作：重启申请 |
| `ops.danger.restart.confirm` | `danger.restart.confirm` | 危险动作：重启确认 |
| `ops.danger.channel_delete.request` | `danger.channel_delete.request` | 危险动作：删频道申请 |
| `ops.danger.channel_delete.confirm` | `danger.channel_delete.confirm` | 危险动作：删频道确认 |
| `ops.model.switch.channel.preview` | `ops.model.switch.channel.preview` | 选频道即回显当前模型 |
| `ops.model.switch.prepare` | `ops.model.switch.prepare` | 模型切换参数预检 |
| `ops.model.switch.commit` | `ops.model.switch.commit` | 模型切换执行 |
| `ops.model.switch.bulk.prepare` | `ops.model.switch.bulk.prepare` | 批量模型切换准备（双确认） |
| `ops.model.switch.bulk.commit` | `ops.model.switch.bulk.commit` | 批量模型切换提交（双确认） |

---

## 2) 最小编排入口（统一 JSON）

文件：`scripts/ops/panel_dispatcher.py`

- 输入：`--action <action_key>` + `--params '{...}'`
- 输出统一结构：

```json
{
  "ok": true,
  "partial": false,
  "generatedAt": "..."
}
```

受限/失败统一结构：

```json
{
  "ok": false,
  "partial": true,
  "reason": "...",
  "nextAction": "..."
}
```

---

## 3) 真实执行覆盖（新增脚本）

### A. `scripts/ops/codex_sessions.py`
- `--history`: 解析 `openclaw status` 会话表
- `--refresh`: 刷新并落盘缓存到 `~/.openclaw/workspace/.cache/codex_sessions_cache.json`

### B. `scripts/ops/channel_model_usage.py`
- 从 JSONL 聚合 `channelId/threadId` 维度的模型使用
- 优先读字段 `model`，否则从 `content` 里正则提取模型名

### C. `scripts/ops/active_sessions.py`
- 从 JSONL 按 `channelId + sessionId + ts` 聚合窗口内活跃会话

### D. `scripts/ops/health_snapshot.py`
- 本机 CPU load / 内存 / 磁盘 / 网络 / `openclaw gateway status`

---

## 4) 危险操作强化（双确认）

已在 dispatcher 实现以下强约束（状态文件：`.cache/ops_panel_confirm_state.json`）：

1. **操作者绑定**：`operatorId` 必须与 request 阶段一致
2. **5 分钟 TTL**：超时必须重新发起 request
3. **confirm_code**：随机码 `RESTART-xxxx` / `DELETE-xxxx`
4. **删频道 ID 一致性校验**：
   - request 的 `targetChannelId`
   - confirm 的 `targetChannelId`
   - modal `channelIdAgain`
   三者必须一致，否则拒绝

> 备注：dispatcher 只做本地预检；真正 Discord 删除动作由主 handler 调 `message.channel-delete` 执行。

---

## 5) 模型切换流程（v2.1 新增）

### 5.0 选频道即回显当前模型（preview）

1. 当 `ops.model.switch.channel` 下拉选择频道后，主 handler 调 `ops.model.switch.channel.preview`。
2. 入参：`channel_id`（Discord snowflake）。
3. 行为：从 `openclaw sessions --json` 中按 `agent:main:discord:channel:<channel_id>` 查找会话并回显。
4. 返回：`channel_id`、`session_key`、`current_model`、`updated_at`。
5. 若不存在会话：返回 `partial=true` + `reason` + `nextAction`（提示先在该频道发一条消息再重试）。

### 5.1 普通模型切换（prepare -> commit）

1. `ops.model.switch.prepare` 预检参数：
   - `model` 必须在白名单（`codex5.2-main/codex5.2-backup/miaomiao/Kimi for Coding`）
   - `channel_id` 必须是 Discord snowflake（17-22 位数字）
   - `scope` 必须在 `current_session/channel_default/channel_active_bulk`
2. `ops.model.switch.commit` 执行：
   - `current_session`：优先走 `sessions_send` 等价链路（`sessions_list` 解析 key→sessionId，再向目标会话发送 `/model <alias>`）；失败后回退原有 `--session-id <session_key>` 方式
   - `channel_default`：若无官方“频道持久默认模型”入口，返回 `partial=true` + `reason` + `nextAction`
   - `channel_active_bulk`：自动枚举频道活跃会话并逐个切换，输出成功/失败列表

### 5.2 批量模型切换（双确认）

1. `ops.model.switch.bulk.prepare`：要求 `operator/channel_id/model`，生成 `confirm_code`，绑定操作者并设置 5 分钟 TTL。
2. `ops.model.switch.bulk.commit`：必须提供完全匹配的 `operator/channel_id/model/confirm_code` 才会执行。
3. 输出统一 JSON：`ok/partial/reason/nextAction/details`。

---

## 6) v2 -> v2.1 迁移说明（5 步）

1. 面板文件从 `ops_panel_v2_components.json` 升级到 `ops_panel_v2_1_components.json`。
2. 主路由增加 4 个稳定 action key：
   `ops.model.switch.prepare/commit/bulk.prepare/bulk.commit`。
3. dispatcher 接入 `scripts/ops/model_switch.py`，模型切换统一由该脚本处理。
4. 对批量切换启用二次确认（操作者绑定 + 5 分钟 TTL + confirm_code）。
5. 主 handler 回帖按统一 JSON 字段读取：`ok/partial/reason/nextAction/details`。

---

## 7) 示例命令（可直接运行）

```bash
# 1) channel.preview（选频道即回显）
python3 scripts/ops/panel_dispatcher.py --action ops.model.switch.channel.preview --params '{"channel_id":"1480620479722295316"}'

# 2) prepare（普通切换预检）
python3 scripts/ops/panel_dispatcher.py --action ops.model.switch.prepare --params '{"scope":"current_session","session_key":"agent:main:discord:channel:1480620479722295316","channel_id":"1480620479722295316","model":"codex5.2-main"}'

# 3) commit（current_session 真执行）
python3 scripts/ops/panel_dispatcher.py --action ops.model.switch.commit --params '{"scope":"current_session","session_key":"agent:main:discord:channel:1480620479722295316","channel_id":"1480620479722295316","model":"codex5.2-backup"}'

# 4) bulk.prepare（二次确认）
python3 scripts/ops/panel_dispatcher.py --action ops.model.switch.bulk.prepare --params '{"operator":"u_ops_1","channel_id":"1480620479722295316","model":"miaomiao","minutes":1440}'

# 5) bulk.commit（二次确认提交）
python3 scripts/ops/panel_dispatcher.py --action ops.model.switch.bulk.commit --params '{"operator":"u_ops_1","channel_id":"1480620479722295316","model":"miaomiao","confirm_code":"REPLACE_CODE","minutes":1440}'
```
