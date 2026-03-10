# Ops Panel Final Release Notes

## 版本定位
- 基于 `v2.1` 的整理优化版。
- 目标：**不推倒重来**，在保持能力与 action key 稳定的前提下提升可读性、闭环性与容错提示。

## 关键改动（Final）
1. UI 分区重排为：查询区 / 会话区 / 模型切换区 / 危险操作区。
2. 保留 v2.1 action key，补充 `ops.model.switch.channel.preview` 的显式入口按钮与说明。
3. 会话区文案加入时间窗口建议：`24h=1440`、`7d=10080`。
4. 模型切换流程文案改为 1-2-3 步（选频道→选模型→选作用域）降低歧义。
5. 强化 `current_session` 路径执行说明（key->sessionId 优先，legacy 回退）。
6. 危险操作区统一高风险提示，明确双确认三要素：`operator + TTL + confirm_code`。
7. `panel_dispatcher.py` 增加统一错误模板输出：`errorCode + userMessage`。
8. handlers 文档补全成功/失败示例与接入注意点，便于主 handler 最小改造。

## 实跑验证（3 条）

### 1) 频道模型回显
命令：
```bash
python3 scripts/ops/panel_dispatcher.py --action ops.model.switch.channel.preview --params '{"channel_id":"1480620479722295316"}'
```
摘要：
```json
{"ok":true,"details":{"channel_id":"1480620479722295316","session_key":"agent:main:discord:channel:1480620479722295316","current_model":"gpt-5.3-codex"}}
```

### 2) 活跃会话查询（24h）
命令：
```bash
python3 scripts/ops/panel_dispatcher.py --action sessions.active --params '{"channel":"1480620479722295316","minutes":1440,"limit":1000}'
```
摘要：
```json
{"ok":true,"windowMinutes":1440,"channels":[{"channelId":"1480620479722295316","activeSessionCount":2}]}
```

### 3) 模型切换预检（current_session）
命令：
```bash
python3 scripts/ops/panel_dispatcher.py --action ops.model.switch.prepare --params '{"scope":"current_session","session_key":"agent:main:discord:channel:1480620479722295316","channel_id":"1480620479722295316","model":"codex5.2-main"}'
```
摘要：
```json
{"ok":true,"details":{"scope":"current_session","validated":true,"model":"codex5.2-main"}}
```

## 从 v2.1 切换到 final（最小步骤，5步）
1. 备份旧文件：`ops_panel_v2_1_components.json`、`ops_panel_v2_handlers.md`。
2. 发送面板时改用 `ops_panel_final_components.json`。
3. 主 handler 路由保持不变，仅补：
   - `ops.model.switch.channel` 选择后自动触发 `ops.model.switch.channel.preview`
   - 会话查询默认 `minutes=1440`（支持 10080）
4. 使用更新后的 `scripts/ops/panel_dispatcher.py`（含统一错误模板字段）。
5. 灰度观察 24h 后再全量替换旧文档引用。

## 建议先灰度的发布策略
- **阶段 1（10%-20%频道）**：仅开启查询区 + 会话区 + preview，不开放危险操作按钮给全部运维成员。
- **阶段 2（核心运维频道）**：开放模型切换（含 bulk.prepare/bulk.commit），记录失败原因 TopN。
- **阶段 3（全量）**：在确认 `errorCode/userMessage` 可被主 handler稳定消费后开放到所有目标频道。
- 回滚条件：
  - 连续出现 `PERMISSION_DENIED` 或 `NO_SESSION_OR_CONFIRMATION` 异常峰值
  - bulk 提交失败率 > 20%
  - 危险操作确认链路异常（prepare/commit 对不上）

## 已知限制
1. `channel_default` 仍缺官方“每频道持久默认模型”API，仅能给出 fallback 引导。
2. `channel_active_bulk` 依赖本地会话文件活跃度，极低活跃频道可能返回空结果。
3. 危险操作中的删频道动作 dispatcher 仅做预检，真正删除仍由主流程调用 `message.channel-delete`。
