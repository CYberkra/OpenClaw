# Star-Office-UI 适配评估报告（OpenClaw + 已完成状态上报链路）

- 评估对象：`ringhyacinth/Star-Office-UI`
- 本地仓库：`/home/baiiy1/.openclaw/workspace/research/star-office-ui`
- 评估时间：2026-03-10
- 结论等级：**部分适合**
- 匹配度评分：**78 / 100**

---

## 1) 结论摘要

Star-Office-UI 与我们“OpenClaw + 状态上报”场景总体方向高度一致，且已提供现成 API 与多 Agent 推送脚本，**可在不改生产敏感配置的前提下快速接入**。  
但当前我们本地 `star-office-event/watcher` 脚本与该项目后端接口存在**状态枚举与字段名不兼容**（`reviewing/coding/debugging` + `text`），会导致状态不生效或 UI 回退为默认逻辑。  
因此建议：**先做轻量映射层修复（1天内），再做多人链路稳态化（本周）**。

---

## 2) 依据与项目拆解

### 核心能力（从 README / 代码提取）

1. 像素办公室状态看板（6 状态）
   - `idle / writing / researching / executing / syncing / error`
   - 状态映射到区域：休息区 / 工作区 / Bug 区
2. 多 Agent 协作
   - `join-agent` + `agent-push` + `agents` 列表
   - 支持 join key、并发上限、过期策略、离线判定
3. OpenClaw 深度集成导向
   - README 直接给出 `set_state.py` 工作流
4. 辅助能力
   - yesterday memo（读取 `memory/*.md`）
   - 资产替换与布局管理（assets API）
   - 三语 UI（CN/EN/JP）

### 部署与依赖

- 后端：Flask（`backend/requirements.txt`: `flask==3.0.2`, `pillow==10.4.0`）
- 运行：Python 3.10+
- 默认端口：`19000`
- 首次初始化：`cp state.sample.json state.json`
- 可选：Cloudflare Tunnel 对外
- 可选：Tauri 桌面壳（实验性）

### 状态同步机制（关键）

1. 主 Agent（本地）
   - `POST /set_state` 或 `set_state.py` 写入 `state.json`
   - `GET /status` 供前端轮询
2. 多 Agent（远端）
   - `POST /join-agent` 获取/确认 agentId
   - `POST /agent-push` 每 15s 推送状态
   - `GET /agents` 拉取在线与离线
3. 兼容性策略（后端内置）
   - `normalize_agent_state` 支持 `working -> writing` 等同义映射
   - 但**不包含**`reviewing/coding/debugging`

### 可扩展点（资源替换 / 状态映射 / 多人同步）

1. 资源替换
   - `/assets/upload`、`/assets/list`、位置与默认值 API 已完整
   - 支持备份 `.bak` / 默认快照 `.default`
2. 状态映射
   - 后端 `normalize_agent_state` 可继续扩展别名
   - `STATE_TO_AREA_MAP` 统一控制区域映射
3. 多人同步
   - join key 并发限制、过期与离线判定已实现
   - 适合接入我们已完成的上报链路做可视层

---

## 3) 与我们现状匹配度评估

## 评分：78/100（部分适合）

### 加分项

- 与 OpenClaw 场景高度对齐（README 明确）
- API 结构清晰，可直接脚本化
- 多 Agent 状态推送机制现成，减少自研成本
- 近期持续维护（最近提交在 2026-03）

### 扣分项

- 我方现有脚本接口不兼容（见第 4 节）
- 许可证层面：代码 MIT，但项目声明美术资源“非商用”，商用需替换资产
- 前端状态体系固定 6 类，复杂工作流状态需做映射层

---

## 4) 与现有脚本（star-office-event/watcher）衔接分析

### 已发现的关键不兼容

当前本地脚本：
- `scripts/star-office-event.sh`
- `scripts/star-office-watch-subagents.sh`
- `scripts/star-office-state.sh`

问题点：

1. **状态值不兼容**
   - 当前脚本发：`coding/debugging/reviewing/idle`
   - Star-Office-UI 认可：`idle/writing/researching/executing/syncing/error`
   - 后果：`/set_state` 可能忽略无效状态（状态保持旧值）

2. **字段名不兼容**
   - 当前脚本 payload：`{"state":"...","text":"..."}`
   - 后端读取字段：`state` + `detail`
   - 后果：描述信息丢失

3. **watcher 语义偏弱**
   - `subagents active>0` 直接标记 `reviewing`
   - 无法表达 `executing/researching/syncing/error` 粒度

### 建议接入方式（最小改造优先）

- 保留现有 `star-office-event/watcher` 调用入口不变
- 仅修改 `scripts/star-office-state.sh`：
  1) 增加状态映射表（旧状态 -> 新状态）
  2) payload 字段改为 `detail`
  3) 保持目标 API 仍为 `/set_state`

推荐映射：
- `reviewing -> researching`
- `coding -> writing`
- `debugging -> error`
- `idle -> idle`

进阶（本周）：
- `watch-subagents` 根据上下文细化为 `executing/syncing/researching`
- 子代理完成事件触发 `syncing -> idle` 两段式状态

---

## 5) 立即可复用（今天可做）

1. 本地直接跑 Star-Office-UI 后端并可视化
2. 用 `set_state.py` 接收我们主流程状态（不改生产配置）
3. 先打通单 Agent 看板（无需多人 join key）

---

## 6) 需要改造（本周可做）

1. 修复 `scripts/star-office-state.sh` 的状态映射与字段名
2. 将 `star-office-event.sh` 的事件语义扩展到 6 状态
3. 评估是否切换到 `agent-push` 机制支撑多人协同展示

---

## 7) 风险与限制

1. License 风险
   - 代码 MIT 可用
   - 美术资源非商用（如对外商用必须替换）
2. 稳定性风险
   - 项目更新快、功能较多（资产管理/生图/桌宠），建议先启用核心状态链路
3. 维护风险
   - 状态模型固定 6 类，后续复杂状态需长期维护映射规则

---

## 8) 明确下一步（3 条执行命令）

```bash
# 1) 启动项目（验证可运行）
cd /home/baiiy1/.openclaw/workspace/research/star-office-ui && python3 -m pip install -r backend/requirements.txt && cp -n state.sample.json state.json && (cd backend && python3 app.py)

# 2) 先人工验证状态链路（应在 UI 可见）
cd /home/baiiy1/.openclaw/workspace/research/star-office-ui && python3 set_state.py researching "接入链路联调中"

# 3) 对接我们现有事件脚本（最小改造前先做一次现网观察）
cd /home/baiiy1/.openclaw/workspace && bash scripts/star-office-event.sh task_start "subagent workflow started"
```

---

## 9) 建议优先级

- **P0（今天）**：完成脚本字段与状态映射兼容（否则状态展示失真）
- **P1（本周）**：接入多 Agent `join-agent/agent-push`，形成完整协作看板
- **P2（后续）**：资产替换与视觉定制，必要时替换为可商用素材
