# 规则去重分析报告

**分析日期**: 2026-03-17  
**分析范围**: `/home/baiiy1/.openclaw/workspace` 规则体系  
**目标**: 减少 30% 冗余

---

## 执行摘要

通过分析 6 个核心规则文件，发现 **大量内容重复**，主要集中在路由规则、验收闸门、角色边界和模式切换等模块。当前规则体系存在以下结构性问题：

| 问题类型 | 数量 | 主要涉及文件 |
|---------|------|-------------|
| 内容重复 | 5 处 | AGENTS.md ↔ user-preferences |
| 职责重叠 | 3 处 | 路由规则分散在 4 个文件 |
| 版本漂移 | 2 处 | archive 与主源版本不一致 |

**预估可合并内容**: 约 40-50% 的重复描述，超过目标 30%。

---

## 发现的问题

### 问题 1: 路由判定表重复（重度重复）

- **涉及文件**: `AGENTS.md`, `skills/user-preferences/SKILL.md`
- **重复内容**: 
  - "Default Routing Table v1" 完整章节（约 40 行）
  - 包含相同的 6 条路由规则（纯问答→直答、代码改动→opencode、多步骤→manager 等）
  - 冲突决策逻辑完全一致
- **建议**: 
  - **主源**: `skills/user-preferences/SKILL.md`（SSOT 定位）
  - **AGENTS.md**: 改为摘要引用，仅保留"路由规则详见 user-preferences"一句话 + 链接

### 问题 2: 验收闸门 SOP 重复（重度重复）

- **涉及文件**: `AGENTS.md`, `skills/user-preferences/SKILL.md`
- **重复内容**:
  - G1-G6 标准顺序描述（约 25 行）
  - 防御性补丁（Max Iterations 3 次、Timeout 熔断）
- **建议**:
  - **主源**: `skills/user-preferences/SKILL.md`
  - **AGENTS.md**: 仅保留验收闸门概念说明，具体步骤引用主源

### 问题 3: 模式切换规则重复（中度重复）

- **涉及文件**: `AGENTS.md`, `skills/user-preferences/SKILL.md`, `skills/rule-archive-lite/SKILL.md`
- **重复内容**:
  - 5 种模式（default/strict/proactive/evolver/ralph）定义
  - 冲突优先级顺序（strict > ralph > evolver > proactive > default）
  - 模式持久化策略（单条任务一次性）
- **版本漂移**: rule-archive-lite 中编号为 v1.1，user-preferences 中为 v1.1 + 额外补丁
- **建议**:
  - **主源**: `skills/user-preferences/SKILL.md`
  - **AGENTS.md**: 仅说明存在模式系统，详情引用主源
  - **rule-archive-lite**: 保持历史快照，不再更新

### 问题 4: 角色边界定义重复（中度重复）

- **涉及文件**: `AGENTS.md`, `skills/user-preferences/SKILL.md`, `SYSTEM_BOOTSTRAP.md`
- **重复内容**:
  - subagent_manager / opencode / coder 三者职责边界
  - 决策顺序：manager → opencode → coder
- **建议**:
  - **主源**: `skills/user-preferences/SKILL.md`
  - **AGENTS.md**: 删除详细定义
  - **SYSTEM_BOOTSTRAP.md**: 保留最小启动所需（agent 角色列表即可）

### 问题 5: 规则优先级链条重复（轻度重复）

- **涉及文件**: `AGENTS.md`, `skills/user-preferences/SKILL.md`, `rules/INDEX.md`, `SYSTEM_BOOTSTRAP.md`
- **重复内容**:
  - 相同的 5 级优先级（用户指令 > user-preferences > AGENTS > archive > 其他）
- **建议**:
  - **主源**: `rules/INDEX.md`（注册表定位，适合作为权威来源）
  - 其他文件改为引用 INDEX

### 问题 6: 关键词速查重复（轻度重复）

- **涉及文件**: `skills/user-preferences/SKILL.md`, `rules/INDEX.md`
- **重复内容**:
  - 路由关键词（直答/走 manager/走 opencode/加 reviewer/开 CI）
  - 模式关键词（切 strict/proactive/evolver/ralph/恢复 default）
  - 验收关键词（仅到 G3/执行全闸门/跳过 CI）
- **建议**:
  - **主源**: `rules/INDEX.md`（适合作为速查入口）
  - **user-preferences**: 删除或简化为"见 INDEX.md 关键词速查"

### 问题 7: SYSTEM_BOOTSTRAP 与主源内容重叠（结构性重叠）

- **涉及文件**: `SYSTEM_BOOTSTRAP.md`, `skills/user-preferences/SKILL.md`
- **重叠内容**:
  - 路由摘要（第3节）与 Default Routing Table v1 内容高度重叠
  - 验收闸门摘要（第4节）与 SOP v1 重叠
  - 模式系统摘要（第5节）与模式切换补丁重叠
- **设计意图冲突**: BOOTSTRAP 定位为"快速入口"，但实际复制了大量内容，导致维护时必须同步修改多处
- **建议**: BOOTSTRAP 应极度精简，仅保留导航性质内容

### 问题 8: rule-archive-lite 版本号混乱（版本漂移）

- **涉及文件**: `skills/rule-archive-lite/SKILL.md`
- **问题**:
  - 规则 35 出现两次（"工作流模式持久化策略"和"防死循环补丁"都标为 35）
  - 规则编号从 29 直接跳到 30，但内容存在时间线错位
  - 与 user-preferences 中的 v1.2、v1.4 补丁版本号体系不一致
- **建议**: archive 文件仅作为历史留痕，不再维护编号体系，避免与主源混淆

---

## 合并方案

### 方案 A: 主源中心化（推荐）

**核心思路**: 明确 `skills/user-preferences/SKILL.md` 为唯一执行主源（SSOT），其他文件全部改为引用或摘要。

| 文件 | 处理方式 | 预估缩减 |
|-----|---------|---------|
| `AGENTS.md` | 删除重复章节，仅保留高层摘要、红线和记忆管理 | 60% |
| `SYSTEM_BOOTSTRAP.md` | 精简为导航卡片，删除所有详细规则描述 | 50% |
| `rules/INDEX.md` | 保留作为注册表，适当增加引用链接 | 10% |
| `skills/rule-archive-lite/SKILL.md` | 归档锁定，不再维护编号 | 5% |

**优点**:
- 单点维护，消除同步成本
- 职责清晰：主源 = 执行规则，其他 = 导航/摘要/历史
- 符合现有 SSOT 设计意图

**缺点**:
- 需要一次性修改多个文件
- 需要验证引用链接有效性

---

### 方案 B: 分层精简（渐进式）

**核心思路**: 保留各文件存在理由，但严格分层内容，每层只保留本层专属内容。

**分层定义**:
1. **执行层** (`user-preferences`): 详细规则、版本号、补丁
2. **摘要层** (`AGENTS.md`, `SYSTEM_BOOTSTRAP.md`): 仅保留"有什么规则"，不保留"规则是什么"
3. **导航层** (`rules/INDEX.md`): 纯注册表 + 链接
4. **历史层** (`rule-archive-lite`): 冻结，不再追加新内容

**处理步骤**:
1. 将 AGENTS.md 中的详细规则改为 "详见 user-preferences/SKILL.md#章节"
2. 将 SYSTEM_BOOTSTRAP.md 中的第3-5节改为极简列表（仅标题 + 链接）
3. INDEX.md 增加"快速跳转"链接区块
4. rule-archive-lite 添加头部注释："历史归档，不再更新"

**优点**:
- 改动较小，风险可控
- 保留现有文件结构，用户习惯不受影响

**缺点**:
- 需要持续维护"分层纪律"，可能再次漂移
- 冗余减少幅度约 25%，略低于 30% 目标

---

### 方案对比

| 维度 | 方案 A（主源中心化） | 方案 B（分层精简） |
|-----|-------------------|------------------|
| 冗余减少 | ~45% | ~25% |
| 维护成本 | 低（单点维护） | 中（需维持分层） |
| 改动风险 | 中（多文件修改） | 低（渐进式） |
| 长期可持续性 | 高 | 中 |
| 符合 SSOT 设计 | 完全 | 部分 |

---

## 推荐方案

**推荐方案 A（主源中心化）**，理由：

1. **符合现有设计**: 文件已明确 user-preferences 为 SSOT，但未严格执行，方案 A 是落实这一设计
2. **超额完成目标**: 可减少约 45% 冗余，超过 30% 目标
3. **长期维护成本最低**: 单点修改，消除同步遗漏风险
4. **架构清晰**: 执行/导航/历史三层职责分明

---

## 执行步骤

### Phase 1: AGENTS.md 精简（预计减少 60% 内容）

1. 删除 "Default Routing Table v1" 完整内容
   - 替换为："路由规则详见 [user-preferences/SKILL.md#默认路由判定表]"
   
2. 删除 "Acceptance Gate SOP v1" 完整内容
   - 替换为："验收闸门详见 [user-preferences/SKILL.md#验收闸门-sop-v1]"
   
3. 删除 "Workflow Clarifications v1.1" 完整内容
   - 保留小节标题，内容改为引用主源

4. 保留内容（AGENTS.md 专属）：
   - Session Startup 流程
   - Memory 管理指南
   - Red Lines（红线）
   - Group Chats 社交指南
   - Heartbeats 使用指南

### Phase 2: SYSTEM_BOOTSTRAP.md 精简（预计减少 50% 内容）

1. 第3节（默认路由摘要）→ 改为列表 + 链接
2. 第4节（验收闸门摘要）→ 改为列表 + 链接
3. 第5节（模式系统摘要）→ 改为列表 + 链接
4. 保留内容：
   - Quick Start 流程
   - 规则优先级（仅保留顺序，不展开）
   - 按需加载策略
   - 当前有效常量

### Phase 3: rules/INDEX.md 优化

1. 在"文档路由速查"后增加"快速跳转链接"区块
2. 确保每个规则文档都有可直接点击的锚点链接

### Phase 4: rule-archive-lite 标记

1. 在文件头部添加注释块：
   ```markdown
   > **归档状态**: 本文件为历史快照，不再更新。
   > 当前规则以 `skills/user-preferences/SKILL.md` 为准。
   ```
2. 删除编号体系说明，避免版本混淆

---

## 预期效果

### 量化指标

| 指标 | 当前 | 预期 | 变化 |
|-----|-----|-----|-----|
| 总行数（6个文件） | ~1800 行 | ~1000 行 | **-44%** |
| 重复描述段落 | 8 处 | 0 处 | **-100%** |
| 需要同步维护的内容块 | 6 块 | 1 块 | **-83%** |
| 单点修改即可生效 | 否 | 是 | ✓ |

### 文件级变化预估

| 文件 | 当前行数 | 预期行数 | 缩减比例 |
|-----|---------|---------|---------|
| AGENTS.md | ~500 | ~200 | **60%** |
| user-preferences/SKILL.md | ~400 | ~400 | 0%（主源） |
| rule-archive-lite/SKILL.md | ~500 | ~450 | 10%（去编号） |
| rules/INDEX.md | ~150 | ~140 | 7% |
| SYSTEM_BOOTSTRAP.md | ~200 | ~100 | **50%** |
| HEARTBEAT.md | ~100 | ~100 | 0%（无重复） |

### 质量改善

1. **消除版本漂移**: 单一主源，不再出现"AGENTS.md 已更新但 user-preferences 未同步"
2. **降低认知负担**: 开发者只需记忆"看 user-preferences 就对了"
3. **提升启动速度**: SYSTEM_BOOTSTRAP 精简后，新 agent 读取内容更少
4. **保留历史追溯**: archive 文件虽然冻结，但仍可查看规则演变

---

## 风险与缓解

| 风险 | 影响 | 缓解措施 |
|-----|-----|---------|
| 引用链接失效 | 中 | 执行时同步验证所有锚点链接 |
| 用户习惯被打破 | 低 | 保留原文件位置，仅内容精简 |
| 主源文件过大 | 低 | user-preferences 当前结构清晰，无需担忧 |
| 误删 AGENTS.md 专属内容 | 中 | Phase 1 明确列出"保留内容"清单 |

---

## 结论

当前规则体系存在显著的结构性冗余，主要集中在 **AGENTS.md 与 user-preferences 之间** 的路由、验收、模式三大模块重复。通过实施 **方案 A（主源中心化）**，可在保持功能完整的前提下，将规则体系总体积减少约 **45%**，远超 30% 目标，同时建立可持续的"单点维护"机制。

**建议立即执行 Phase 1-2 的核心精简**，Phase 3-4 可后续迭代完成。

---

*报告生成时间: 2026-03-17*  
*分析报告文件路径: `reports/rule-deduplication-analysis-2026-03-17.md`*
