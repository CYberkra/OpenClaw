"""
每日时报 - 配置向导
首次使用时运行，收集用户偏好和推送设置
"""

import json
import os
from pathlib import Path

def main():
    print("🌸 欢迎来到每日时报配置向导！")
    print("=" * 50)
    print()
    
    config = {
        "version": "1.0.0",
        "user": {},
        "newspaper": {},
        "columns": [],
        "schedule": {
            "enabled": True,
            "time": "08:00",
            "timezone": "Asia/Shanghai"
        },
        "notifications": {
            "discord": {
                "enabled": False,
                "channel": "",
                "ask_on_setup": False
            }
        },
        "server": {
            "port": 8090,
            "auto_start": False
        }
    }
    
    # 用户基本信息
    print("📋 第一步：基本信息")
    name = input("你的名字（用于署名）: ").strip() or "读者"
    config["user"]["name"] = name
    
    title = input("你的身份/头衔（如：研究者、开发者）: ").strip() or "读者"
    config["user"]["title"] = title
    
    # 报纸设置
    print()
    print("📰 第二步：报纸设置")
    paper_title = input("报纸标题 [默认:每日时报]: ").strip() or "每日时报"
    config["newspaper"]["title"] = paper_title
    config["newspaper"]["subtitle"] = f"DAILY TIMES · {title}的资讯"
    
    has_logo = input("是否有 Logo 图片？(y/n) [默认:n]: ").strip().lower()
    if has_logo == 'y':
        logo_path = input("Logo 文件路径（相对于报纸目录）: ").strip()
        config["newspaper"]["masthead_logo"] = logo_path
    else:
        config["newspaper"]["masthead_logo"] = ""
    
    # 栏目定制
    print()
    print("📚 第三步：栏目定制（共4个栏目）")
    print()
    
    # 栏目1：新闻
    print("【栏目1】新闻资讯")
    news_pref = input("偏好哪类新闻？\n1. 科技\n2. 财经\n3. 综合\n选择 [默认:1]: ").strip() or "1"
    news_types = {"1": "科技", "2": "财经", "3": "综合"}
    news_name = news_types.get(news_pref, "科技")
    config["columns"].append({
        "id": "news",
        "name": f"📰 {news_name}资讯",
        "description": f"每日精选{news_name}新闻",
        "sources": [{"type": "hackernews", "name": "Hacker News"}],
        "max_items": 3
    })
    
    # 栏目2：专业
    print()
    print("【栏目2】专业领域")
    print("这是你最关注的技术或研究领域")
    field = input("你的专业领域（如：AI、嵌入式、前端、生物等）: ").strip() or "技术"
    keywords = input("相关关键词（用空格分隔，用于搜索）: ").strip().split() or [field]
    config["columns"].append({
        "id": "tech",
        "name": f"🔬 {field}",
        "description": f"{field}领域动态",
        "sources": [
            {"type": "arxiv", "query": " ".join(keywords), "name": "arXiv"}
        ],
        "max_items": 3
    })
    
    # 栏目3：工具
    print()
    print("【栏目3】工具/平台")
    print("你日常使用的工具或关注的平台")
    tools = input("关注的工具（用空格分隔，如：VSCode Docker React）: ").strip().split()
    if tools:
        repos = [f"microsoft/{tools[0].lower()}" if tools[0].lower() == "vscode" else f"{tools[0].lower()}/{tools[0].lower()}" for t in tools[:2]]
        config["columns"].append({
            "id": "tools",
            "name": "🛠️ 工具·平台",
            "description": "开发工具更新",
            "sources": [{"type": "github_releases", "repos": repos, "name": "GitHub"}],
            "max_items": 2
        })
    else:
        config["columns"].append({
            "id": "tools",
            "name": "🛠️ 工具·平台",
            "description": "开发工具更新",
            "sources": [{"type": "rss", "url": "https://github.blog/feed/", "name": "GitHub Blog"}],
            "max_items": 2
        })
    
    # 栏目4：兴趣
    print()
    print("【栏目4】个人兴趣")
    interest = input("其他感兴趣的领域（可选）: ").strip()
    if interest:
        config["columns"].append({
            "id": "interest",
            "name": f"💡 {interest}",
            "description": f"{interest}相关资讯",
            "sources": [{"type": "rss", "url": "", "name": "待配置"}],
            "max_items": 2
        })
    else:
        config["columns"].append({
            "id": "interest",
            "name": "💡 综合",
            "description": "其他精选资讯",
            "sources": [{"type": "hackernews", "name": "Hacker News"}],
            "max_items": 2
        })
    
    # 推送设置
    print()
    print("📢 第四步：推送设置")
    enable_notify = input("是否启用 Discord 推送？(y/n) [默认:n]: ").strip().lower()
    if enable_notify == 'y':
        config["notifications"]["discord"]["enabled"] = True
        channel = input("Discord 频道名称或ID: ").strip()
        config["notifications"]["discord"]["channel"] = channel
    
    # 定时设置
    print()
    print("⏰ 第五步：定时生成")
    time_input = input("每天早上几点生成报纸？(HH:MM) [默认:08:00]: ").strip() or "08:00"
    config["schedule"]["time"] = time_input
    
    # 保存配置
    data_dir = Path.home() / ".openclaw" / "daily-newspaper"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    config_path = data_dir / "config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print()
    print("=" * 50)
    print(f"✅ 配置已保存到: {config_path}")
    print()
    print(f"📰 {config['newspaper']['title']} 栏目：")
    for i, col in enumerate(config["columns"], 1):
        print(f"  {i}. {col['name']} - {col['description']}")
    print()
    
    if config["notifications"]["discord"]["enabled"]:
        print(f"📢 推送频道: {config['notifications']['discord']['channel']}")
    else:
        print("📢 推送: 已禁用")
    
    print()
    print("🚀 现在可以生成你的第一份报纸了：")
    print(f"   uv run python scripts/fetch_news.py")
    print()
    print("💡 提示：随时编辑 config.json 修改配置")

if __name__ == '__main__':
    main()
