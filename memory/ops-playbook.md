# Ops Playbook (Token-Saver)

## GPR GUI 快速路径
- Repo: `/mnt/e/Openclaw/.openclaw/workspace/repos/GPR_GUI`
- 示例数据（默认）: `测线main_40dbm_普通飞高.csv`
- GUI 启动: `python3 app_qt.py`
- EXE 输出: `repos/GPR_GUI/dist/`

## 子分区常用线程
- GUI性能优化: `1480502191717613681`
- self-improve评估: `1480620479722295316`
- AI可视化调研: `1480888694847176817`

## 默认执行策略
- 群聊：只注入任务相关最小记忆，不加载全量长期记忆。
- 复杂任务：优先子代理。
- 汇报格式：结论 + 证据路径 + 下一步。
- 每次回复附 token（in/out）。

## Heartbeat 关键点
- 周期：每2小时
- 频道：`1479758987728650445`
- 必含：gateway状态/端口、磁盘摘要、active subagents、queue摘要、queued tasks、last commit hash
