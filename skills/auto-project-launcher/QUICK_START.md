# Auto Project Launcher - 快速启动指南

## 🚀 立即可用的方案

由于完全自动化可能需要特定配置，以下是**立即可用**的方案：

---

## 方案A：两步法（推荐，最稳定）

### Step 1：在主频道创建 Thread

```
@OpenClaw 创建子分区做：优化 GPR GUI 性能
```

OpenClaw 会创建 Thread，然后你进入 Thread。

### Step 2：在 Thread 中快速启动

```
@OpenClaw 启动项目
```

或

```
@OpenClaw /boot
```

OpenClaw 会自动：
- 识别 Thread 主题
- 调用 project-bootstrap
- 生成 EDL 报告
- 等待你确认

---

## 方案B：一句话启动（使用 subagent-manager）

```
@OpenClaw 使用 subagent-manager 在子分区执行：优化 GPR GUI 性能，coder 负责实现，reviewer 负责检查
```

OpenClaw 会自动：
- 创建 Thread
- Dispatch 指定子代理
- 在 Thread 中开始工作

---

## 方案C：手动指定（最灵活）

### Step 1：创建 Thread

```
@OpenClaw 创建子分区：调研 SVD 背景抑制算法
```

### Step 2：指定参数启动

```
@OpenClaw 使用 project-bootstrap：
- type: mixed
- priority: high
- goal: Research and implement SVD background suppression
```

---

## 📋 实际对话示例

### 示例 1：编码项目

**你：**
```
@OpenClaw 创建子分区做：优化 GPR GUI 渲染性能
```

**OpenClaw：**
```
✅ 已创建子分区: "优化 GPR GUI 渲染性能"
```

**你（在 Thread 中）：**
```
@OpenClaw 启动项目
```

**OpenClaw：**
```
🚀 项目初始化

EDL-ID: 20260309-gpr-gui-perf-bootstrap
Goal: 优化 GPR GUI 渲染性能
Type: coding | Priority: normal
Subagents: coder → reviewer
Plan: 1) coder: 分析和优化性能瓶颈 2) reviewer: 验证改进效果
Next: 回复"确认"启动 coder
```

**你：**
```
确认
```

**OpenClaw：**
```
✅ 已启动 coder，Thread 内跟进
```

---

## 🎯 快捷短语速查

| 你想做的事 | 在主频道说 | 在 Thread 中说 |
|-----------|-----------|---------------|
| 创建 Thread | "创建子分区做：XXX" | - |
| 快速启动 | - | "启动项目" 或 "/boot" |
| 详细启动 | - | "使用 project-bootstrap：type=coding" |
| 一句话启动 | "使用 subagent-manager 在子分区执行：XXX" | - |

---

## 💡 进阶用法

### 指定子代理

```
@OpenClaw 启动项目，只要 coder
```

### 指定优先级

```
@OpenClaw 启动项目，高优先级
```

### 组合指令

```
@OpenClaw 启动项目：type=mixed，priority=high，只要 researcher 和 coder
```

---

## ⚠️ 注意事项

1. **Thread 创建后需要等待** OpenClaw 确认创建成功再发送第二条消息
2. **子代理启动需要确认**，符合你的"显式确认"规则
3. **项目记录会自动保存**到 memory 文件

---

## 🔧 如果要用完全自动化

如果想要完全自动化（一句话完成所有操作），需要：

1. 修改 `openclaw.json` 添加 trigger 配置
2. 或等待 OpenClaw 更新支持自动 thread 创建 + skill 调用

目前推荐**方案A（两步法）**，稳定可靠且符合你的工作流。
