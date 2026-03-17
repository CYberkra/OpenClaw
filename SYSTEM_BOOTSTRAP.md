---
id: rule-system-bootstrap
type: core-system
priority: medium
scope: [bootstrap, startup, quickstart, agent]
description: "新代理快速启动入口，提供最小启动流程和规则优先级摘要"
---

# SYSTEM_BOOTSTRAP

> 目标：给新 agent 的**快速入口**（不是全量手册）。
> 原则：先看索引与主规则，按需加载，避免旧流程漂移。

## 0) Quick Start（首轮最小启动）

1. 读取 `rules/INDEX.md`（导航 + 规则优先级）
2. 读取 `skills/user-preferences/SKILL.md`（执行主源 SSOT）
3. 如需追溯历史规则，再读取 `skills/rule-archive-lite/SKILL.md`
4. 仅在任务命中时按需加载其他文档

## 1) 当前角色与主流程

- **主进程**：路由判定、人工核验、对外回传
- **subagent_manager**：任务拆解/并行编排（不做最终代码执行）
- **opencode**：默认代码执行器
- **coder**：仅在 opencode 不可用/失败时兜底
- **reviewer/researcher**：按需附加（复核/调研）

主流程：路由 → 执行（必要时 manager 编排）→ 验收闸门（G1-G6）→ 对外回传

## 核心文档导航

| 文档 | 用途 | 链接 |
|---|---|---|
| user-preferences | 执行主源（SSOT） | [查看](skills/user-preferences/SKILL.md) |
| AGENTS | 高层摘要 | [查看](AGENTS.md) |
| INDEX | 规则注册表 | [查看](rules/INDEX.md) |
| rule-archive-lite | 历史归档 | [查看](skills/rule-archive-lite/SKILL.md) |
| SYSTEM_BOOTSTRAP | 本文件（启动入口） | - |

> 详细执行规则、路由判定、验收闸门、模式切换等，请查阅 `skills/user-preferences/SKILL.md`（主源）。
