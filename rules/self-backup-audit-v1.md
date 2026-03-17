---
id: rule-self-backup-audit
type: skill-detail
priority: medium
scope: [backup, audit, maintenance, drift]
description: "自我规则定期备份与漂移巡检方案，每3天执行一次一致性检查"
---

# 自我规则定期备份与巡检方案 v1（轻量）

目标：在“事件驱动备份”之外，补一个低维护的定期一致性检查，防止规则漂移与入口过时。

## 1) 巡检对象（固定最小集）

- 规则入口与导航
  - `AGENTS.md`
  - `rules/INDEX.md`
  - `SYSTEM_BOOTSTRAP.md`
- 规则主源与历史
  - `skills/user-preferences/SKILL.md`（SSOT）
  - `skills/rule-archive-lite/SKILL.md`（快照）
- 留痕与心跳
  - `HEARTBEAT.md`
  - `memory/YYYY-MM-DD.md`（本次巡检记录）

## 2) 触发频率

- 默认：**每 3 天一次**。
- 若近期发生规则集中变更（>3 处文件改动），可提前触发一次。

## 3) 巡检内容（10 分钟内完成）

1. **漂移检查**
   - `user-preferences` 与 `rules/INDEX` 的优先级、关键词、路由描述是否一致。
   - `SYSTEM_BOOTSTRAP` 的入口顺序/常量是否仍与当前规则一致。
2. **归档检查**
   - 最近一轮硬规则变更是否同时留痕到：
     - `skills/rule-archive-lite/SKILL.md`
     - `memory/YYYY-MM-DD.md`
3. **备份/提交检查**
   - `git status --short` 看是否有规则相关未提交改动。
   - 有必要时执行：`git add`（仅相关文件）→ `git commit` → `git push`。
4. **bootstrap/index 过时检查**
   - 若发现入口文档仍引用旧流程或旧常量，做最小修正（只改关键句，不重写大段）。

## 4) 输出与留痕（必须）

每次巡检在当日 `memory/YYYY-MM-DD.md` 追加一条：

- 时间
- 巡检范围
- 结果：`一致 / 发现漂移`
- 处理动作：`无需改动` 或 `已修正文件列表`
- Git 状态：`无改动` 或 `已提交 <commit-hash>`

建议模板：

```md
- [Rule Audit v1 | YYYY-MM-DD HH:mm] 检查 AGENTS/rules INDEX/user-preferences/rule-archive/SYSTEM_BOOTSTRAP/HEARTBEAT；结论：一致（或：发现漂移并已修正 X/Y）；Git：无改动（或：已提交 <hash> 并 push）。
```

## 5) 失败/异常处理（轻量）

- **读文件失败/冲突不清**：先记入 memory 为 `巡检中断`，下一轮补检；不做猜测性大改。
- **git push 失败**：
  1) 保留本地 commit；
  2) 在 memory 标注失败原因；
  3) 下一次 heartbeat 或手动窗口重试 push。
- **发现高风险不一致**（例如优先级冲突导致执行歧义）：
  - 只做“止血级”最小修复（改索引/入口一句话），并在 memory 标注“需主进程确认后再扩展修订”。

## 6) 边界

- 不引入 cron/守护进程/复杂脚本。
- 不做重型自动化，仅保留人工可执行的最小流程。
- 与现有事件驱动备份并行：事件驱动仍是主路径，定期巡检是兜底网。
