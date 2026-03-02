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
- Sub-agent dispatch/progress/completion must be synchronized to **#multi-agent**.

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

## Usage Notes
- When outputting plots, ensure data parsing is correct (respect column definitions and A‑scan reshaping). If input format is ambiguous, ask or infer carefully, and state assumptions.
- Always include a short analysis paragraph after posting plots.
