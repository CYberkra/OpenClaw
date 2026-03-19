# 使用示例库

> 典型任务完整示例，从输入到输出的完整流程

---

## 示例 1：创建新项目并初始化

**场景**：开始一个新的 GPR 优化项目

**用户输入**：
```
创建个子分区做 GPR GUI 性能优化
```

**执行流程**：
1. `auto-project-launcher` 识别意图
2. 创建 Discord Thread "GPR GUI性能优化"
3. `project-bootstrap` 生成 EDL 报告
4. 等待用户确认后 dispatch `subagent-manager`
5. `subagent-manager` 派 `opencode` 执行代码优化
6. `reviewer` 复核代码质量
7. 生成报告并推送 GitHub

**输出**：
```markdown
EDL-ID: 20260319-gpr-gui-perf-bootstrap
Goal: GPR GUI 性能优化
Subagents: coder → reviewer
Result: 2-phase project initialized
```

---

## 示例 2：代码审查

**场景**：审查一个 Python 模块的 PR

**用户输入**：
```
审查这个 PR 的代码质量
```

**执行流程**：
1. 读取 `code-review` skill
2. 三阶段检查：
   - Pass 1: 架构审查（2分钟）
   - Pass 2: 详细代码审查（主要时间）
   - Pass 3: 边界情况和安全审查（5分钟）
3. 按严重级别分类评论：
   - [CRITICAL] 安全问题
   - [MAJOR] 逻辑错误
   - [MINOR] 改进建议
   - [NIT] 风格问题

**输出**：
```markdown
## 代码审查报告

### 严重级别统计
- CRITICAL: 0
- MAJOR: 1
- MINOR: 3
- NIT: 2

### 主要问题
[MAJOR] line 42: SQL 注入风险，建议使用参数化查询

### 改进建议
[MINOR] 添加边界值测试用例
```

---

## 示例 3：多步骤调研任务

**场景**：调研 SVD 背景抑制算法并给出实现建议

**用户输入**：
```
调研 SVD 背景抑制算法，比较不同实现方案
```

**执行流程**：
1. `subagent-manager` 拆解任务：
   - Step 1: `researcher` 文献调研
   - Step 2: `coder` 实现原型
   - Step 3: `reviewer` 验证结果
2. 每步完成后汇报进度
3. 汇总最终报告

**输出**：
```markdown
## SVD 背景抑制算法调研报告

### 方法对比
| 方法 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 标准 SVD | 稳定 | 计算量大 | 小数据集 |
| 随机 SVD | 快速 | 近似结果 | 大数据集 |
| 增量 SVD | 内存友好 | 实现复杂 | 流式数据 |

### 推荐方案
随机 SVD（sklearn.extmath.randomized_svd）
理由：GPR 数据量大，需要快速处理

### 代码示例
```python
from sklearn.extmath import randomized_svd
U, s, Vt = randomized_svd(data, n_components=10)
```
```

---

## 示例 4：文档转换与总结

**场景**：将 PDF 论文转换为 Markdown 并总结

**用户输入**：
```
把这个 PDF 转成 Markdown 并总结核心观点
```

**执行流程**：
1. `markdown-converter` 转换 PDF → Markdown
2. `summarize` 提取核心观点
3. 保存到 `reports/` 目录

**输出**：
```markdown
## 论文总结: [标题]

### 核心贡献
1. 提出新的 GPR 背景抑制方法
2. 实验验证在 X 数据集上提升 Y%

### 关键方法
- 使用 Hankel 矩阵 + SVD
- 自动确定奇异值阈值

### 对我们的启发
可以应用到当前 GPR_GUI 项目中...

### 原始文档
[链接到转换后的 Markdown]
```

---

## 示例 5：GitHub Issue 修复

**场景**：自动发现并修复仓库中的 bug

**用户输入**：
```
修复这个仓库的 open issues
```

**执行流程**：
1. `github-issue-resolver` 加载 5 层护栏
2. `recommend.py` 评分并推荐 issue
3. 用户选择 issue
4. 锁定 issue（防止并发）
5. Clone 仓库 → 创建分支 → 修复 → 测试
6. Draft PR 等待用户审查

**输出**：
```markdown
## Issue 修复报告

### 修复的问题
- Issue #123: 内存泄漏问题

### 变更内容
- src/memory_manager.py: 添加析构函数释放资源
- tests/test_memory.py: 添加回归测试

### 测试状态
✅ 所有测试通过

### PR
Draft PR: https://github.com/.../pull/456
```

---

## 示例 6：自动化报告生成

**场景**：生成周报总结本周工作

**用户输入**：
```
生成本周工作周报
```

**执行流程**：
1. 查询本周 memory 文件
2. 统计完成的任务
3. 汇总代码提交、文档更新
4. 生成周报文档

**输出**：
```markdown
# 周报 2026-03-17 至 2026-03-19

## 完成任务
- ✅ GPR GUI 性能优化（3项改进）
- ✅ 架构优化 P1-P5（5项优化）
- ✅ 文档完善（新增3个文档）

## 代码提交
- 12 commits pushed to GitHub
- 主要变更：规则系统优化、Skill 精简

## 下周计划
- 继续 GUI 开发
- 测试新版本性能
```

---

## 快速参考

| 任务类型 | 主要 Skill | 预计时间 |
|---------|-----------|---------|
| 新项目启动 | auto-project-launcher | 2-5 分钟 |
| 代码审查 | code-review | 10-30 分钟 |
| 调研任务 | subagent-manager | 30-60 分钟 |
| 文档转换 | markdown-converter | 1-2 分钟 |
| Issue 修复 | github-issue-resolver | 20-60 分钟 |
| 报告生成 | documentation | 5-10 分钟 |

---

*更多示例持续添加中...*
