# Auto Project Launcher - 设置指南

## 实现方案

由于 OpenClaw 的自动触发需要特定配置，提供以下三种实现方案：

---

## 方案1：关键词触发（推荐）

### 设置步骤

1. **在 openclaw.json 中添加 skill 配置**

```json
{
  "skills": {
    "entries": {
      "auto-project-launcher": {
        "enabled": true,
        "triggers": [
          "创建.*子分区.*做",
          "新建.*项目.*thread",
          "为这个.*创建.*thread",
          "开.*子分区.*处理"
        ]
      }
    }
  }
}
```

2. **重启 Gateway**

```bash
openclaw gateway restart
```

---

## 方案2：快捷指令模式（无需配置）

如果不修改配置，可以使用**固定短语**快速触发：

### 在主频道发送：

```
@OpenClaw /project 做GPR GUI性能优化
```

或

```
@OpenClaw /task 调研SVD背景抑制算法，紧急
```

### OpenClaw 会自动：

1. 识别 `/project` 或 `/task` 指令
2. 创建 Thread
3. 在 Thread 中调用 project-bootstrap

---

## 方案3：自然语言+显式指令

### 在主频道发送：

```
@OpenClaw 创建子分区并启动项目：优化GPR GUI性能
```

这会被识别为：
1. 创建 Thread
2. 自动调用 project-bootstrap

---

## 当前可用方案（立即可用）

由于方案1需要修改配置，目前**立即可用**的是：

### 使用 project-bootstrap + 手动创建 Thread

**Step 1：** 在主频道说：
```
@OpenClaw 创建子分区：优化GPR GUI性能
```

**Step 2：** 进入 Thread 后说：
```
@OpenClaw /bootstrap
```
或
```
@OpenClaw 初始化项目
```

### 优化后的快速流程

为了让这个流程更顺畅，创建一个**简化版 project-bootstrap**：

---

## 简化版使用方案

创建快捷指令 `/start` 或 `/boot`：

### 用户使用：

在 Thread 中发送：
```
@OpenClaw /start coding:优化GPR GUI性能
```

格式：
```
/start <type>:<goal>
```

### 示例：

```
/start coding:实现实时数据处理模块
/start research:调研FK滤波算法
/start review:检查agcGain模块
/start mixed:优化背景抑制算法并验证
```

---

## 推荐配置（需要添加到 openclaw.json）

```json
{
  "commands": {
    "shortcuts": {
      "/project": {
        "skill": "auto-project-launcher",
        "args": "auto-extract"
      },
      "/boot": {
        "skill": "project-bootstrap",
        "args": "from-context"
      }
    }
  }
}
```

---

## 当前最实用的方案

由于自动触发可能需要特定版本的 OpenClaw 支持，当前最实用的方案是：

### 两步法（已可用）

```
[主频道] @OpenClaw 创建子分区做：优化GPR GUI性能
                ↓
[OpenClaw 创建 Thread]
                ↓
[Thread 中] @OpenClaw 使用 project-bootstrap 启动项目
                ↓
[确认] 确认启动 coder
```

### 或者一步法（使用 subagent-manager）

```
[主频道] @OpenClaw 使用 subagent-manager 在子分区中执行：优化GPR GUI
```

---

## 需要确认的问题

要实现完全自动化（一句话创建 thread + 启动项目），需要确认：

1. **OpenClaw 版本**是否支持 skill 自动触发
2. 是否有**创建 thread 的权限**
3. 是否允许**自动 dispatch 子代理**（还是必须显式确认）

建议先测试手动两步法，确认 workflow 合适后再配置自动化。
