# 典型任务路由速查表

> 快速决策：看到任务 → 匹配场景 → 执行路由

---

## 纯问答类（主进程直答）

| 用户输入示例 | 路由 | 说明 |
|-------------|------|------|
| "什么是XXX" | 直答 | 知识性问题 |
| "解释YYY" | 直答 | 概念解释 |
| "比较A和B" | 直答 | 简单对比 |
| "怎么用Z" | 直答 | 用法说明 |
| "总结这段内容" | summarize | 内容摘要 |

---

## 代码类（opencode 优先）

| 场景 | 路由 | Skill |
|------|------|-------|
| 写/改 Python 代码 | opencode | - |
| 生成 Python 项目 | opencode + python-script-generator | 先咨询用户类型 |
| 代码审查 | opencode + code-review | 审查已有代码 |
| 修复 GitHub Issue | github-issue-resolver | 完整 workflow |
| 生成 CI/CD | github-actions-generator | 快速生成配置 |
| 复杂多文件改动 | subagent-manager → opencode | 拆解后执行 |

---

## 多步骤/多工具任务（必走 subagent-manager）

| 场景 | 子代理分配 | 说明 |
|------|-----------|------|
| 调研+实现+验证 | researcher → coder → reviewer | 完整 pipeline |
| 多文件重构 | manager 拆解文件 → opencode 并行 | 按文件分派 |
| 长期运行任务 | manager + 定时进度汇报 | >3分钟的任务 |
| 跨工具链操作 | manager 协调各步骤 | 如：搜索→下载→处理→上传 |

---

## 文档处理类

| 需求 | Skill | 说明 |
|------|-------|------|
| PDF转Markdown | markdown-converter | 保留结构 |
| 总结文章/视频 | summarize | 快速摘要 |
| 生成PPT | pptx-master | 组会汇报等 |
| 编辑Word | docx-master | 合同/报告 |
| 生成技术文档 | documentation | 按规范编写 |

---

## 项目管理类

| 场景 | 路由 | 输出 |
|------|------|------|
| "创建子分区做XXX" | auto-project-launcher | Thread + EDL报告 |
| 初始化新项目 | project-bootstrap | 子代理规划 |
| 复杂多代理协调 | fis-architecture | JSON ticket管理 |

---

## 搜索/调研类

| 需求 | Skill | 说明 |
|------|-------|------|
| 快速搜索 | multi-search-engine | 17引擎并行 |
| 深度调研 | researcher | 文献/方案比较 |

---

## 语音处理类

| 需求 | 默认 | 备用 |
|------|------|------|
| 文本转语音 | openai-tts | edge-tts |
| 本地音频转文字 | openai-whisper | - |
| 在线/实时转文字 | openai-whisper-api | - |

---

## 决策兜底规则

1. **犹豫时**：用 `subagent_manager`
2. **涉及代码**：先 `opencode`，失败再 `coder`
3. **多步骤(≥3)**：必走 `subagent_manager`
4. **高风险/不确定**：加 `reviewer` 复核
5. **适合CI**：启用 `github-actions-generator`

---

## 快速匹配流程

```
用户请求
  ↓
纯问答? → 直答
  ↓ No
代码相关? → opencode
  ↓ No
多步骤/多工具? → subagent_manager
  ↓ No
文档处理? → 对应 doc skill
  ↓ No
其他 → 查上表或询问用户
```
