# Daily Newspaper - 每日时报

个性化复古报纸风格的每日资讯聚合器。

## 功能特点

- 📰 **复古报纸风格** - 1920s 大报风格排版
- 🎨 **完全可定制** - 通过配置文件自定义栏目和内容源
- 🤖 **AI 自动生成** - 定时抓取 RSS/API 生成报纸
- 📚 **自动存档** - 历史报纸自动装订成册
- 🌐 **Web 访问** - 本地服务器随时阅读

## 快速开始

### 方式1：自动配置（推荐）

让 Agent 自动解压并配置：

```
请帮我解压 daily-newspaper-v1.0.zip 到 OpenClaw workspace，
然后运行配置向导，帮我设置每日时报。
```

Agent 会自动：
1. 解压到 `~/.openclaw/workspace/skills/daily-newspaper/`
2. 运行配置向导询问你的偏好
3. 生成第一份报纸
4. 设置定时任务

### 方式2：手动配置

```bash
# 1. 解压到 OpenClaw workspace
mv daily-newspaper-package ~/.openclaw/workspace/skills/daily-newspaper

# 2. 运行配置向导
uv run python scripts/config_wizard.py

# 3. 生成第一份报纸
uv run python scripts/fetch_news.py
```

### 4. 启动 Web 服务器

```bash
cd ~/.openclaw/daily-newspaper
uv run python -m http.server 8090
```

访问 http://localhost:8090 查看报纸

## 配置说明

编辑 `config.json`：

```json
{
  "user": {
    "name": "你的名字",
    "title": "你的身份"
  },
  "newspaper": {
    "title": "报纸标题",
    "subtitle": "副标题",
    "masthead_logo": "logo图片路径（可选）"
  },
  "columns": [
    {
      "id": "唯一标识",
      "name": "栏目名称",
      "description": "栏目描述",
      "sources": [
        {
          "type": "rss|hackernews|arxiv|github_releases",
          "url": "RSS地址（仅rss类型）",
          "name": "来源名称"
        }
      ],
      "max_items": 3
    }
  ]
}
```

### 支持的内容源

| 类型 | 说明 | 示例 |
|------|------|------|
| `rss` | RSS 订阅源 | IT之家、知乎、博客 |
| `hackernews` | Hacker News 热门 | 技术新闻 |
| `arxiv` | 学术论文 | 研究论文搜索 |
| `github_releases` | GitHub 发布 | 工具更新 |

## 定时任务

自动每天早上生成报纸：

```bash
# 查看定时任务
openclaw cron list

# 手动触发
openclaw cron run daily-newspaper-generator
```

## 目录结构

```
daily-newspaper/
├── assets/              # 模板和样式
│   └── template.html    # 报纸模板
├── scripts/
│   ├── fetch_news.py    # 内容抓取
│   ├── manager.py       # 内容管理
│   └── config_wizard.py # 配置向导
├── config.json          # 用户配置
├── config.example.json  # 示例配置
├── index.html           # 今日报纸
├── archive.html         # 往期索引
└── archive/             # 历史存档
```

## 自定义模板

编辑 `assets/template.html` 修改报纸样式：

- 修改 CSS 变量调整配色
- 调整字体和排版
- 添加自定义区块

## 许可证

MIT License - 自由使用和修改

---

Made with ❤️ by Hanako
