---
name: daily-newspaper
description: |
  每日时报 - 个性化复古报纸风格资讯聚合器。
  
  首次使用时会询问用户的兴趣领域，自动定制四个栏目：
  - 栏目1：国内/国际新闻（如科技、财经、体育）
  - 栏目2：专业技术（如GPR、嵌入式、AI等）
  - 栏目3：工具/框架动态（如OpenClaw、Agent等）
  - 栏目4：个人兴趣（可自定义）
  
  支持定时自动生成、Web服务器、往期存档。
---

# Daily Newspaper - 每日时报

> 一份完全由你定制的个性化复古报纸 📰

## 首次使用配置

运行配置向导：

```bash
uv run ~/.openclaw/workspace/skills/daily-newspaper/scripts/config_wizard.py
```

或直接编辑配置文件：

```bash
# 配置文件位置
~/.openclaw/daily-newspaper/config.json
```

### 配置示例

```json
{
  "user_profile": {
    "name": "Linn",
    "research_field": "GPR信号处理",
    "interests": ["无人机", "嵌入式开发", "FPGA"]
  },
  "columns": [
    {
      "id": "domestic",
      "name": "🇨🇳 国内科技",
      "sources": ["ithome", "36kr"],
      "keywords": ["AI", "芯片", "无人机"]
    },
    {
      "id": "tech", 
      "name": "📡 GPR·嵌入式",
      "sources": ["ieee", "arxiv"],
      "keywords": ["GPR", "UAV", "FPGA", "ARM", "STM32"]
    },
    {
      "id": "tools",
      "name": "🤖 AI Agent·工具", 
      "sources": ["github", "hackernews"],
      "keywords": ["OpenClaw", "Codex", "Claude Code", "Agent"]
    },
    {
      "id": "general",
      "name": "📚 综合资讯",
      "sources": ["rss"],
      "rss_urls": ["https://example.com/feed.xml"]
    }
  ],
  "schedule": {
    "enabled": true,
    "time": "08:00",
    "timezone": "Asia/Shanghai"
  },
  "server": {
    "enabled": true,
    "port": 8090,
    "auto_start": false
  }
}
```

## 使用方法

### 生成今日报纸

```bash
uv run ~/.openclaw/workspace/skills/daily-newspaper/scripts/generate.py
```

### 启动 Web 服务器

```bash
# 前台运行
uv run python -m http.server 8090 --directory ~/.openclaw/daily-newspaper

# 或使用后��脚本
~/.openclaw/daily-newspaper/start-server.bat
```

### 添加单条资讯

```bash
# 添加头条
uv run scripts/manager.py add-headline "标题" "摘要"

# 添加栏目资讯
uv run scripts/manager.py add-news [栏目ID] "标题" "内容" "来源" "链接"
```

## 目录结构

```
~/.openclaw/daily-newspaper/
├── config.json          # 用户配置文件
├── index.html           # 今日报纸
├── archive.html         # 往期索引
├── hanako-logo.jpg      # 用户头像/logo
├── assets/              # 样式资源
└── archive/             # 历史存档
    ├── 2026-03-22.json
    └── 2026-03-22.html
```

## 定时任务

默认每天早上 8:00 自动生成报纸并发送通知。

```bash
# 查看定时任务
openclaw cron list

# 手动触发
openclaw cron run daily-newspaper-generator
```

---
*个性化资讯，复古体验 🌸*
