---
name: change-control-lite
description: Light change-control rules for configuration changes, backups, and periodic GitHub updates. Use when planning or executing config changes that might impact connectivity/availability, or when deciding whether to back up/update/push memory or important files to GitHub.
---

# Change Control (Lite)

- Before any configuration change that could impact connectivity or availability, notify the user and explicitly ask for approval.
- Always include a rollback plan before changes (e.g., which backup to restore, or exact commands to revert).
- Create a backup before making the change.
  - Prefer a timestamped copy in `backups/` under the workspace.
  - Keep the backup until the user confirms no safety risk; delete only after confirmation.
- Backup scope should be explicit (e.g., MEMORY.md, memory/*, key config files).
- If a disconnection occurs or is likely, inform the user immediately and explain what happened.

## Periodic GitHub Updates

- Periodically (self-judged cadence), update/push memory and other important files to GitHub.
- Avoid pushing sensitive data without user approval.
- After each update, notify the user with a brief summary of what was pushed.
