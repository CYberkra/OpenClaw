# Star-Office 状态同步 Hooks（最小接入）

## 接入点

1. **开始复杂任务前**
   - 根据阶段调用：`coding` / `debugging` / `reviewing`
2. **准备回复用户前**
   - 调用 `idle`，表示当前已完成处理、待机
3. **派发 subagent 后（可选）**
   - 调用 `reviewing`，并附带说明（如有活跃子代理数量）

## 可复制示例（3条）

```bash
scripts/star-office-state.sh coding "implementing feature X"
scripts/star-office-state.sh idle "ready to reply"
scripts/star-office-watch-subagents.sh --once
```

## 持续监控（可选）

```bash
# 每30秒轮询一次 subagents，并自动同步 reviewing/idle
scripts/star-office-watch-subagents.sh
```
