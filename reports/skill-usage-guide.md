# Skill 使用方案总览

> 生成时间：2026-03-19 | 共 37 个自定义 Skill

---

## 一、工作流控制类（必须优先使用）

| Skill | 触发条件 | 核心用法 |
|-------|---------|---------|
| **user-preferences** | 所有任务默认适用 | 包含你的硬规则和偏好，自动加载 |
| **subagent-manager** | 多步骤(≥3步)/跨工具/长时间任务 | `sessions_spawn` 派子代理，必须优先使用 |
| **fis-architecture** | 多代理工作流 | `fis_lifecycle.py create/complete` JSON ticket 管理 |
| **auto-project-launcher** | 创建 Thread 做项目 | 自动触发，创建 Thread + project-bootstrap |

---

## 二、代码开发类

| Skill | 触发条件 | 核心用法 |
|-------|---------|---------|
| **code-review** | 代码审查/PR 评审 | 三阶段检查：结构→详细→边界，输出 [CRITICAL]/[MAJOR]/[MINOR]/[NIT] |
| **github-issue-resolver** | 修复 GitHub Issues | 5层护栏：发现→评分→修复→测试→Draft PR |
| **github-actions-generator** | 生成 CI/CD | `github-actions-generator ci --lang python` |
| **python-script-generator** | 生成 Python 项目 | `python-script-generator mytool --type cli/fastapi/scraper/bot` |
| **lsp-python** | Python 开发支持 | 代码补全、跳转、重构 |

---

## 三、文档处理类

| Skill | 触发条件 | 核心用法 |
|-------|---------|---------|
| **markdown-converter** | PDF/Word/PPT/Excel 转 Markdown | `uvx markitdown input.pdf -o output.md` |
| **summarize** | 总结 URL/文件/YouTube | `summarize "url" --model google/gemini-3-flash-preview` |
| **documentation** | 编写技术文档 | 遵循文档结构层次（README→Guides→Reference） |
| **docx-master** | Word 文档处理 | 创建/编辑专业文档 |
| **pptx-master** | PPT 制作 | 自动化演示文稿生成 |

---

## 四、知识管理类

| Skill | 触发条件 | 核心用法 |
|-------|---------|---------|
| **ontology** | 实体管理/知识图谱 | `ontology.py create/query/relate` 管理实体关系 |
| **gpr-memory-archive-lite** | GPR 进度归档 | 写入 `memory/YYYY-MM-DD.md` + git push |
| **rule-archive-lite** | 规则历史归档 | 规则快照存储（只读历史） |
| **self-improving-agent** | 记录错误/学习 | 写入 `.learnings/ERRORS.md` / `LEARNINGS.md` |

---

## 五、项目管理类

| Skill | 触发条件 | 核心用法 |
|-------|---------|---------|
| **project-bootstrap** | 初始化新项目 | 自动确定子代理管道（researcher→coder→reviewer） |
| **project-management-2** | 项目规划 | Eisenhower 矩阵、周计划、日计划 |
| **change-control-lite** | 配置变更 | 变更前通知+备份+回滚计划 |

---

## 六、工具集成类

| Skill | 触发条件 | 核心用法 |
|-------|---------|---------|
| **multi-search-engine** | 多引擎搜索 | 17个搜索引擎（8 CN + 9 Global） |
| **openai-tts** | 文本转语音 | OpenAI TTS API |
| **openai-whisper** | 本地语音转文字 | Whisper CLI |
| **obsidian** | Obsidian 笔记 | obsidian-cli 操作 |

---

## 七、Skill 管理类

| Skill | 触发条件 | 核心用法 |
|-------|---------|---------|
| **skill-creator** | 创建新 skill | `init_skill.py` → 编辑 → `package_skill.py` |
| **skill-vetter** | 审核 skill | 质量检查 |
| **find-skills** | 发现 skill | 搜索可用 skill |

---

## 核心路由规则

### 默认路由判定表 v1

| 场景 | 路由 |
|------|------|
| 纯问答/即时澄清 | 主进程直答 |
| 代码改动 | opencode |
| 多步骤(≥3步)/跨工具 | **subagent_manager**（必须） |
| 资料调研 | researcher |
| 高风险/结果不稳定 | + reviewer |
| 适合自动验收 | 启用 CI |

### 验收闸门 SOP (G1-G6)

```
G1: 执行完成 → G2: 执行者自检 → G3: 主进程人工核验 → G4: CI/自动验收 → G5: reviewer 复核 → G6: 对外回传
```

### 模式切换关键词

- `切 strict` / `切 proactive` / `切 evolver` / `切 ralph` / `恢复 default`
- 优先级：`strict > ralph > evolver > proactive > default`

---

## 强制规则（来自 user-preferences）

1. **subagent_manager 强制**：凡任务存在正向收益，必须优先使用
2. **防死循环**：自检→修复循环最多 3 次
3. **Timeout 熔断**：外部依赖超时 = 闸门失败
4. **No Silent Failure**：无论任何情况必须给用户反馈
5. **按需加载**：闲聊/简单路由只常驻骨架规则

---

## 文件位置

- **User Preferences**: `skills/user-preferences/SKILL.md`
- **Rule Archive**: `skills/rule-archive-lite/SKILL.md`
- **All Skills**: `skills/<skill-name>/SKILL.md`
