# Skill 一页纸速查

> 快速选择正确的 Skill，无需翻阅完整文档

---

## 🚀 快速决策流程

```
用户请求
  ↓
代码相关? ──→ opencode ──→ 失败? ──→ coder
  ↓ 否
多步骤(≥3)? ──→ subagent-manager
  ↓ 否
文档处理? ──→ 查看"文档"分类
  ↓ 否
调研搜索? ──→ researcher / multi-search-engine
  ↓ 否
其他 ──→ 查阅下表
```

---

## 📋 按场景分类

### 代码开发
| 场景 | Skill | 命令/触发 |
|------|-------|-----------|
| 写/改 Python | opencode | 直接执行 |
| 生成 Python 项目 | python-script-generator | `--type cli/fastapi/scraper` |
| 代码审查 | code-review | 3阶段检查 |
| 修复 GitHub Issue | github-issue-resolver | 完整 workflow |
| 生成 CI/CD | github-actions-generator | `--lang python/node` |

### 文档处理
| 场景 | Skill | 命令 |
|------|-------|------|
| PDF → Markdown | markdown-converter | `uvx markitdown input.pdf` |
| 内容总结 | summarize | `summarize "url"` |
| 生成 PPT | pptx-master | 脚本调用 |
| 编辑 Word | docx-master | 脚本调用 |
| 技术文档 | documentation | 按规范编写 |

### 项目管理
| 场景 | Skill | 说明 |
|------|-------|------|
| 创建新项目 | auto-project-launcher | 自动创建 Thread + EDL |
| 初始化项目 | project-bootstrap | 子代理规划 |
| 多代理协调 | fis-architecture | JSON ticket |

### 语音处理
| 场景 | 首选 | 备用 |
|------|------|------|
| 文本转语音 | openai-tts | edge-tts |
| 本地音频转文字 | openai-whisper | - |
| 在线转文字 | openai-whisper-api | - |

### 搜索/调研
| 场景 | Skill | 特点 |
|------|-------|------|
| 快速搜索 | multi-search-engine | 17引擎并行 |
| 深度调研 | researcher | 文献/方案比较 |

### 知识管理
| 场景 | Skill | 用途 |
|------|-------|------|
| GPR 归档 | gpr-memory-archive-lite | 进度记录 |
| 实体管理 | ontology | 知识图谱 |
| 规则归档 | rule-archive-lite | 规则历史 |

---

## 🎯 兜底规则

1. **犹豫时** → 用 `subagent-manager`
2. **代码时** → 先 `opencode`，失败再 `coder`
3. **多步骤** → 必走 `subagent-manager`
4. **高风险** → 加 `reviewer`
5. **适合CI** → 启用 `github-actions-generator`

---

## ⚡ 快速命令

```bash
# 代码相关
opencode                    # 默认代码执行
python-script-generator     # 生成项目
code-review                 # 代码审查

# 文档相关
uvx markitdown input.pdf    # PDF 转 Markdown
summarize "url"             # 总结内容

# 项目相关
auto-project-launcher       # 创建新项目
subagent-manager            # 多步骤任务

# 搜索
multi-search-engine         # 多引擎搜索
```

---

## 📁 文件位置

```
skills/
├── user-preferences/SKILL.md     # 主规则
├── subagent-manager/SKILL.md     # 多步骤任务
├── code-review/SKILL.md          # 代码审查
├── markdown-converter/SKILL.md   # 文档转换
├── summarize/SKILL.md            # 内容总结
└── ...

rules/
└── routing-cheat-sheet.md        # 完整路由表

examples/
└── task-examples.md              # 使用示例
```

---

*快速参考，详细内容请查阅对应 SKILL.md*
