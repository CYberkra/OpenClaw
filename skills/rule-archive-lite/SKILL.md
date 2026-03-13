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
6) 模型分层：默认 5.2；关键代码/关键结论用 5.3；切换需说明原因。
7) 工具调用最小化：不跑 qmd embed/query 深探针，除非明确要求。
8) 用量提醒：已用百分比每消耗 10% 提醒；Brave 额度剩余5%停止；并在用量不可查时说明。
9) 交付循环：每15分钟至少1个可验证交付（memory/reports/scripts/commit），无则“无交付+原因+预计”；交付前自检并给 qmd 证据；每小时汇报必须基于证据。
10) 证据命令顺序：
   - 默认：grep -n "EDL-ID:" <file>
   - 次选：tail -n 20 <file>
   - 仅在 grep 得到真实行号后，允许 qmd get --from <真实行号> -l 30。
11) GPR 规则：所有进展落盘 memory 并 git push；同步到 #探地雷达gpr；禁止 @。
12) 多Agent协作：派单/进度/完成需同步到 channel:1477202149728587952 频道。
13) 规则存档：变更需写入 memory 并提交。
14) 证据/交付路径：一律 /mnt/e/Openclaw/.openclaw/...；允许 ~/.openclaw 作为别名但不得出现在证据里。
15) Subagent Manager 强制策略：凡任务存在正向收益（效率/质量/并行/上下文隔离），必须优先使用 subagent_manager skill；仅在明显不适配的极小任务可豁免，并简要说明。
16) Token 回报规则：用户已取消“每次对话都汇报该次 token 消耗”的要求；默认后续回复不再附 token in/out，除非用户再次明确要求恢复。
17) 节流落地规则（不降质）：固定提示前缀顺序以提高缓存命中；只注入必要上下文；复杂任务用子代理，简单任务低thinking。
18) 复述压缩规则：状态汇报优先“结论+证据路径+下一步”，避免重复粘贴长日志；长日志改摘要+命令可复现。
19) self-improving-agent 策略：仅部分启用（不全局常开）。
   - 启用：代码修复（首轮失败/跨文件）、多步骤交付（>3步、跨工具、有产物）
   - 禁用：短问答、秒回场景、强可控一步到位场景
   - 护栏：条件触发 + 最多1轮自改进 + token/时延阈值停机 + 超限降级 baseline
20) GUI 迭代提交规范（主线程+子线程统一）：每次 GUI 迭代必须使用固定提交模板 `type(scope): summary`；提交前完成最小检查（`git status`、关键功能自检、变更文件清单确认）；提交后必须输出简报（变更点/风险/回滚点/产物路径）；严禁提交环境噪音文件（cache/log/dist 中间产物等）；main session 与 all subagents 必须执行同一规则。
21) Discord 结构术语规范：
   - “子区” = Discord 线程（Thread），用于短期事项/一次性问题；通常挂在某个频道下，处理完通常不再保留。
   - “频道” = Discord 频道（Channel），用于长期事项/持续跟进。
   - “类别” = Discord 类别（Category），用于不同大项目/复杂事项的高层级容器，其下承载多个频道。
   执行时必须先按“短期/长期/项目级复杂度”判断，再选择创建子区、频道或类别，避免误建结构。

## Workflow
1) 用户新增/修改规则 → 追加到 memory/YYYY-MM-DD.md。
2) 更新本技能“Current Rules Snapshot”。
3) git commit + push（私有仓库）。
4) 回报“已归档并推送”。

## Guardrails
- 规则冲突时以用户最新指令为准。
- 不删除历史规则，改用追加与标注替代。
