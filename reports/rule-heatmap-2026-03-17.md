# 规则访问热力图

> 生成时间: 2026-03-17  
> 分析周期: 最近30天 (2026-02-15 ~ 2026-03-17)  
> 数据来源: memory日志 + git提交历史 + INDEX注册表

---

## 热点规则 TOP 10

| 排名 | 规则ID | 文件路径 | 引用/修改次数 | 热度 |
|-----|--------|----------|--------------|------|
| 1 | rule-archive-lite-snapshot | skills/rule-archive-lite/SKILL.md | 28 | 🔥🔥🔥 |
| 2 | rule-user-preferences-main | skills/user-preferences/SKILL.md | 16 | 🔥🔥 |
| 3 | rule-system-bootstrap | SYSTEM_BOOTSTRAP.md | 8 | 🔥🔥 |
| 4 | rule-agents-overview | AGENTS.md | 8 | 🔥🔥 |
| 5 | rule-index-registry | rules/INDEX.md | 5 | 🔥 |
| 6 | rule-user-profile | USER.md | 4 | 🔥 |
| 7 | rule-change-control-lite | skills/change-control-lite/SKILL.md | 3 | 🔥 |
| 8 | rule-self-backup-audit | rules/self-backup-audit-v1.md | 3 | 🔥 |
| 9 | rule-tools-mappings | TOOLS.md | 2 | 🔥 |
| 10 | (skill-tavily-search) | skills/tavily-search/SKILL.md | 2 | 🔥 |

---

## 冷门规则（建议审查）

| 规则ID/文件 | 文件路径 | 最后修改 | 建议 |
|------------|----------|---------|------|
| summarize | skills/summarize/SKILL.md | 2026-03-01 (初始创建) | 使用频率低，检查是否被主动调用 |
| proactive-agent-lite | skills/proactive-agent-lite/SKILL.md | 2026-03-01 (初始创建) | 评估是否启用主动模式功能 |
| pptx-master | skills/pptx-master/*.md | 2026-03-01 (初始创建) | 检查PPT生成需求频率 |
| openai-whisper | skills/openai-whisper/SKILL.md | 2026-03-01 (初始创建) | 评估本地Whisper使用场景 |
| openai-whisper-api | skills/openai-whisper-api/SKILL.md | 2026-03-01 (初始创建) | 对比API与本地版本的使用率 |
| openai-tts | skills/openai-tts/SKILL.md | 2026-03-01 (初始创建) | 检查TTS使用偏好 (vs edge-tts) |
| obsidian | skills/obsidian/SKILL.md | 2026-03-01 (初始创建) | 评估Obsidian集成活跃性 |
| multi-search-engine | skills/multi-search-engine/*.md | 2026-03-01 (初始创建) | 检查搜索需求是否被其他工具覆盖 |
| markdown-converter | skills/markdown-converter/SKILL.md | 2026-03-01 (初始创建) | 评估文档转换需求 |
| gpr-memory-archive-lite | skills/gpr-memory-archive-lite/SKILL.md | 2026-03-01 (初始创建) | GPR专用，按需保留 |
| fis-architecture | skills/fis-architecture/SKILL.md | 2026-03-01 (初始创建) | 评估多Agent工作流启用情况 |
| find-skills | skills/find-skills/SKILL.md | 2026-03-01 (初始创建) | 检查技能发现功能使用频率 |
| edge-tts | skills/edge-tts/SKILL.md | 2026-03-01 (初始创建) | 评估TTS使用偏好 (vs openai-tts) |

> **说明**: 以上规则多为2026-03-01初始创建后未被修改，可能原因：
> 1. 功能稳定，无需更新
> 2. 使用频率低，可考虑归档或删除
> 3. 需检查 memory 日志中是否有实际调用记录

---

## Scope 热度分布

| Scope | 命中次数 | 占比 | 说明 |
|-------|---------|------|------|
| rule | 3 | 10.7% | 规则系统元标签 |
| user | 2 | 7.1% | 用户相关规则 |
| startup | 2 | 7.1% | 启动/初始化流程 |
| preference | 2 | 7.1% | 用户偏好设置 |
| bootstrap | 2 | 7.1% | 系统引导配置 |
| agent | 2 | 7.1% | Agent行为规则 |
| tools | 1 | 3.6% | 工具映射配置 |
| snapshot | 1 | 3.6% | 快照/归档功能 |
| session | 1 | 3.6% | 会话管理 |
| routing | 1 | 3.6% | 路由决策 |
| registry | 1 | 3.6% | 注册表功能 |
| quickstart | 1 | 3.6% | 快速入门 |
| profile | 1 | 3.6% | 用户画像 |
| navigation | 1 | 3.6% | 导航功能 |
| mode | 1 | 3.6% | 模式切换 |
| memory | 1 | 3.6% | 内存管理 |
| mapping | 1 | 3.6% | 映射配置 |
| maintenance | 1 | 3.6% | 维护任务 |
| index | 1 | 3.6% | 索引功能 |
| identity | 1 | 3.6% | 身份管理 |
| history | 1 | 3.6% | 历史记录 |
| execution | 1 | 3.6% | 执行策略 |
| environment | 1 | 3.6% | 环境配置 |
| drift | 1 | 3.6% | 漂移检测 |
| config | 1 | 3.6% | 配置管理 |
| backup | 1 | 3.6% | 备份策略 |
| audit | 1 | 3.6% | 审计功能 |
| archive | 1 | 3.6% | 归档功能 |
| alias | 1 | 3.6% | 别名映射 |

**Scope 聚类分析**:
- **核心系统类** (rule + agent + session + execution): ~21%
- **用户相关类** (user + preference + profile + identity): ~18%
- **系统引导类** (startup + bootstrap + quickstart): ~18%
- **管理运维类** (backup + audit + archive + maintenance + drift): ~18%
- **功能导航类** (index + registry + navigation + routing + mapping): ~18%

---

## 优化建议

### 1. INDEX 重排序建议

**当前问题**: INDEX.md 存在重复条目（rule-index-registry、rule-user-preferences-main 各出现2次）

**建议排序** (按实际使用频率):
```
1. rule-archive-lite-snapshot (28次) - 最活跃
2. rule-user-preferences-main (16次) - 核心规则
3. rule-system-bootstrap (8次) + rule-agents-overview (8次) - 启动双核心
4. rule-index-registry (5次) - 导航中心
5. rule-user-profile (4次) + rule-tools-mappings (2次) - 配置类
6. rule-change-control-lite (3次) + rule-self-backup-audit (3次) - 运维类
7. 其他低频技能 - 按需加载
```

### 2. 技能精简建议

**高优先级审查** (长期未更新):
- 13个技能自2026-03-01后未修改
- 建议检查 memory 日志确认实际调用情况
- 3个月内无调用的技能可考虑归档到 `skills/archive/`

**推荐保留** (高频使用):
- rule-archive-lite: 规则归档系统，被频繁引用
- user-preferences: 核心执行规则
- SYSTEM_BOOTSTRAP + AGENTS: 启动必备

### 3. Scope 标签优化

**建议新增热门 Scope** (基于 memory 日志分析):
- `code` / `opencode` - 代码任务 (memory中多次提及)
- `gpr` - GPR项目专用 (高频出现在memory)
- `discord` - Discord集成 (近期活跃)
- `manager` - 多步骤任务管理

**建议合并低频 Scope**:
- `navigation` + `routing` + `registry` → `nav`
- `backup` + `archive` + `snapshot` → `storage`
- `drift` + `audit` + `maintenance` → `ops`

### 4. 加载策略优化

**当前**: 默认加载 INDEX + Frontmatter，命中 scope 才加载全文
**建议**:
1. 高频规则 (TOP 5) → 启动时预加载全文
2. 中频规则 (6-10) → 保持按需加载
3. 低频规则 → 延迟加载 + 定期清理检查

### 5. 自动化监控建议

添加定期任务 (每7天):
```bash
# 统计规则修改频率
git log --since="7 days ago" --pretty=format: --name-only -- "skills/" "rules/" | sort | uniq -c | sort -rn

# 检查30天无更新的规则
find skills/ -name "SKILL.md" -mtime +30
```

---

## 附录: 数据详情

### 数据来源统计
- **memory文件**: 18个日期的记录 (2026-02-28 ~ 2026-03-17)
- **git提交**: 97条相关提交 (2026-03-01 ~ 2026-03-17)
- **规则文件**: 约30个技能/规则文档
- **分析周期**: 最近30天

### 方法说明
1. **引用次数**: git log 中文件修改次数作为代理指标
2. **热点判定**: 修改次数 ≥ 5次 = 高频, 2-4次 = 中频, ≤ 1次 = 低频
3. **Scope统计**: 提取所有Frontmatter中的scope字段进行频次统计

---

*报告生成: 数据分析子进程*  
*时间: 2026-03-17 14:15*
