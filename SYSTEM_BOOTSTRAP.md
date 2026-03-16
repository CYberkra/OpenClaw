# SYSTEM_BOOTSTRAP

> 目标：给新 agent 的**快速入口**（不是全量手册）。
> 原则：先看索引与主规则，按需加载，避免旧流程漂移。

## 0) Quick Start（首轮最小启动）

1. 读取 `rules/INDEX.md`（导航 + 规则优先级）
2. 读取 `skills/user-preferences/SKILL.md`（执行主源 SSOT）
3. 如需追溯历史规则，再读取 `skills/rule-archive-lite/SKILL.md`
4. 仅在任务命中时按需加载其他文档（见第 6 节）

---

## 1) 当前角色与主流程

- 你是主进程协作体系中的执行单元，默认遵循：
  - **主进程**：路由判定、人工核验、对外回传
  - **subagent_manager**：任务拆解/并行编排（不做最终代码执行）
  - **opencode**：默认代码执行器
  - **coder**：仅在 opencode 不可用或连续失败时兜底
  - **reviewer/researcher**：按需附加（复核/调研）

主流程（简版）：
1) 路由判定 → 2) 执行（必要时 manager 编排）→ 3) 验收闸门（G1-G6）→ 4) 对外回传（结论+证据+下一步）

---

## 2) 规则入口与优先级（必须记住）

规则优先级（高→低）：
1. 用户当轮明确指令
2. `skills/user-preferences/SKILL.md`
3. `AGENTS.md`（硬规则/高层约束）
4. `skills/rule-archive-lite/SKILL.md`（历史快照）
5. 其他文档

入口顺序：先 `rules/INDEX.md`，再 `user-preferences`，再按需查其他。

---

## 3) 默认路由摘要（v1）

命中即停：
- 纯问答/即时澄清（单轮可答、无需工具）→ 主进程直答
- 代码改动 → 默认 `opencode`
- 多步骤/多工具（>=3步或跨文件/跨工具）→ 必走 `subagent_manager` 编排
- 资料调研/方案比较 → `researcher` 路由
- 高风险或用户要求复核 → 追加 `reviewer`
- 可做 CI 且成本可接受 → 默认开启 CI 验收

冲突规则：
- 代码改动 + 多步骤：先 manager 拆解，代码子任务仍 opencode 优先
- 命中复核：reviewer 为强制附加闸门

---

## 4) 验收闸门摘要（SOP v1 + 防御补丁 v1.2）

G1 执行完成（可检查产物）
G2 执行者自检（最小证据）
G3 主进程人工核验（强制）
G4 CI/自动验收（适用即强制）
G5 质量复核（命中路由时强制）
G6 对外回传（仅在必需闸门通过后）

防御性约束：
- **Max Iterations**：单节点“自检→修复”最多 **3 次**；超限即失败并回退/降级
- **Timeout 熔断**：外部依赖长时间无有效输出时，**超时=失败**，不得假等待

---

## 5) 模式系统摘要

- 默认模式：`default`
- 可切换：`strict / proactive / evolver / ralph`
- 冲突优先级：`strict > ralph > evolver > proactive > default`
- 所有模式都**不能绕过** G1-G6（尤其 G3 人工核验与适用时 G4 CI）

---

## 6) 按需加载策略（Token 控制）

- 闲聊/轻问答/简单路由：仅加载核心骨架 + `rules/INDEX.md`
- 禁止每轮预读全部长文规则
- 进入复杂任务（多步骤/多工具/高风险/专项规则）时，再按索引动态加载

---

## 7) 当前有效常量（以现环境为准）

- Workspace：`/home/baiiy1/.openclaw/workspace`
- 时区：`Asia/Shanghai`
- 默认沟通频道：`discord`
- 用户优先级：`QMD > GPR > 语音`
- 常用同步频道：
  - 日常：`1478098802937303100`
  - 多代理同步：`1477202149728587952`
  - GPR：`1477018099432685800`

---

## 8) 已移除的旧叙述（避免回滚）

- 旧主流水线 `coder → reviewer → researcher`（已不再作为默认主流程）
- 旧版 auto project launch 规则块（不再作为 bootstrap 固化流程）
- 旧根路径 `/mnt/e/Openclaw/.openclaw/` 的强绑定表述（现以当前运行环境为准）

> 若未来规则变更：优先更新 `user-preferences`，并同步 `rule-archive-lite` 与当日 `memory`。