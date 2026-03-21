# Auto Project Launcher - 实现说明

## 配置完成状态

### ✅ 已完成

1. **openclaw.json 配置更新**
   - 添加了 project-bootstrap skill 的自动检测配置
   - 配置了 4 个触发关键词模式

2. **SYSTEM_BOOTSTRAP.md 更新**
   - 添加了自动化规则文档
   - 记录配置更新时间

3. **trigger.sh 创建**
   - 参数提取脚本
   - 项目类型推断逻辑
   - 优先级推断逻辑

### 📋 触发关键词

当用户在主频道发送包含以下模式的消息时，会自动触发：

- `创建.*子分区.*做` - 例："创建子分区做性能优化"
- `新建.*子分区.*做` - 例："新建子分区做算法调研"  
- `开.*子分区.*做` - 例："开个子分区做代码审查"
- `为.*创建.*子分区` - 例："为这个任务创建子分区"

### 🔄 自动执行流程

```
[用户消息匹配触发模式]
         ↓
[OpenClaw 识别意图]
         ↓
[提取项目参数]
  - project_name: 从消息提取
  - project_type: 自动推断 (coding/research/review/mixed)
  - priority: 自动推断 (high/normal)
         ↓
[创建 Discord Thread]
         ↓
[在 Thread 中调用 project-bootstrap]
         ↓
[生成 EDL 报告]
         ↓
[等待用户确认]
         ↓
[用户回复"确认"后 dispatch 子代理]
```

### ⚠️ 重要说明

**配置生效方式：**

由于 OpenClaw 的自动触发机制可能需要特定版本支持，提供两种生效方式：

#### 方式1：重启 Gateway（推荐）

```bash
openclaw gateway restart
```

重启后配置完全生效。

#### 方式2：热加载（如支持）

```bash
openclaw config reload
```

如果 OpenClaw 支持热加载配置。

### 🧪 测试方法

配置生效后，在 Discord 主频道发送：

```
@OpenClaw 创建子分区做：测试自动项目启动
```

预期行为：
1. OpenClaw 创建 Thread
2. 在 Thread 中自动生成项目报告
3. 等待你回复"确认"
4. 确认后自动 dispatch 子代理

### 🔧 故障排除

**如果自动触发不工作：**

1. 检查配置是否正确加载：
   ```bash
   openclaw config get skills.entries.project-bootstrap
   ```

2. 查看日志：
   ```bash
   tail -f /mnt/e/Openclaw/.openclaw/logs/openclaw.log
   ```

3. 备用方案（手动两步法）：
   - "创建子分区做：XXX"
   - 进入 Thread 后："启动项目"

**如果误触发：**

可以在消息中添加"不要启动"来跳过：
```
@OpenClaw 创建子分区做：测试（不要启动）
```

### 📝 使用示例

#### 示例1：编码项目

**你：**
```
@OpenClaw 创建子分区做：优化 GPR GUI 渲染性能
```

**OpenClaw 自动：**
1. 创建 Thread: "优化 GPR GUI 渲染性能"
2. 在 Thread 中输出：
```
🚀 项目自动初始化

EDL-ID: 20260309-gpr-gui-perf-bootstrap
Goal: 优化 GPR GUI 渲染性能
Type: coding | Priority: normal
Subagents: coder → reviewer
Plan: 1) coder: 分析和优化性能瓶颈 2) reviewer: 验证改进效果
Next: 回复"确认"启动
```

**你：**
```
确认
```

**OpenClaw：**
```
✅ 已启动 coder agent
```

#### 示例2：紧急研究项目

**你：**
```
@OpenClaw 新建子分区做：紧急调研 SVD 算法
```

**OpenClaw 自动：**
```
🚀 项目自动初始化（紧急）

EDL-ID: 20260309-svd-algo-research-bootstrap
Goal: 紧急调研 SVD 算法
Type: research | Priority: HIGH
Subagents: researcher → coder → reviewer
Plan: 1) researcher: 文献调研 2) coder: 原型实现 3) reviewer: 验证
Next: 回复"确认"启动
```

### 🛡️ 安全机制

1. **不会自动 dispatch 子代理** - 始终等待显式确认
2. **可取消** - 回复"取消"即可中止
3. **可修改** - 回复"修改：XXX"可调整参数
4. **日志记录** - 所有操作记录到 memory 文件

### 🔄 回滚方法

如果配置有问题，可以恢复备份：

```bash
# 恢复配置
cp /mnt/e/Openclaw/.openclaw/openclaw.json.bak.auto.XXXX /mnt/e/Openclaw/.openclaw/openclaw.json

# 重启 Gateway
openclaw gateway restart
```
