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

## 5) brief1 -> v2 迁移步骤（6 步）

1. 将面板投递文件切换为 `ops_panel_v2_components.json`。
2. 主进程路由由“文案匹配”改为“优先 actionKey，文案仅兜底”。
3. 接入 `scripts/ops/panel_dispatcher.py`，所有按钮/下拉统一走 dispatcher。
4. 危险动作改造为 request/confirm 两阶段，必须带 `operatorId/channelId`。
5. 删除频道动作接入 `targetChannelId + channelIdAgain` 一致性校验。
6. 回帖统一读取 dispatcher JSON：`ok/partial/reason/nextAction`，形成闭环反馈。

---

## 6) 示例命令（可直接运行）

```bash
python3 scripts/ops/panel_dispatcher.py --action quota.all --params '{}'
python3 scripts/ops/panel_dispatcher.py --action codex.sessions.history --params '{"limit":10}'
python3 scripts/ops/panel_dispatcher.py --action health.snapshot --params '{}'
python3 scripts/ops/panel_dispatcher.py --action danger.restart.request --params '{"operatorId":"u1","channelId":"c1"}'
```
