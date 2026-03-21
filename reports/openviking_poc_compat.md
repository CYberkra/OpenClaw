# OpenViking 最小 PoC 与 OpenClaw 现有记忆体系兼容性评估

- 时间：2026-03-11
- 范围：`OpenViking README/README_CN`、`examples/openclaw-memory-plugin/README.md` 与插件源码（`config.ts`/`index.ts`/`setup-helper/cli.js`），对照当前工作区 `memory/ops-playbook.md` + `MEMORY.md` + 现有 OpenClaw 配置。

---

## 0) 本次实际 PoC 执行结果（最小验证）

已执行（在隔离目录 `/tmp/openviking_poc`，未改生产配置）：

1. 克隆 OpenViking 仓库并阅读文档/示例。  
2. 创建独立虚拟环境并安装 `openviking`（安装成功，版本 `0.2.5`）。  
3. 使用最小 `ov.conf` 尝试启动 `openviking-server`。  
4. 启动失败，日志明确报错：`embedding.dense` 与 `vlm` 的 `api_key` 必填（无 key 无法完成服务启动）。

结论：
- **OpenViking 服务可安装**；
- **无 embedding/vlm API key 时无法完成服务启动**（至少在本次配置/版本下如此）；
- 当前生产 OpenClaw 配置未被修改（本次 PoC 仅在 `/tmp` 进行）。

---

## 1) OpenViking + openclaw-memory-plugin 接入步骤（从文档与源码归纳）

## A. 依赖与前置

### Local 模式（插件自动拉起 OpenViking）
- 必需：
  - OpenClaw（`openclaw`）
  - Python >= 3.10
  - `openviking` Python 包
- 文档前置还提到（尤其源码安装/构建路径）：
  - Go（README 说 1.22+；setup-helper 检查为 1.19+）
  - `cmake`、`g++`（setup-helper 会检查）

### Remote 模式（连接已有 OpenViking 服务）
- OpenClaw + memory-openviking 插件即可。
- OpenViking 服务端独立部署在别处，客户端无需本地 Python/openviking。

## B. 插件部署

推荐方式（官方）：
- 在 OpenViking 仓库执行：
  - `npx ./examples/openclaw-memory-plugin/setup-helper`

手工方式（README）：
- 复制 `index.ts/config.ts/client.ts/process-manager.ts/memory-ranking.ts/text-utils.ts/openclaw.plugin.json/package.json` 到 `~/.openclaw/extensions/memory-openviking`
- `npm install`

## C. OpenClaw 关键配置

核心配置项（README + `config.ts`）：
- `plugins.enabled = true`
- `plugins.slots.memory = memory-openviking`（注意：这是**替换 memory slot**）
- `plugins.entries.memory-openviking.config.*`

常用项：
- `mode`: `local|remote`（默认 `local`）
- `configPath`（local）：默认 `~/.openviking/ov.conf`
- `port`（local）：默认 `1933`
- `baseUrl`（remote）：默认 `http://127.0.0.1:1933`
- `targetUri`：默认 `viking://user/memories`
- `autoRecall`：默认 true
- `autoCapture`：默认 true
- `recallLimit`：默认 6
- `recallScoreThreshold`：默认 0.01

## D. OpenViking 服务配置（`ov.conf`）

从 README 与 setup-helper 归纳，最小必需：
- `storage.workspace`（数据存储目录）
- `embedding.dense`：`provider/api_base/model/dimension/api_key`
- `vlm`：`provider/api_base/model/api_key`

默认（setup-helper）常见值：
- workspace：`~/.openviking/data`
- server port：`1933`
- agfs port：`1833`
- volcengine 默认模型：
  - VLM：`doubao-seed-2-0-pro-260215`
  - embedding：`doubao-embedding-vision-251215`

---

## 2) 与现有方案（`memory/ops-playbook.md` + `MEMORY.md`）的兼容性分析

## 现状（当前体系）
- 长期/可审计记忆以**文件优先**：
  - `memory/YYYY-MM-DD.md`（日记式原始记录）
  - `MEMORY.md`（长期提炼）
  - `memory/ops-playbook.md`（运维策略）
- OpenClaw 当前配置显示 memory backend 为 **qmd**（非 OpenViking）。

## 可获得收益（引入 OpenViking 旁路后）
- 自动 recall/capture，减少纯手工整理负担。
- 分层与目录式检索（L0/L1/L2 + URI）有机会降低注入 token 噪声。
- 可以把“用户偏好/任务经验”变为可检索对象，增强跨会话关联。

## 冲突点/风险点
1. **memory slot 单占冲突**：
   - `plugins.slots.memory` 一次只能指向一个插件；切到 `memory-openviking` 即等于替换当前 slot。  
2. **双记忆并行的语义冲突**：
   - 若保持现有文件记忆 + qmd + OpenViking 同时做注入，可能出现重复注入、冲突片段、排序不稳。  
3. **配置与稳定性风险**：
   - OpenViking 依赖 embedding/vlm 服务；key 失效会直接影响 recall/capture。  
4. **数据一致性风险**：
   - 文件记忆是“人工可读真相源”；OpenViking 抽取是“模型生成记忆”，可能有抽象偏差。

## 总体兼容判断
- **可兼容，但应走“旁路试验 + 明确真相源”策略**。  
- 建议将 `memory/*.md + MEMORY.md` 继续作为 source-of-truth；OpenViking 先作为“辅助检索层”。

---

## 3) 最小接入策略（不替换现有，只做旁路试验）

目标：不动现网主会话的 qmd/file 记忆主链路，仅在隔离实例验证 OpenViking 价值。

## Phase 1：隔离环境 PoC（推荐）

1. 新建独立 OpenClaw state 目录（例如 `~/.openclaw-openviking-poc`）。  
2. 在该目录安装/启用 `memory-openviking`，主目录 `~/.openclaw` 不改。  
3. OpenViking 建议先用 **remote 模式** 对接独立服务（便于停启与回滚）。  
4. 只在 PoC agent/channel 使用，不切主流量。

判定指标（最小）：
- recall 命中是否稳定
- token 注入长度与主链路对比
- 是否出现“误召回/重复注入”

## Phase 2：旁路灰度

1. 保持 `memory/*.md + MEMORY.md` 继续写入（人工主账本）。  
2. OpenViking 仅用于 recall 辅助；必要时限制：
   - `recallLimit`（如 3~4）
   - 提高 `recallScoreThreshold`（如 0.1~0.2）
3. 先在低风险任务（FAQ、偏好问答）试运行。

## Phase 3：评估后决策

- 若收益明确且稳定，再评估是否扩大范围。  
- 在未验证前，不建议替换主记忆后端。

---

## 4) 回滚方案（必须可一键撤回）

## A. 配置回滚
- 回滚前备份：`openclaw.json`（或 `openclaw config export`）。
- 回滚动作：
  1. 将 `plugins.slots.memory` 恢复为原值（当前体系对应 qmd/既有配置）。
  2. `plugins.entries.memory-openviking.enabled=false`（或移除 entry）。
  3. 重启 `openclaw gateway`。

## B. 进程回滚
- local 模式：停止 OpenViking 子进程/服务。
- remote 模式：断开 baseUrl 或关闭远端服务。

## C. 数据层回滚
- OpenViking 数据目录独立（如 `~/.openviking/data-poc`），可直接归档/删除。
- 文件记忆 (`memory/*.md`, `MEMORY.md`) 全程不动，天然可恢复。

---

## 5) 建议的最小落地命令骨架（用于主进程执行）

> 仅示意（旁路目录），避免改现网默认目录。

```bash
# 1) 隔离 state dir
export OPENCLAW_STATE_DIR="$HOME/.openclaw-openviking-poc"

# 2) 部署插件（在 OpenViking repo 内）
cd /path/to/OpenViking
npx ./examples/openclaw-memory-plugin/setup-helper --workdir "$OPENCLAW_STATE_DIR"

# 3) 启动（local 模式）
source "$OPENCLAW_STATE_DIR/openviking.env"
openclaw gateway
```

Remote 模式把 `mode=remote` + `baseUrl` 指向独立 OpenViking 服务即可。

---

## 6) 结论（给决策者）

- **可做**：OpenViking 作为旁路记忆检索层，与现有文件记忆体系可并存。  
- **不要直接替换主链路**：memory slot 单占 + 抽取型记忆存在偏差风险。  
- **先旁路 PoC，再灰度**：隔离 state dir、独立数据目录、可一键回滚。  
- **本次实测关键门槛**：embedding/vlm API key 缺失时 OpenViking 服务无法启动，接入前必须先落实模型服务配置。
