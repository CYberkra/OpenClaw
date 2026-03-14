# anti-patterns.md

精简版 self-improving 试运行（开始：2026-03-14）

记录高频错误模式，避免重复踩坑。

## Known Anti-Patterns
- 在 Discord 结构术语未完全确认前，擅自把“子区/频道/类别”映射成错误对象。
- 在未得到明确要求前，擅自扩建一整套频道/类别结构。
- 将短期事项错误做成长期结构，或将长期事项错误做成短期结构。
- 自动附带 token 消耗，尽管用户已明确取消。
- 在已有 memory/rule-archive 体系上再做重型重复注入，导致规则双轨和冲突。

## Trial Guardrail
- 只在用户明确纠错或明确声明“以后都这样”时写入 self-improving 文件。
