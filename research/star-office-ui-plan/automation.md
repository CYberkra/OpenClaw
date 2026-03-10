# Star-Office 状态自动化最小架构（草案）

## 目标
通过轻量脚本把 Agent 执行状态同步到 Star-Office UI，保证“工作中/空闲”状态可见。

## 架构

- **状态上报层**：`scripts/star-office-state.sh`
  - 输入：`state` + `message`
  - 处理：状态白名单映射（coding/debugging/reviewing/idle，其他降级 reviewing）
  - 输出：`POST /set_state`，JSON `{state, text}`

- **自动检测层**：`scripts/star-office-watch-subagents.sh`
  - 每 30 秒执行 `openclaw sessions list --kinds spawn --limit 50`（或等价命令）
  - 计算活跃子代理数 `N`
  - `N > 0` → `reviewing + "subagents active: N"`
  - `N = 0` → `idle + "no active subagents"`

- **流程钩子层**：`scripts/star-office-hooks.md`
  - 在复杂任务开始前、回复前、派发 subagent 后接入调用

## 注意事项

1. **幂等与低噪音**
   - 重复上报同一状态通常可接受；若后续有噪音可加“状态未变化则跳过”缓存。
2. **错误处理**
   - `state.sh` 在 HTTP 非 2xx 时返回非 0，便于调用方感知失败。
3. **依赖最小化**
   - 仅依赖 `bash + curl + python3`。
4. **兼容性**
   - `openclaw` 命令不可用时给出降级提示，避免脚本死循环误报。
5. **安全边界**
   - 仅使用本地 `STAR_OFFICE_BASE_URL`（默认 `http://127.0.0.1:19000`），不修改生产配置。

## 一键启用建议

```bash
chmod +x scripts/star-office-state.sh scripts/star-office-watch-subagents.sh
scripts/star-office-watch-subagents.sh --once
```
