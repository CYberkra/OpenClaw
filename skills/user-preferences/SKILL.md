---
id: rule-user-preferences-main
type: core-system
priority: high
scope: [user, preference, rule, execution, routing, mode]
description: "用户长期执行偏好与硬规则的主源（SSOT），包含路由、验收、模式、交互等核心执行策略"
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

### 11) 模式精简规则 v1

**可用模式**：default（默认）/ strict / proactive / evolver / ralph

**使用频率统计**（基于历史数据）：
- `default`: 90% 场景
- `strict`: 5% 场景（高风险任务）
- `proactive`: 3% 场景（需要主动建议）
- `evolver`: 1% 场景（自我改进实验）
- `ralph`: 1% 场景（特定实验）

**简化策略**：
- **90% 任务用 default**，无需切换
- **高风险/关键任务用 strict**（用户明确指令）
- **其他模式仅在明确请求时启用**，默认不推荐

**模式冲突优先级**：`strict > ralph > evolver > proactive > default`

---

### 12) 心跳任务自动化规则 v1

**自动检查项**（每 3 天）：
- [ ] GitHub 未推送的 memory 变更
- [ ] 未归档的规则更新
- [ ] Skill 更新/新增

**自动执行**：
- 检测到未推送变更 → 自动 commit + push
- 汇报："已自动推送 X 条未归档变更"

**手动检查项**（需用户触发）：
- 日历检查
- 邮件检查
- 天气检查

---

## Workflow Clarifications v1.1（执行细化）

1) 角色边界：`subagent_manager` 负责拆解编排；`opencode` 为默认代码执行器；`coder` 仅在 opencode 不可用/失败或明确指定时兜底。
2) 模式切换：默认 `default`；可由用户关键词切到 `strict/proactive/evolver/ralph`；冲突优先级 `strict > ralph > evolver > proactive > default`。
3) 规则优先级：`用户当轮明确指令 > user-preferences > AGENTS 硬规则 > rule-archive 快照 > 其他`。
4) 防漂移：新增/变更硬规则必须同轮联动更新 `user-preferences + rule-archive-lite + memory/YYYY-MM-DD.md`。
5) 关键词规范：
   - 路由：`直答` / `走 manager` / `走 opencode` / `加 reviewer` / `开 CI`
   - 模式：`切 strict` / `切 proactive` / `切 evolver` / `切 ralph` / `恢复 default`
   - 验收：`仅到 G3` / `执行全闸门` / `跳过 CI（需理由）`

## Defensive Patches v1.2（防御性补丁，强制）

### A) 防死循环机制（Max Iterations）
- 适用范围：任何单步任务中的“自检 → 自动修复”内部循环（例如 opencode 改代码、修 bug）。
- 硬上限：同一节点最多 **3 次**迭代。
- 触发条件：连续 3 次仍未解决，或仍未达到 **G2 执行者自检通过标准**。
- 强制动作：立即打断循环，判定该节点失败，进入失败回退/降级流程，并向主进程与用户报告失败原因。

### B) 防僵尸状态（Timeout 熔断）
- 适用范围：所有外部依赖环节（含 G4 CI/自动验收、测试脚本、外部工具响应等待）。
- 规则：长时间卡死且无有效输出时，必须主动超时熔断。
- 结果等价：**超时 = 该闸门失败**，不得继续“假等待”。
- 强制动作：直接走失败降级/回退，并向用户明确回报：`执行超时`。

### C) 上下文与 Token 消耗管理（按需加载）
- 日常闲聊、轻量问答、简单路由判定：默认仅常驻核心骨架规则 + `rules/INDEX.md`。
- 禁止每轮预加载所有长文规则文件。
- 仅当进入复杂路由（多步骤/多工具/高风险/需专项规则）时，按 `rules/INDEX.md` 动态读取所需细分文档。

## New Channel Rule Application Policy

- **Default**: All new Discord channels created within this workspace automatically inherit the current rule system
- **Scope**: Includes but not limited to:
  - YAML Frontmatter + Lazy Loading mechanism
  - Default routing table (v1)
  - Acceptance gates (G1-G6)
  - Workflow modes (default/strict/proactive/evolver/ralph)
  - Intelligent interactive prompts (buttons)
  - Response style (standard: conclusion + key evidence)
  - Rule audit and health check procedures
- **Exceptions**: Only if explicitly specified otherwise by user during channel creation
- **Documentation**: New channels should reference `rules/INDEX.md` for rule navigation

## Response Style Preference

- **Default**: Standard (balanced)
- **Format**: Conclusion (1 sentence) + Key Evidence (2-3 points) + Next Step (if applicable)
- **Avoid**: Verbose replies unless explicitly requested
- **Buttons**: Offer [View Details] or [Expand] for users who want more

## Discord Interactive Controls Preference

- **Message Format (Mandatory)**: Use **separate messages** for content and buttons:
  - Message 1: Pure text with full explanation/details
  - Message 2: Pure buttons for selection/confirmation (simplified format)
  - Never mix complex text blocks with buttons in a single message
- **Button Format (Working)**: Use simplified structure only:
  ```json
  {"blocks": [{"type": "actions", "buttons": [...]}]}
  ```
  - Do NOT include "text" elements in the same message as buttons
  - Do NOT use "accessory" or complex nested structures
- **Priority use cases**:
  - authorization (allow / cancel)
  - option selection (plan A/B/C, choose skill, choose route)
  - workflow progression (continue / pause / direct apply / plan only)
  - acceptance level (仅到 G3 / 执行全闸门 / 加 reviewer)
  - mode switching (`default` / `strict` / `proactive` / `evolver` / `ralph`)
- **High-risk actions** (delete / install / push / enable experimental high-autonomy mode): Must clearly state what will happen in the text message (Message 1) before showing buttons (Message 2).
- **Fallback**: If buttons fail to render, automatically fall back to numbered list selection (reply with number 1-N).

## SYSTEM_BOOTSTRAP Maintenance Policy

- `SYSTEM_BOOTSTRAP.md` is a live bootstrap entry, not a historical note.
- It must be checked and updated whenever any of the following becomes stably true:
  - default workflow topology changes
  - routing / acceptance / mode system changes
  - rule entrypoints or rule priority changes
  - key constants change (paths, channels, priorities, default execution assumptions)
- In addition to event-driven updates, run a lightweight consistency review every **7–14 days**.
- Updates should keep the file short, bootstrap-oriented, and aligned with `rules/INDEX.md` + `skills/user-preferences/SKILL.md`.

## Intelligent Interactive Prompt Policy v1.4

- **Trigger Conditions** (automatically pop up interactive prompts with buttons):
  1. **Complex Task Start**: When a task has ≥2 distinct execution paths → offer [Plan Only] [Direct Implementation] [Research First]
  2. **High-Impact Actions**: Before git push / delete / install / config changes → require explicit [✅ Confirm] [❌ Cancel]
  3. **Workflow Mode Selection**: At task start when a specific mode is recommended → offer [default] [strict] [proactive] [evolver] [ralph]
  4. **Task Blocked**: After 3 failed self-checks or timeout → offer [Retry] [Alternative] [Skip] [Human Intervention]
  5. **Acceptance Gate**: After G3/CI/reviewer completion → offer [Continue CI] [Deliver] [Refine]
  6. **Periodic Audit (every 3 days)**: When uncommitted rule changes detected → offer [Commit Now] [Later] [View Details]

- **Button Design**:
  - 🟢 Green (success): Confirm/Allow/Continue
  - 🔴 Red (danger): Cancel/Stop/Risky operations
  - 🔵 Blue (primary): Main recommended option
  - ⚪ Gray (secondary): Alternative options

- **Constraints**:
  1. Content must be presented BEFORE buttons (never buttons-only)
  2. High-risk actions must explicitly state what will happen above buttons
  3. Buttons expire after 15 minutes (requires re-trigger if timeout)
  4. Typed replies override button clicks
  5. Mode persistence rules still apply (confirm before each task if persistent)

- **Fallback**: If Discord components unavailable, fall back to numbered list for typed selection.
