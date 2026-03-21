# Project Bootstrap - Quick Reference Card

## 🚀 最快上手方式

在 Discord 中直接说：

```
@OpenClaw 新coding项目：优化GPR GUI性能，在#gpr-gui，高优先级
```

## 📋 完整参数调用

```
@OpenClaw 使用 project-bootstrap skill 启动项目：
- project_name: gpr-gui-optimization
- project_type: coding
- channel_id: 1478098802937303100
- goal: Optimize GPR GUI rendering performance
- priority: high
```

## 🔄 推荐工作流程（Thread模式）

```
[Step 1] 创建 Thread
@OpenClaw 为这个任务创建一个子分区：优化 GPR GUI 性能

[Step 2] 在 Thread 中启动项目
@OpenClaw 使用 project-bootstrap skill 启动项目：
- project_name: gpr-gui-perf-opt
- project_type: coding
- channel_id: 1478098802937303100
- goal: Optimize GPR GUI rendering performance
- priority: high

[Step 3] 确认启动
确认，启动 coder
```

## 📊 project_type 选择指南

| 项目类型 | 说明 | 子代理流水线 |
|---------|------|-------------|
| coding | 纯编码任务 | coder → reviewer |
| research | 调研/文献 | researcher → coder → reviewer |
| review | 代码审查 | reviewer → researcher |
| mixed | 综合项目 | researcher → coder → reviewer |

## 🆔 常用 Channel ID

| 频道 | Channel ID |
|------|-----------|
| #gpr-gui | 1478098802937303100 |
| #multi-agent | 1477202149728587952 |
| #日常 | 1476983838994600109 |

## ⚡ 快捷模板

**编码项目：**
```
@OpenClaw 新coding项目：实现XXX功能，在#gpr-gui，高优先级
```

**研究项目：**
```
@OpenClaw 新research项目：调研XXX算法，在#日常，普通优先级
```

**审查项目：**
```
@OpenClaw 新review项目：审查XXX模块代码，在#gpr-gui，高优先级
```

**混合项目：**
```
@OpenClaw 新mixed项目：研究并实现XXX，在#gpr-gui，高优先级
```

## ✅ OpenClaw 响应流程

1. 生成 EDL 格式启动报告
2. 等待你确认
3. 确认后 dispatch 子代理
4. 子代理在指定频道/thread 中工作

## 📝 记忆保存

项目启动后，OpenClaw 会自动记录到：
`/mnt/e/Openclaw/.openclaw/workspace/memory/YYYY-MM-DD.md`
