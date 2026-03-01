---
name: rule-archive-lite
description: Persist user operating rules and execution constraints. Use when the user defines workflow rules (report cadence, evidence requirements, model policy, sub-agent policy) and asks to save/apply them across restarts.
---

# Rule Archive Lite

## Overview
Store and apply user-defined operating rules so they survive restarts. Treat these rules as binding unless explicitly changed.

## Current Rules Snapshot (2026-03-01)
1) 节流模式：先检索后推理；qmd search 取最相关3条，必要才 qmd get -l 80。
2) 输出默认短：结论+关键依据+下一步；≤10行；除非用户要求展开。
3) 分两段走：先给计划/要点/需输入，待“继续”再执行。
4) 子代理串行：coder → reviewer → researcher；每次只启1个。
5) 控制上下文注入：仅引用今天 memory + 本次必要变量。
6) 模型分层：默认 gpt-5.3-codex；低风险可用 5.2；关键结论回 5.3；切换需说明原因；gpt-5.3 reasoning=medium。
7) 工具调用最小化：不跑 qmd embed/query 深探针，除非明确要求。
8) 用量提醒：已用百分比每消耗 10% 提醒；Brave 额度剩余5%停止；并在用量不可查时说明。
9) 交付循环：每15分钟至少1个可验证交付（memory/reports/scripts/commit），无则“无交付+原因+预计”；交付前自检并给 qmd 证据；每小时汇报必须基于证据。
10) 证据命令固定：qmd get qmd://openclaw_workspace/memory/YYYY-MM-DD.md --from <行号> -l 80。
11) GPR 规则：所有进展落盘 memory 并 git push；同步到 #探地雷达gpr；禁止 @。
12) 规则存档：变更需写入 memory 并提交。

## Workflow
1) 用户新增/修改规则 → 追加到 memory/YYYY-MM-DD.md。
2) 更新本技能“Current Rules Snapshot”。
3) git commit + push（私有仓库）。
4) 回报“已归档并推送”。

## Guardrails
- 规则冲突时以用户最新指令为准。
- 不删除历史规则，改用追加与标注替代。
