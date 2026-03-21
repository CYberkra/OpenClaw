# Auto Project Launcher

自动识别项目启动意图，创建 Thread 并初始化项目。

## Trigger Patterns

当用户消息匹配以下模式时自动触发：

```regex
(创建|新建|开).{0,5}(子分区|thread|频道).{0,10}(做|处理|跟进|跟踪|执行)
(创建|新建|开).{0,5}(项目|任务).{0,10}(在子分区|在thread|在thread里)
为这个.*创建.{0,5}(子分区|thread)
新建.*项目.*(在|去).{0,5}(thread|子分区)
```

## Workflow

### Step 1: 意图识别

从用户消息中提取：
- 项目名称（任务描述）
- 项目类型（推断）
- 优先级（推断）

### Step 2: 创建 Thread

```
创建 Discord Thread：
- 名称：从任务描述提取（≤100字符）
- 频道：当前频道
- 初始消息：任务描述 + 自动生成的项目信息
```

### Step 3: 在 Thread 中执行 project-bootstrap

自动调用 project-bootstrap skill 的逻辑：
1. 执行 qmd search 检索相关记忆
2. 确定项目类型和子代理
3. 生成 EDL 格式报告
4. 投递到 Thread

### Step 4: 等待确认

在 Thread 中等待用户确认后才 dispatch 子代理。

## Input Extraction

从自然语言中提取参数：

```yaml
项目名称提取：
  模式1: "创建子分区做XXX" → project_name: xxx, goal: XXX
  模式2: "新建项目：XXX" → project_name: xxx, goal: XXX
  模式3: "为XXX创建thread" → project_name: xxx, goal: XXX

项目类型推断：
  - 包含"优化"|"实现"|"开发"|"代码" → coding
  - 包含"调研"|"研究"|"文献"|"综述" → research
  - 包含"审查"|"检查"|"评估" → review
  - 混合特征 → mixed

优先级推断：
  - 包含"紧急"|"马上"|"立刻"|"高优先级" → high
  - 包含"普通"|"一般"|"正常" → normal
  - 其他 → normal
```

## Output Format

在 Thread 中输出：

```markdown
🚀 项目自动初始化完成

EDL-ID: <timestamp>-<project_name>-bootstrap
Goal: <extracted_goal>
Inputs: project=<name>, type=<type>, channel=<channel_id>
Context: <3-line summary from qmd search>
Subagents: <agent1> → <agent2> → <agent3>
Plan: 1) <agent1>: <task> 2) <agent2>: <task> 3) <agent3>: <task>
Result: <N>-phase project initialized in this thread
Risks: <blockers>
Next: Reply "确认启动" or "修改：<你的调整>"
```

## Examples

### Example 1: 简单编码任务

**用户输入：**
```
@OpenClaw 创建个子分区做GPR GUI性能优化
```

**系统自动执行：**
1. 创建 Thread: "GPR GUI性能优化"
2. 在 Thread 中输出：

```markdown
🚀 项目自动初始化完成

EDL-ID: 20260309-gpr-gui-perf-bootstrap
Goal: Optimize GPR GUI performance
Inputs: project=gpr-gui-perf, type=coding, channel=1478098802937303100
Context: Qt packaging skill available; GUI optimization methods documented
Subagents: coder → reviewer
Plan: 1) coder: Profile and optimize performance bottlenecks 2) reviewer: Validate improvements
Result: 2-phase coding project initialized in this thread
Risks: Qt deps may require cross-platform testing
Next: Reply "确认启动" or "修改：<你的调整>"
```

### Example 2: 研究型任务

**用户输入：**
```
@OpenClaw 新建一个子分区调研SVD背景抑制算法，比较紧急
```

**系统自动执行：**
1. 创建 Thread: "SVD背景抑制算法调研（紧急）"
2. 在 Thread 中输出：

```markdown
🚀 项目自动初始化完成

EDL-ID: 20260309-svd-bg-research-bootstrap
Goal: Research SVD background suppression algorithms
Inputs: project=svd-bg-research, type=mixed, priority=high, channel=...
Context: SVD methods referenced in memory; background suppression skills available
Subagents: researcher → coder → reviewer
Plan: 1) researcher: Literature review and method comparison 2) coder: Prototype implementation 3) reviewer: Validate against requirements
Result: 3-phase mixed project initialized (HIGH priority)
Risks: External paper access may need VPN
Next: Reply "确认启动" or "修改：<你的调整>"
```

### Example 3: 代码审查任务

**用户输入：**
```
@OpenClaw 为这个代码审查创建一个thread跟进
```

**系统自动执行：**
1. 创建 Thread: "代码审查跟进"
2. 在 Thread 中输出：

```markdown
🚀 项目自动初始化完成

EDL-ID: 20260309-code-review-bootstrap
Goal: Code review and validation
Inputs: project=code-review, type=review, channel=...
Context: Reviewer agent available; code quality guidelines in memory
Subagents: reviewer → researcher
Plan: 1) reviewer: Comprehensive code review 2) researcher: Cross-reference best practices
Result: 2-phase review project initialized
Risks: Review scope not fully specified
Next: Reply "确认启动" or "修改：<你的调整>"
```

## User Confirmation Flow

用户在 Thread 中的回复选项：

| 回复 | 动作 |
|-----|------|
| "确认启动" / "开始" / "执行" | Dispatch 第一个子代理 |
| "修改：XXX" | 更新项目参数，重新生成报告 |
| "加 researcher" / "去掉 reviewer" | 调整子代理配置 |
| "优先级改为 high" | 调整优先级 |
| "取消" | 取消项目，关闭 thread |

## Implementation Notes

- 始终在主频道响应 "正在创建子分区..."
- 所有详细输出在 Thread 中完成
- 符合 EDL 规则（≤8行汇报，≤30行证据）
- 自动记录到 memory 文件
