# ops_panel_brief1 handlers（Discord Components v2）

> 目标：定义“收到交互后主进程如何执行并回帖”。
> 约定：所有回帖都用 `message` 工具（`channel: discord`）；数据采集优先用 `exec/read/nodes`。

## 0) 主流程（统一）

1. 收到组件交互事件（按钮 / 下拉 / modal 提交）。
2. 根据按钮文案或 select value 路由到 handler。
3. 调用对应 OpenClaw 工具执行业务命令。
4. 将输出整理成简短中文结果（成功/失败 + 关键数据 + 时间戳）。
5. 用 `message.send` 回复到同频道；必要时 `message.thread-reply` 回到原线程。
6. 对失败场景返回：错误摘要 + 建议重试动作。

---

## 1) 一键查看全部模型额度（按钮：`全部模型额度`）

- 工具映射：`exec` → `message.send`
- 执行命令：
  - `exec`: `python3 scripts/ops/model_quota.py --all --json`
- 输出字段（JSON）：
  - 顶层：`ok`, `generatedAt`, `runtime`, `providers`
  - `runtime`：来自 `openclaw status` 解析，含 `available`, `reason`, `sessions[]`, `activeSession`, `maxObservedLimit`
  - `providers[]`：`name`, `available`, `reason`, `usage`, `resetAt`, `detectedConfig`, `configSource`
- 回帖建议：
  - 优先展示 `runtime.activeSession.used/limit/remaining`
  - 平台项展示 `available` 与 `reason`（当前脚本不直连账单 API）

## 2) 查看 Codex 历史会话（按钮：`Codex历史会话`）

- 工具映射：`exec/read` → `message.send`
- 推荐执行（示例）：
  - `exec`: `python3 scripts/ops/codex_sessions.py --history --limit 20 --json`
  - 或 `read` 读取本地历史缓存文件（若已有固定路径）。
- 回帖内容：最近会话列表（时间、会话ID、状态）。

## 3) 刷新 Codex 会话缓存（按钮：`刷新Codex缓存`）

- 工具映射：`exec` → `message.send`
- 推荐执行：
  - `exec`: `python3 scripts/ops/codex_sessions.py --refresh`
- 回帖内容：`已刷新` + 刷新条目数 + 耗时。

## 4) 查看各频道/帖子所用模型（按钮：`频道/帖子模型`）

- 工具映射：`message.search/read` + `exec` → `message.send`
- 推荐执行：
  - `message.search` 在目标 guild/channel 范围按关键词抽样（如模型标识）。
  - `exec`: `python3 scripts/ops/channel_model_usage.py --guild <id> --json`
- 回帖内容：按频道/帖子聚合的模型使用分布。

## 5) 查看本机健康状态（按钮：`本机健康状态`）

- 工具映射：`nodes.device_health`（优先）或 `exec`（兜底）→ `message.send`
- 推荐执行：
  - `nodes` action: `device_health`（若有配对 node）
  - 兜底 `exec`: `python3 scripts/ops/health_snapshot.py --json`
- 回帖内容：CPU / 内存 / 磁盘 / 网络 / 关键进程状态。

## 6) 按平台查看单项额度（select value: `quota_*`）

- 路由映射：
  - `quota_openai` / `quota_anthropic` / `quota_google` / `quota_groq` / `quota_deepseek`
- 工具映射：`exec` → `message.send`
- 执行命令：
  - `exec`: `python3 scripts/ops/model_quota.py --provider <provider> --json`
- 输出字段（JSON）：
  - 顶层与 `--all` 一致；`providers` 仅返回单一平台对象
  - 平台对象：
    - `available=false` 且 `reason` 说明为何无法直接给到账单额度
    - `usage=null`, `resetAt=null`（若未来接入账单 API 再填充）
    - `detectedConfig/configSource` 标注配置探测来源（env/config）
- 回帖内容：
  - 展示该平台 `available/reason`
  - 同时附上 `runtime.activeSession` 作为实时可用运行额度参考

## 7) 按频道查看活跃会话（channel select）

- 输入：用户在 `channel` 类型 select 里选中的 `channel_id`
- 工具映射：`exec` +（可选）`message.read` → `message.send`
- 推荐执行：
  - `exec`: `python3 scripts/ops/active_sessions.py --channel <channel_id> --json`
- 回帖内容：活跃会话数、最近活跃时间、Top 会话ID。

---

## 8) 重启 OpenClaw 网关（危险，双重确认）

### Step A（首确认）

- 触发：按钮 `重启网关`
- 工具映射：`message.send`
- 动作：发送 `confirm_restart_step1` 载荷（含 `确认重启（步骤2）` + modal）。

### Step B（二次确认 + 确认码）

- 触发：modal 提交
- 校验：`confirm_code == RESTART`
- 不通过：`message.send` 回复“确认码错误，已取消”。
- 通过后执行：
  - `exec`: `openclaw gateway restart`
  - `exec`: `openclaw gateway status`
- 回帖：
  - 成功：`网关已重启，当前状态：...`
  - 失败：`重启失败，错误：...`

> 安全要求：必须 Step A + Step B 都通过，且确认码匹配，才允许执行。

---

## 9) Discord 频道预览/删除（危险，双重确认）

### Step A（首确认 + 选频道）

- 触发：按钮 `频道预览/删除`
- 工具映射：`message.send`
- 动作：发送 `confirm_delete_channel_step1` 载荷（先选频道，可预览，可进入删除步骤2）。

### 预览流程（非删除）

- 触发：按钮 `预览频道`
- 工具映射：`message.channel-info` + `message.read` → `message.send`
- 推荐执行：
  - `message.channel-info`（拿频道类型/ID/父级/权限概览）
  - `message.read`（最近 N 条，供操作者核对）
- 回帖：频道元信息 + 最近消息摘要。

### Step B（二次确认删除）

- 触发：按钮 `确认删除（步骤2）` 的 modal 提交
- 校验：
  1. `confirm_code == DELETE`
  2. `channel_id_again` 与 Step A 选中的频道ID一致
- 任一不通过：`message.send` 回复“校验失败，已取消删除”。
- 通过后执行：
  - `message.channel-delete`（`channel: discord`, `channelId: <target>`, `reason: ...`）
- 回帖：
  - 成功：`频道 <id> 已删除`
  - 失败：`删除失败：...`

> 安全要求：必须“先预览可选 + 二次确认码 + 再次输入频道ID一致”三层防护。

---

## 建议的回帖格式（统一）

- 标题：`✅ 操作完成` / `❌ 操作失败`
- 内容：
  - 操作名
  - 关键结果（最多 5 行）
  - 执行时间（本地时区）
  - 如失败：下一步建议（重试/检查脚本/检查权限）

## 最小实现建议（主进程）

1. 将 `ops_panel_brief1_components.json` 的 `panel_send_payload` 直接投递。
2. 维护一张路由表：`交互标识 -> handler`。
3. 对危险操作维护短时上下文（操作者ID、目标频道ID、发起时间，TTL 5 分钟）。
4. 所有 handler 最终都回帖，避免“执行了但无反馈”。
