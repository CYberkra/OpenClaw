"""
每日时报 - 内容抓取引擎
基于用户配置的 RSS/API 抓取
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from manager import NewspaperManager
from datetime import datetime
import urllib.request
import urllib.parse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def load_config():
    """加载用户配置"""
    config_path = Path.home() / ".openclaw" / "daily-newspaper" / "config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def fetch_rss(url: str, max_items: int = 3):
    """抓取 RSS 源"""
    news_items = []
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read().decode('utf-8')
        
        root = ET.fromstring(xml_data)
        items = root.findall('.//item')[:max_items]
        
        for item in items:
            title = item.find('title').text if item.find('title') is not None else "无标题"
            link = item.find('link').text if item.find('link') is not None else ""
            description = item.find('description').text if item.find('description') is not None else ""
            
            # 清理 HTML 标签
            description = re.sub('<[^\u003e]+>', '', description)
            if len(description) > 120:
                description = description[:120] + "..."
            
            news_items.append({
                "title": title,
                "content": description or "",
                "source": urllib.parse.urlparse(url).netloc.replace("www.", ""),
                "url": link
            })
    except Exception as e:
        print(f"  RSS 获取失败 {url}: {e}")
    
    return news_items

def fetch_hackernews(max_items: int = 3):
    """抓取 Hacker News"""
    news_items = []
    try:
        req = urllib.request.Request(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            top_ids = json.loads(response.read().decode())[:max_items + 2]
        
        for item_id in top_ids:
            if len(news_items) >= max_items:
                break
            try:
                req = urllib.request.Request(
                    f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json",
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    item = json.loads(response.read().decode())
                
                if item and item.get("title"):
                    url = item.get("url", "")
                    if url:
                        domain = urllib.parse.urlparse(url).netloc.replace("www.", "")
                        source = domain
                    else:
                        source = "Hacker News"
                        url = f"https://news.ycombinator.com/item?id={item_id}"
                    
                    news_items.append({
                        "title": item["title"],
                        "content": f"{item.get('score', 0)} 赞 · {item.get('descendants', 0)} 评论",
                        "source": source,
                        "url": url
                    })
            except:
                continue
    except Exception as e:
        print(f"  Hacker News 获取失败: {e}")
    
    return news_items

def fetch_arxiv(query: str, max_items: int = 3):
    """抓取 arXiv 论文"""
    news_items = []
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&sortBy=submittedDate&sortOrder=descending&max_results={max_items}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read().decode()
        
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        for entry in root.findall('atom:entry', ns)[:max_items]:
            title_elem = entry.find('atom:title', ns)
            summary_elem = entry.find('atom:summary', ns)
            link_elem = entry.find('atom:id', ns)
            
            title = title_elem.text.strip() if title_elem is not None else "无标题"
            summary = summary_elem.text.strip() if summary_elem is not None else ""
            link = link_elem.text if link_elem is not None else ""
            
            if len(summary) > 120:
                summary = summary[:120] + "..."
            
            news_items.append({
                "title": title,
                "content": summary or "arXiv 论文",
                "source": "arXiv",
                "url": link
            })
    except Exception as e:
        print(f"  arXiv 获取失败: {e}")
    
    return news_items

def fetch_github_releases(repos: list, max_items: int = 3):
    """抓取 GitHub Releases"""
    news_items = []
    for repo in repos[:max_items]:
        try:
            url = f"https://api.github.com/repos/{repo}/releases/latest"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                release = json.loads(response.read().decode())
            
            if release:
                news_items.append({
                    "title": f"{repo} 发布 {release.get('tag_name', '新版本')}",
                    "content": release.get('body', '无更新说明')[:120] + "...",
                    "source": "GitHub",
                    "url": release.get('html_url', f"https://github.com/{repo}/releases")
                })
        except Exception as e:
            print(f"  GitHub Releases 获取失败 {repo}: {e}")
    
    return news_items

def fetch_column_content(column_config: dict):
    """根据栏目配置抓取内容"""
    all_items = []
    max_items = column_config.get("max_items", 3)
    
    for source in column_config.get("sources", []):
        source_type = source.get("type")
        
        if source_type == "rss":
            items = fetch_rss(source.get("url"), max_items)
            all_items.extend(items)
        
        elif source_type == "hackernews":
            items = fetch_hackernews(max_items)
            all_items.extend(items)
        
        elif source_type == "arxiv":
            items = fetch_arxiv(source.get("query", ""), max_items)
            all_items.extend(items)
        
        elif source_type == "github_releases":
            items = fetch_github_releases(source.get("repos", []), max_items)
            all_items.extend(items)
    
    # 去重并限制数量
    seen = set()
    unique_items = []
    for item in all_items:
        if item["title"] not in seen and len(unique_items) < max_items:
            seen.add(item["title"])
            unique_items.append(item)
    
    return unique_items

def generate_daily_newspaper():
    """生成每日报纸"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始生成每日时报...")
    
    # 加载配置
    config = load_config()
    if not config:
        print("❌ 未找到配置文件，请先运行配置向导")
        return None
    
    manager = NewspaperManager()
    
    # 先存档当前报纸
    archive_result = manager.archive_current()
    if archive_result:
        print(f"  已存档旧报纸: {archive_result}")
    
    # 清空旧内容
    for section in ["headlines", "domestic", "international", "gpr", "ai", "memory", "notes"]:
        manager.clear_section(section)
    
    # 添加头条
    today = datetime.now()
    user_name = config.get("user", {}).get("name", "读者")
    manager.add_headline(
        title=f"{config['newspaper']['title']} - {today.strftime('%Y年%m月%d日')}",
        summary=f"本期精选：{', '.join([col['description'] for col in config['columns'][:2]])}等资讯。专为{user_name}定制的个性化报纸。",
        author="Hanako"
    )
    
    # 抓取各栏目内容
    for column in config.get("columns", []):
        column_id = column["id"]
        column_name = column["name"]
        print(f"  抓取栏目: {column_name}")
        
        items = fetch_column_content(column)
        print(f"    获取 {len(items)} 条资讯")
        
        for item in items:
            manager.add_news(column_id, item["title"], item["content"], item["source"], item["url"])
    
    # 添加记忆心得
    manager.add_memory(
        f"今天为 {user_name} 生成了新的每日时报～ 包含 {len(config['columns'])} 个栏目的精选内容。"
        f"报纸风格复古优雅，希望你喜欢！🌸",
        author="Hanako"
    )
    
    # 生成 HTML
    output_path = manager.generate_html()
    print(f"  已生成今日报纸: {output_path}")
    
    # 生成存档索引
    manager.generate_archive_index()
    print(f"  已更新存档索引")
    
    # 为今天的存档生成 HTML 页面
    date_str = today.strftime("%Y-%m-%d")
    try:
        archive_html = manager.generate_archive_html(date_str)
        print(f"  已生成存档页面: {archive_html}")
    except Exception as e:
        print(f"  生成存档页面失败: {e}")
    
    # 生成所有存档 HTML
    manager.generate_all_archive_htmls()
    
    print("每日时报生成完成！")
    
    return {
        "date": date_str,
        "output_path": str(output_path),
        "archive_path": str(archive_result) if archive_result else None
    }

if __name__ == '__main__':
    result = generate_daily_newspaper()
    if result:
        print(json.dumps(result, ensure_ascii=False))
