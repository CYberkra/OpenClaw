# Star-Office 事件驱动状态同步 Runbook

## 为什么纯轮询会漏检

纯轮询（例如每 30 秒检查一次）有天然盲区：

1. **短任务被吞掉**
   - 任务在两次轮询之间开始并结束，轮询永远看不到中间状态。
2. **状态切换延迟**
   - 用户已经开始处理任务，但看板还停留在 idle，造成“假空闲”。
3. **异常时段放大误差**
   - CLI 抖动、网络偶发失败、单次轮询报错都会把误差持续到下一轮。

结论：轮询适合作为兜底，不应作为唯一状态源。

## 推荐操作流（事件驱动优先）

1. **任务开始前**
   - `scripts/star-office-event.sh task_start "<任务说明>"`
2. **需要派发子任务时**
   - `scripts/spawn-with-star-office.sh "<任务描述>" "<label>" [command ...]`
   - 如果不带 command（降级模式），会先上报 reviewing，并提示你任务完成后手动上报。
3. **任务结束准备回复前**
   - `scripts/star-office-event.sh task_done "<收尾说明>"`
4. **轮询兜底（可选）**
   - 后台可继续跑 `scripts/star-office-watch-subagents.sh`，用于防止遗漏。

## 故障排查

### 1) 报错“缺少可执行脚本”
- 检查脚本权限：
  - `chmod +x scripts/star-office-state.sh scripts/star-office-event.sh scripts/spawn-with-star-office.sh`

### 2) 上报失败 / 连接不上后端
- 默认地址：`http://127.0.0.1:19000/set_state`
- 先确认后端是否启动，再测试：
  - `scripts/star-office-state.sh reviewing "health check"`
- 如后端地址不同，设置环境变量：
  - `export STAR_OFFICE_BASE_URL="http://<host>:<port>"`

### 3) 派发命令无法可靠等待
- 使用降级模式（不带 command）：
  - 先上报开始，任务结束时手动执行：
  - `scripts/star-office-event.sh subagent_done "<label>: done"`
