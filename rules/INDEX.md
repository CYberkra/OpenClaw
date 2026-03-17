---
id: rule-index-registry
type: core-system
priority: high
scope: [index, registry, rule, navigation, frontmatter]
description: "规则注册表与导航中心，汇总所有文档的 Frontmatter 元数据供按需加载"
---

# 规则注册表（Frontmatter Registry）

> **按需加载指引**：主进程默认只读取本 INDEX 和各文件的 Frontmatter，命中 scope 或匹配 description 意图时才加载全文。

## 核心执行规则

| id | type | priority | scope | description |
|---|---|---|---|---|
| rule-user-preferences-main | core-system | high | [user, preference, rule, execution, routing, mode] | 用户长期执行偏好与硬规则的主源（SSOT），包含路由、验收、模式、交互等核心执行策略 |
| rule-agents-overview | core-system | high | [agent, session, startup, memory, bootstrap] | 工作区高层规则与代理启动指引，包含内存管理、红线和技能速查 |
| rule-index-registry | core-system | high | [index, registry, rule, navigation, frontmatter] | 规则注册表与导航中心，汇总所有文档的 Frontmatter 元数据供按需加载 |
| rule-archive-lite-snapshot | core-system | medium | [archive, history, snapshot, rule] | 规则历史归档快照，用于追溯和审计，非执行主源 |
| rule-self-backup-audit | skill-detail | medium | [backup, audit, maintenance, drift] | 自我规则定期备份与漂移巡检方案，每3天执行一次一致性检查 |

## 辅助配置文档

| id | type | priority | scope | description |
|---|---|---|---|---|
| rule-system-bootstrap | core-system | medium | [bootstrap, startup, quickstart, agent] | 新代理快速启动入口，提供最小启动流程和规则优先级摘要 |
| rule-user-profile | agent-profile | medium | [user, profile, identity, preference] | 用户画像与稳定偏好事实，包含称呼、长期关注点等 |
| rule-tools-mappings | tool-spec | medium | [tools, environment, mapping, config, alias] | 环境特定映射与本地配置，包含路径、设备、主机、别名等 |

## 规则优先级（高 → 低）

1. 用户当轮明确指令
2. `skills/user-preferences/SKILL.md` (rule-user-preferences-main)
3. `AGENTS.md` (rule-agents-overview)
4. `skills/rule-archive-lite/SKILL.md` (rule-archive-lite-snapshot)
5. 其他文档

## 文档路由速查

- 需要"现在就怎么执行" → `skills/user-preferences/SKILL.md`
- 需要"规则怎么来的/历史版本" → `skills/rule-archive-lite/SKILL.md`
- 需要"用户身份/称呼/长期偏好" → `USER.md`
- 需要"路径/设备/环境映射" → `TOOLS.md`
- 需要"今天发生过什么" → `memory/YYYY-MM-DD.md`
- 需要"专项规则细节" → `rules/` 对应文件

## 变更联动原则（防漂移）

- 新增/修改**硬规则**：必改 `user-preferences` + 必留痕 `rule-archive-lite` + `memory/YYYY-MM-DD.md`
- 仅当日临时约束：只写 `memory/YYYY-MM-DD.md`
- 用户画像变化：更新 `USER.md`，若影响执行行为再同步 `user-preferences`
- 环境/路径/设备变化：更新 `TOOLS.md`，若升格为硬约束再同步 `user-preferences`

## 用户关键词速查

- **路由**：`直答` / `走 manager` / `走 opencode` / `加 reviewer` / `开 CI`
- **模式**：`切 strict` / `切 proactive` / `切 evolver` / `切 ralph` / `恢复 default`
- **验收**：`仅到 G3` / `执行全闸门` / `跳过 CI（需理由）`

## 维护说明

本注册表仅在以下情况更新：
- 新增/删除规则文档
- 规则 Frontmatter 元数据变更
- 规则优先级或路由关系变化

日常规则内容变更无需修改本文件，只需确保各文档自身的 Frontmatter 准确即可。
