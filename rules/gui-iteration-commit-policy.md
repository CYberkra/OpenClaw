# GUI Iteration Commit Policy

## 目的
规范每次 GUI 迭代更新的提交流程，确保提交质量、可回滚性与跨线程一致执行。

## 适用范围
- main session（主线程）
- all subagents（全部子线程）

以上范围必须执行同一规则，不得因执行主体不同而放宽。

## 提交流程（Pre-check -> Commit -> Post-report）

### 1) Pre-check
在提交前必须完成以下最小检查：
1. `git status`：确认仅包含本次 GUI 迭代相关改动。
2. 关键功能自检：至少覆盖本次改动涉及的核心 GUI 交互路径。
3. 变更文件清单：逐项确认将被提交的文件，排除噪音文件。

### 2) Commit
必须使用固定模板：

`type(scope): summary`

推荐用于 GUI 迭代的 type 示例：
- `feat(gui): add ...`
- `fix(gui): resolve ...`
- `perf(gui): optimize ...`

### 3) Post-report
提交后必须输出简报，至少包含：
- 变更点（做了什么）
- 风险（潜在影响/已知限制）
- 回滚点（如何快速撤回）
- 产物路径（相关文件或构建产物位置）

## 禁止提交清单
严禁将下列环境噪音或中间产物混入提交（含同类目录/后缀）：
- cache / .cache
- log / logs / *.log
- dist / build 中间产物
- 临时文件（如 *.tmp、*.swp、系统自动生成缓存）

如确需纳入，应在简报中说明必要性并单独评审。

## 回滚策略
- 优先使用单提交回滚：`git revert <commit>`。
- 紧急场景可临时回退到上一稳定提交并记录原因。
- 回滚后必须补充一条简报，说明：触发原因、影响范围、后续修复计划。
