---
name: gpr-memory-archive-lite
description: Enforce GPR progress archival. Use whenever you produce GPR progress, conclusions, parameter changes, plots, or experiment updates. Requires writing a structured entry to memory/YYYY-MM-DD.md and immediately committing + pushing to the private GitHub repo as the source of truth.
---

# GPR Memory Archive Lite

## Overview
Ensure every GPR milestone is recorded in a traceable, versioned Markdown log and pushed to the private GitHub repo. Chat updates are secondary; GitHub MD is the source of truth.

## Workflow (mandatory)

### 1) Append a memory entry (do not overwrite)
**Path:** `/mnt/e/Openclaw/.openclaw/workspace/memory/YYYY-MM-DD.md`

**Template (copy exactly):**
```
[HH:MM] <短标题>

Context / 数据：

dataset: <文件名/来源>

repo: <仓库/分支/commit>

script: <涉及脚本/函数>

params: <关键参数（窗口、ntraces、length_trace…）>

Steps / 做了什么：

...

...

Results / 结果：

图像/输出：<文件路径>

指标：<SNR/对比/异常现象>

结论：<一句话结论>

Issues / 风险：

<NaN trace / 列全零 / 参数不自洽 / 不可复算原因…>

Next / 下一步：

researcher: ...

coder: ...

reviewer: ...
```

### 2) GitHub 归档（私有仓库）
- 只提交：`memory/*.md`、`reports/*.md`、`scripts/*.py` 等文本
- 禁止提交：token/凭据、`openclaw.json`、`credentials/`、原始数据大文件（csv/png/sqlite）、任何 `.env`

**提交节奏：** 每次写完记忆条目后，立即 `git add/commit/push`

**commit message 格式：**
```
Sync: OpenClaw GPR memory YYYY-MM-DD HH:MM
```

### 3) 同步到 GPR 频道
- 所有 GPR 进展同时在 **#探地雷达gpr** 同步
- **禁止 @mention**
- 以 GitHub 的 MD 为“真源”

### 4) 主动回报
每次 push 后必须回复：
```
已归档并推送：YYYY-MM-DD.md（新增X条）
```

## Guardrails
- 路径固定：`/mnt/e/Openclaw/.openclaw/workspace/`
- 只追加，不覆盖
- 不提交敏感信息或原始大文件
