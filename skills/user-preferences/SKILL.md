---
name: user-preferences
description: User-specific operating rules and response requirements for baiiy1. Use for any task or response in this workspace, especially GPR work, Discord/Telegram messaging, image outputs, or system configuration.
---

# User Preferences

## Overview
Apply these rules whenever working for baiiy1. They override default habits and ensure consistent behavior.

## Rules & Requirements

### 1) Image outputs (hard rule)
- **Always do image analysis first, then explanation.**
- Use a fixed structure:
  1) 图像观察
  2) 变化/趋势
  3) 结论/影响
  4) 下一步建议（如需要）

### 2) GPR workflow
- **Deliver thorough results** (background suppression + AGC + cross‑correlation coverage).
- Post GPR progress/results in **#探地雷达gpr** (no @ mention).
- **If GPR-related content appears in other channels, sync it to #探地雷达gpr and reply there too.**
- Demo with synthetic data if needed; **do not modify** user’s PythonModule repo.

### 2.1) Multi-agent sync
- Sub-agent dispatch/progress/completion must be synchronized to **channel:1477202149728587952**.

### 3) Priority order
- **QMD > GPR > 语音**. Keep QMD enabled. No A/B testing that disables it.

### 4) Cross‑platform sync
- Partial Discord+Telegram sync is OK via **#全平台同步** anchor.

### 5) Model usage
- Use **openai-codex/gpt-5.2-codex** for main work.
- If multi‑agent coding role exists, use **codex5.3**.
- Keep multi‑agent mode available; when you decide multi‑agent is needed, use it and **post the coordination updates so the user can see the scheduling/dispatch process**.

### 6) Paths & stability
- All files/caches under **E:\Openclaw** (`/mnt/e/Openclaw/.openclaw`).
- Avoid downtime; don’t stop WSL unless required.

### 7) Feishu policy
- Create/append/read only. **No deletions** without explicit consent.

### 8) Messaging
- **No @mention** in Discord replies.
- Be concise, avoid spam in group chats; respond when asked or when valuable.

### 9) Memory & Git
- Important behavior changes/preferences: write to memory.
- Auto‑push meaningful memory changes to GitHub (rebase, no force).
- **If any task has progress, proactively sync updates to the user.**
- **禁止将任何 token/apiKey/含key的URL 写入 memory 或 commit。**
- **push 前必须 git diff --stat；并在 memory 留 commit hash 指针。**

## Rule Routing & Archival Policy (v1)

When deciding where a new rule, preference, or note should live, use this routing policy:

- **Temporary / same-day context** → `memory/YYYY-MM-DD.md`
- **User-executable long-term preferences and constraints** → `skills/user-preferences/SKILL.md`
- **Rule history / snapshot / audit trail** → `skills/rule-archive-lite/SKILL.md`
- **User profile facts** (name, preferred form of address, long-term focus) → `USER.md`
- **Environment-specific mappings** (paths, devices, hosts, aliases) → `TOOLS.md`
- **Project-specific rules** → the project directory (`README`, `docs`, project `AGENTS.md`, or a dedicated `RULES.md`)
- **Workspace-wide high-level operating rules** → `AGENTS.md`

When a rule affects both execution and traceability, update multiple layers together:
- New/changed user hard rule → `user-preferences` + `rule-archive-lite` + `memory/YYYY-MM-DD.md`
- Environment change with execution impact → `TOOLS.md` + `memory/YYYY-MM-DD.md` (and `user-preferences` if it becomes a hard constraint)
- User profile change that affects execution → `USER.md` + `user-preferences` (if it changes behavior)
- Project workflow change → project-local docs/rules first; only elevate to workspace-level files if it generalizes across projects

## Workflow Clarifications v1.1（执行细化）

1) 角色边界：`subagent_manager` 负责拆解编排；`opencode` 为默认代码执行器；`coder` 仅在 opencode 不可用/失败或明确指定时兜底。
2) 模式切换：默认 `default`；可由用户关键词切到 `strict/proactive/evolver/ralph`；冲突优先级 `strict > ralph > evolver > proactive > default`。
3) 规则优先级：`用户当轮明确指令 > user-preferences > AGENTS 硬规则 > rule-archive 快照 > 其他`。
4) 防漂移：新增/变更硬规则必须同轮联动更新 `user-preferences + rule-archive-lite + memory/YYYY-MM-DD.md`。
5) 关键词规范：
   - 路由：`直答` / `走 manager` / `走 opencode` / `加 reviewer` / `开 CI`
   - 模式：`切 strict` / `切 proactive` / `切 evolver` / `切 ralph` / `恢复 default`
   - 验收：`仅到 G3` / `执行全闸门` / `跳过 CI（需理由）`

## Usage Notes
- When outputting plots, ensure data parsing is correct (respect column definitions and A‑scan reshaping). If input format is ambiguous, ask or infer carefully, and state assumptions.
- Always include a short analysis paragraph after posting plots.
