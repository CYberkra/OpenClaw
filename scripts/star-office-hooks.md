# Star-Office 状态同步 Hooks（事件驱动优先）

## 策略：事件驱动优先，轮询兜底

- **优先**：在关键动作发生时立刻上报（任务开始/结束、子任务派发/完成）。
- **兜底**：保留轮询脚本用于补偿漏报或异常场景，不再作为唯一来源。

## 输入状态 -> Star-Office 状态映射

- `coding` -> `executing`
- `debugging` -> `researching`
- `reviewing` -> `writing`
- `idle` -> `idle`

> 兼容说明：`scripts/star-office-state.sh` 仍接受旧输入（`coding/debugging/reviewing/idle`），并在内部转换为 Star-Office 推荐状态。发送 `/set_state` 时会同时带上 `text` 与 `detail` 字段（双字段兼容）。

## 接入点

1. **开始复杂任务前**
   - `scripts/star-office-event.sh task_start "..."`（上报 `reviewing`）
2. **准备回复用户前/任务完成后**
   - `scripts/star-office-event.sh task_done "..."`（上报 `idle`）
3. **派发 subagent 时**
   - `scripts/star-office-event.sh subagent_spawn "..."`（上报 `reviewing`）

## 可复制示例（3条）

```bash
scripts/star-office-event.sh task_start "implementing feature X"
scripts/star-office-event.sh task_done "ready to reply"
scripts/star-office-event.sh subagent_spawn "label-a: investigate flaky test"
```

## 轮询兜底（可选）

```bash
# 每30秒轮询一次 subagents，并自动同步 reviewing/idle
scripts/star-office-watch-subagents.sh
```
