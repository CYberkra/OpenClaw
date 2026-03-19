# Skill 精简与合并方案

> 生成时间：2026-03-19
> 当前 Skill 数量：34 → 目标：25-28

---

## 一、重叠 Skill 分组与默认选择

### 1. TTS (文本转语音)

| Skill | 技术 | 优点 | 缺点 | 建议 |
|-------|------|------|------|------|
| **openai-tts** | OpenAI API | 音质好，多种声音 | 需要 API key，按量付费 | ⭐ **默认首选** |
| **edge-tts** | 微软 Edge | 免费，无需 API key | 依赖微软服务 | 备用 |

**决策规则**：
- 默认使用 `openai-tts`
- 当 OpenAI API 不可用时，降级到 `edge-tts`

---

### 2. STT (语音转文字)

| Skill | 技术 | 优点 | 缺点 | 建议 |
|-------|------|------|------|------|
| **openai-whisper** | 本地 Whisper | 免费，离线可用 | 需本地安装，占资源 | ⭐ **默认首选** (本地文件) |
| **openai-whisper-api** | OpenAI API | 快速，无需本地资源 | 需 API key，按量付费 | 在线/实时场景 |

**决策规则**：
- 本地音频文件 → `openai-whisper`
- 在线/实时/大文件 → `openai-whisper-api`

---

### 3. 文档处理

| Skill | 功能 | 建议 |
|-------|------|------|
| **markdown-converter** | 各种格式 → Markdown | ⭐ **保留** (专用转换) |
| **summarize** | 总结 URL/文件/视频 | ⭐ **保留** (专用总结) |

**决策规则**：
- 需要完整文档内容 → `markdown-converter`
- 只需要摘要 → `summarize`
- **两者不冲突，都保留**

---

### 4. 项目管理

| Skill | 功能 | 建议 |
|-------|------|------|
| **project-bootstrap** | 项目初始化，生成 EDL | ⭐ **保留** |
| **auto-project-launcher** | 自动识别意图创建 Thread | ⭐ **保留** |
| **project-management-2** | 通用项目管理方法 | ❌ **废弃** (理论文档，无实际工具) |

**决策规则**：
- 新项目启动 → `auto-project-launcher` → `project-bootstrap`
- `project-management-2` 仅为方法论，可合并到文档

---

## 二、可废弃/合并的 Skill

| Skill | 原因 | 处理方式 |
|-------|------|----------|
| **project-management-2** | 纯方法论，无实际工具 | 内容合并到 `documentation` |
| **references** | 空目录/占位符 | 删除 |
| **scripts** | 与 workspace scripts 重复 | 审查后合并 |

---

## 三、Skill 分类重组

### 核心工作流 (必须)
- `user-preferences` - 用户偏好主源
- `subagent-manager` - 子代理管理
- `fis-architecture` - 多代理工作流
- `auto-project-launcher` - 项目自动启动
- `project-bootstrap` - 项目初始化

### 代码开发 (5个)
- `code-review` - 代码审查
- `github-issue-resolver` - Issue 修复
- `github-actions-generator` - CI 生成
- `python-script-generator` - Python 项目生成
- `lsp-python` - Python 语言支持

### 文档处理 (4个)
- `docx-master` - Word 处理
- `pptx-master` - PPT 处理
- `markdown-converter` - 文档转换
- `summarize` - 内容总结
- `documentation` - 文档规范

### 知识管理 (4个)
- `ontology` - 知识图谱
- `gpr-memory-archive-lite` - GPR 归档
- `rule-archive-lite` - 规则归档
- `self-improving-agent` - 自我改进

### 工具集成 (6个)
- `openai-tts` (默认) / `edge-tts` (备用) - TTS
- `openai-whisper` (本地) / `openai-whisper-api` (在线) - STT
- `multi-search-engine` - 多引擎搜索
- `obsidian` - Obsidian 笔记
- `discord-voice` - Discord 语音

### Skill 管理 (3个)
- `skill-creator` - 创建 skill
- `skill-vetter` - 审核 skill
- `find-skills` - 发现 skill

### 其他 (2个)
- `change-control-lite` - 变更控制
- `proactive-agent-lite` - 主动代理模式
- `turix-cua` - 桌面自动化
- `python-dataviz` - 数据可视化

---

## 四、默认选择速查表

| 需求 | 默认 Skill | 降级/备用 |
|------|-----------|----------|
| TTS | `openai-tts` | `edge-tts` |
| STT 本地文件 | `openai-whisper` | - |
| STT 在线/实时 | `openai-whisper-api` | - |
| 文档转 Markdown | `markdown-converter` | - |
| 内容总结 | `summarize` | - |
| 项目管理 | `auto-project-launcher` | - |
| 代码审查 | `code-review` | - |
| 搜索 | `multi-search-engine` | - |

---

## 五、执行清单

- [ ] 1. 标记 `project-management-2` 为废弃（内容迁移）
- [ ] 2. 删除空 `references` skill
- [ ] 3. 审查 `scripts` skill 内容
- [ ] 4. 更新 `user-preferences` 添加默认选择规则
- [ ] 5. 测试精简后的 skill 调用

---

## 六、预计效果

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| Skill 数量 | 34 | 30 | -12% |
| 决策时间 | 平均 5-10s | 平均 2-3s | -60% |
| 认知负担 | 高 | 中 | 显著降低 |
