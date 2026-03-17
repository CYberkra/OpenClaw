---
id: rule-index-registry
type: core-system
priority: high
scope: [index, registry, rule, navigation]
description: 规则注册表与导航中心，汇总所有文档的 Frontmatter 元数据供按需加载
last_updated: 2026-03-17
auto_generated: true
---

# 规则注册表 (Rule Registry)

> 本文件由 `scripts/sync-index.py` 自动生成，请勿手动编辑。
> 如需更新，运行：`python scripts/sync-index.py`

## 核心执行规则

| id | type | priority | scope | description | path |
|---|---|---|---|---|---|
| rule-user-preferences-main | core-system | high | user, preference, rule... | 用户长期执行偏好与硬规则的主源（SSOT），包含路由、验收、模式、交互等核心执行策略 | skills/user-preferences/SKILL.md |
| rule-index-registry | core-system | high | index, registry, rule... | 规则注册表与导航中心，汇总所有文档的 Frontmatter 元数据供按需加载 | rules/INDEX.md |
| rule-agents-overview | core-system | high | agent, session, startup... | 工作区高层规则与代理启动指引，包含内存管理、红线和社交指南 | AGENTS.md |
| rule-index-registry | core-system | high | index, registry, rule... | 规则注册表与导航中心，汇总所有文档的 Frontmatter 元数据供按需加载 | rules/INDEX.md |
| rule-user-preferences-main | core-system | high | user, preference, rule... | 用户长期执行偏好与硬规则的主源（SSOT），包含路由、验收、模式、交互等核心执行策略 | skills/user-preferences/SKILL.md |

## 辅助配置文档

| id | type | priority | scope | description | path |
|---|---|---|---|---|---|
| unknown | unknown | medium |  | Light change-control rules for configuration chang... | skills/change-control-lite/SKILL.md |
| unknown | unknown | medium |  | Real-time voice conversations in Discord voice cha... | skills/discord-voice/SKILL.md |
| unknown | unknown | medium |  | Use this skill whenever the user wants to create, ... | skills/docx-master/SKILL.md |
| unknown | unknown | medium |  | Text-to-speech conversion using node-edge-tts npm ... | skills/edge-tts/SKILL.md |
| unknown | unknown | medium |  | Helps users discover and install agent skills when... | skills/find-skills/SKILL.md |
| unknown | unknown | medium |  | Multi-agent workflow framework using JSON tickets ... | skills/fis-architecture/SKILL.md |
| unknown | unknown | medium |  | Convert documents and files to Markdown using mark... | skills/markdown-converter/SKILL.md |
| unknown | unknown | medium |  | Multi search engine integration with 17 engines (8... | skills/multi-search-engine/SKILL.md |
| unknown | unknown | medium |  | Work with Obsidian vaults (plain Markdown notes) a... | skills/obsidian/SKILL.md |
| unknown | unknown | medium |  | Text-to-speech via OpenAI Audio Speech API. | skills/openai-tts/SKILL.md |
| unknown | unknown | medium |  | Local speech-to-text with the Whisper CLI (no API ... | skills/openai-whisper/SKILL.md |
| unknown | unknown | medium |  | Transcribe audio via OpenAI Audio Transcriptions A... | skills/openai-whisper-api/SKILL.md |
| unknown | unknown | medium |  | Use this skill any time a .pptx file is involved i... | skills/pptx-master/SKILL.md |
| unknown | unknown | medium |  | Transform AI agents from task-followers into proac... | skills/proactive-agent-lite/SKILL.md |
| unknown | unknown | medium |  | Security-first skill vetting for AI agents. Use be... | skills/skill-vetter/SKILL.md |
| unknown | unknown | medium |  | Manager skill that delegates all tasks to sub-agen... | skills/subagent-manager/SKILL.md |
| unknown | unknown | medium |  | Summarize URLs or files with the summarize CLI (we... | skills/summarize/SKILL.md |
| rule-self-backup-audit | skill-detail | medium | backup, audit, maintenance... | 自我规则定期备份与漂移巡检方案，每3天执行一次一致性检查 | rules/self-backup-audit-v1.md |
| rule-system-bootstrap | core-system | medium | bootstrap, startup, quickstart... | 新代理快速启动入口，提供最小启动流程和规则优先级摘要 | SYSTEM_BOOTSTRAP.md |
| rule-tools-mappings | tool-spec | medium | tools, environment, mapping... | 环境特定映射与本地配置，包含路径、设备、主机、别名等 | TOOLS.md |
| rule-user-profile | agent-profile | medium | user, profile, identity... | 用户画像与稳定偏好事实，包含称呼、长期关注点等 | USER.md |
| rule-self-backup-audit | skill-detail | medium | backup, audit, maintenance... | 自我规则定期备份与漂移巡检方案，每3天执行一次一致性检查 | rules/self-backup-audit-v1.md |
| unknown | unknown | medium |  | Self-reflection + Self-criticism + Self-learning +... | self-improving/SKILL.md |
| unknown | unknown | medium |  | Light change-control rules for configuration chang... | skills/change-control-lite/SKILL.md |
| unknown | unknown | medium |  | Real-time voice conversations in Discord voice cha... | skills/discord-voice/SKILL.md |
| unknown | unknown | medium |  | Use this skill whenever the user wants to create, ... | skills/docx-master/SKILL.md |
| unknown | unknown | medium |  | Text-to-speech conversion using node-edge-tts npm ... | skills/edge-tts/SKILL.md |
| unknown | unknown | medium |  | Helps users discover and install agent skills when... | skills/find-skills/SKILL.md |
| unknown | unknown | medium |  | Multi-agent workflow framework using JSON tickets ... | skills/fis-architecture/SKILL.md |
| unknown | unknown | medium |  | Convert documents and files to Markdown using mark... | skills/markdown-converter/SKILL.md |
| unknown | unknown | medium |  | Multi search engine integration with 17 engines (8... | skills/multi-search-engine/SKILL.md |
| unknown | unknown | medium |  | Work with Obsidian vaults (plain Markdown notes) a... | skills/obsidian/SKILL.md |
| unknown | unknown | medium |  | Text-to-speech via OpenAI Audio Speech API. | skills/openai-tts/SKILL.md |
| unknown | unknown | medium |  | Local speech-to-text with the Whisper CLI (no API ... | skills/openai-whisper/SKILL.md |
| unknown | unknown | medium |  | Transcribe audio via OpenAI Audio Transcriptions A... | skills/openai-whisper-api/SKILL.md |
| unknown | unknown | medium |  | Use this skill any time a .pptx file is involved i... | skills/pptx-master/SKILL.md |
| unknown | unknown | medium |  | Transform AI agents from task-followers into proac... | skills/proactive-agent-lite/SKILL.md |
| unknown | unknown | medium |  | Security-first skill vetting for AI agents. Use be... | skills/skill-vetter/SKILL.md |
| unknown | unknown | medium |  | Manager skill that delegates all tasks to sub-agen... | skills/subagent-manager/SKILL.md |
| unknown | unknown | medium |  | Summarize URLs or files with the summarize CLI (we... | skills/summarize/SKILL.md |
| unknown | unknown | medium |  | Create distinctive, production-grade frontend inte... | tmp/skill_frontend_design_3/SKILL.md |

## 按需加载指引

主进程默认只读取本 INDEX 和各文件的 Frontmatter，命中 scope 或匹配 description 意图时才加载全文。

### 快速路由

- 代码任务 → 找 scope 含 `code` / `opencode` 的规则
- 多步骤任务 → 找 scope 含 `manager` / `multi-step` 的规则
- 调研任务 → 找 scope 含 `research` / `investigate` 的规则
- 高风险任务 → 找 priority 为 `high` 且 scope 含 `review` 的规则

---

*最后同步时间: 2026-03-17 14:09:01*