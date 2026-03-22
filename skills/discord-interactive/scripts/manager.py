"""
Daily Newspaper Content Manager
管理每日时报的内容数据
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

class NewspaperManager:
    def __init__(self, data_dir: Optional[str] = None):
        """初始化报纸管理器"""
        if data_dir is None:
            self.data_dir = Path.home() / ".openclaw" / "daily-newspaper"
        else:
            self.data_dir = Path(data_dir)
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = self.data_dir / "content.json"
        self.archive_dir = self.data_dir / "archive"
        self.archive_dir.mkdir(exist_ok=True)
        
        if not self.data_file.exists():
            self._init_data()
    
    def _init_data(self):
        """初始化数据文件"""
        initial_data = {
            "version": "2.0",
            "last_updated": datetime.now().isoformat(),
            "headlines": [],
            "domestic": [],
            "international": [],
            "gpr": [],
            "ai": [],
            "tech": [],
            "academic": [],
            "general": [],
            "memory": [],
            "notes": []
        }
        self._save_data(initial_data)
    
    def _load_data(self) -> dict:
        """加载数据"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self._init_data()
            return self._load_data()
    
    def _save_data(self, data: dict):
        """保存数据"""
        data["last_updated"] = datetime.now().isoformat()
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_headline(self, title: str, summary: str, author: str = "Hanako"):
        """添加头条新闻"""
        data = self._load_data()
        headline = {
            "id": f"headline_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": title,
            "summary": summary,
            "author": author,
            "created_at": datetime.now().isoformat()
        }
        data["headlines"] = [headline]
        self._save_data(data)
        return headline["id"]
    
    def add_news(self, section: str, title: str, content: str, source: str = "", url: str = ""):
        """通用添加新闻方法"""
        data = self._load_data()
        
        news = {
            "id": f"{section}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": title,
            "content": content,
            "source": source,
            "url": url,
            "created_at": datetime.now().isoformat()
        }
        
        if section not in data:
            data[section] = []
        
        data[section].insert(0, news)
        data[section] = data[section][:15]
        self._save_data(data)
        return news["id"]
    
    # 兼容旧版方法
    def add_tech_news(self, title: str, content: str, source: str = "", url: str = ""):
        return self.add_news("tech", title, content, source, url)
    
    def add_academic_news(self, title: str, content: str, source: str = "", url: str = ""):
        return self.add_news("academic", title, content, source, url)
    
    def add_general_news(self, title: str, content: str, source: str = "", url: str = ""):
        return self.add_news("general", title, content, source, url)
    
    def add_memory(self, content: str, author: str = "Hanako"):
        """添加记忆心得"""
        data = self._load_data()
        memory = {
            "id": f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "content": content,
            "author": author,
            "created_at": datetime.now().isoformat()
        }
        data["memory"].insert(0, memory)
        data["memory"] = data["memory"][:10]
        self._save_data(data)
        return memory["id"]
    
    def add_note(self, content: str):
        """添加笔记"""
        data = self._load_data()
        note = {
            "id": f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "content": content,
            "created_at": datetime.now().isoformat()
        }
        data["notes"].insert(0, note)
        data["notes"] = data["notes"][:30]
        self._save_data(data)
        return note["id"]
    
    def clear_section(self, section: str):
        """清空某个栏目"""
        valid_sections = ["headlines", "domestic", "international", "gpr", "ai", "tech", "academic", "general", "memory", "notes"]
        if section not in valid_sections:
            raise ValueError(f"Invalid section: {section}")
        
        data = self._load_data()
        data[section] = []
        self._save_data(data)
    
    def clear_all(self):
        """清空所有内容"""
        self._init_data()
    
    def get_data(self) -> dict:
        """获取所有数据"""
        return self._load_data()
    
    def archive_current(self) -> str:
        """将当前报纸存档"""
        data = self._load_data()
        
        has_content = any([
            data.get("headlines"),
            data.get("domestic"),
            data.get("international"),
            data.get("gpr"),
            data.get("ai"),
            data.get("tech"),
            data.get("academic"),
            data.get("memory"),
            data.get("notes")
        ])
        
        if not has_content:
            return None
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        archive_file = self.archive_dir / f"{date_str}.json"
        
        if archive_file.exists():
            timestamp = datetime.now().strftime("%H%M%S")
            archive_file = self.archive_dir / f"{date_str}_{timestamp}.json"
        
        archive_data = {
            "date": date_str,
            "archived_at": datetime.now().isoformat(),
            **data
        }
        
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(archive_data, f, ensure_ascii=False, indent=2)
        
        return str(archive_file)
    
    def list_archives(self) -> list:
        """列出所有存档"""
        archives = []
        for file in sorted(self.archive_dir.glob("*.json"), reverse=True):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                archives.append({
                    "file": file.name,
                    "date": data.get("date", file.stem[:10]),
                    "archived_at": data.get("archived_at", ""),
                    "headline": data.get("headlines", [{}])[0].get("title", "无标题") if data.get("headlines") else "无标题"
                })
            except:
                continue
        return archives
    
    def load_archive(self, date_or_file: str) -> dict:
        """加载指定日期的存档"""
        archive_file = self.archive_dir / date_or_file
        if not archive_file.exists():
            archive_file = self.archive_dir / f"{date_or_file}.json"
        
        if not archive_file.exists():
            raise FileNotFoundError(f"找不到存档: {date_or_file}")
        
        with open(archive_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_archive_html(self, date_or_file: str, output_path: Optional[str] = None) -> str:
        """为指定存档生成 HTML"""
        archive_data = self.load_archive(date_or_file)
        
        if output_path is None:
            filename = date_or_file.replace('.json', '.html') if date_or_file.endswith('.json') else f"{date_or_file}.html"
            output_path = self.data_dir / filename
        else:
            output_path = Path(output_path)
        
        template_path = Path(__file__).parent.parent / "assets" / "template.html"
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        archive_date = archive_data.get("date", "")
        html = html.replace('<div class="masthead-date" id="current-date">Loading...</div>', f'<div class="masthead-date" id="current-date">{archive_date}</div>')
        
        if archive_data.get("headlines"):
            headline = archive_data["headlines"][0]
            html = html.replace('<h2 class="headline-title">欢迎使用每日时报</h2>', f'<h2 class="headline-title">{headline["title"]}</h2>')
            html = html.replace('<p class="headline-summary">\n                    这是一份专属于你的个性化报纸，汇集每日科技动态、学术前沿、个人笔记与AI助手的心得体会。\n                    复古的排版风格，现代的资讯内容，让阅读成为一种享受。\n                </p>', f'<p class="headline-summary">{headline["summary"]}</p>')
        
        # 替换各栏目
        for section in ["domestic", "international", "gpr", "ai", "tech", "academic"]:
            if archive_data.get(section):
                articles = self._generate_articles_html(archive_data[section][:3])
                html = self._replace_column(html, f'data-column="{section}"', articles)
        
        if archive_data.get("memory"):
            memory = archive_data["memory"][0]
            html = html.replace('<p class="feature-content">\n                    "每一天都是新的开始，每一刻都值得记录。在这里，我会分享关于 GPR 信号处理、UAV 遥感技术、以及 AI 在地球物理探测中应用的思考与感悟。"\n                </p>', f'<p class="feature-content">"{memory["content"]}"</p>')
        
        if archive_data.get("notes"):
            notes_html = self._generate_notes_html(archive_data["notes"][:3])
            html = self._replace_section(html, 'notes-section', notes_html)
        
        # 添加存档标记
        archive_banner = f'<div style="background: var(--paper-dark); padding: 10px; text-align: center; border-bottom: 1px solid var(--border-color); font-family: var(--font-sans); font-size: 12px; color: var(--ink-light);">📰 存档报纸 · {archive_date} · <a href="archive.html" style="color: var(--accent-red);">查看所有存档</a> · <a href="index.html" style="color: var(--accent-red);">返回今日</a></div>'
        html = html.replace('<div class="newspaper">', archive_banner + '\n    <div class="newspaper">')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return str(output_path)
    
    def generate_archive_index(self) -> str:
        """生成存档索引页面"""
        archives = self.list_archives()
        output_path = self.data_dir / "archive.html"
        
        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>往期报纸 - Daily Times Archive</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Noto+Sans+SC:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --paper-bg: #F5F0E6;
            --paper-dark: #E8E0D0;
            --ink-black: #1A1A1A;
            --ink-gray: #4A4A4A;
            --ink-light: #7A7A7A;
            --accent-red: #8B2635;
            --accent-gold: #B8860B;
            --border-color: #2A2A2A;
            --font-display: 'Playfair Display', 'Noto Serif SC', serif;
            --font-body: 'Noto Serif SC', Georgia, serif;
            --font-sans: 'Noto Sans SC', sans-serif;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: var(--font-body);
            background: var(--paper-bg);
            color: var(--ink-black);
            line-height: 1.7;
            min-height: 100vh;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .header {{
            text-align: center;
            padding: 30px 0;
            border-bottom: 3px double var(--border-color);
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-family: var(--font-display);
            font-size: 48px;
            font-weight: 900;
            margin-bottom: 10px;
        }}
        .header p {{
            font-family: var(--font-sans);
            font-size: 14px;
            color: var(--ink-light);
            letter-spacing: 3px;
        }}
        .back-link {{
            display: inline-block;
            margin-bottom: 30px;
            font-family: var(--font-sans);
            font-size: 13px;
            color: var(--accent-red);
            text-decoration: none;
        }}
        .back-link:hover {{ text-decoration: underline; }}
        .archive-list {{ list-style: none; }}
        .archive-item {{
            border-bottom: 1px solid var(--border-color);
            padding: 25px 0;
            transition: background 0.3s;
        }}
        .archive-item:hover {{
            background: var(--paper-dark);
            margin: 0 -20px;
            padding-left: 20px;
            padding-right: 20px;
        }}
        .archive-date {{
            font-family: var(--font-sans);
            font-size: 12px;
            color: var(--accent-gold);
            letter-spacing: 2px;
            margin-bottom: 8px;
        }}
        .archive-title {{
            font-family: var(--font-display);
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        .archive-title a {{
            color: inherit;
            text-decoration: none;
        }}
        .archive-title a:hover {{ color: var(--accent-red); }}
        .archive-meta {{
            font-family: var(--font-sans);
            font-size: 12px;
            color: var(--ink-light);
        }}
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: var(--ink-light);
        }}
        .footer {{
            text-align: center;
            padding: 40px 0;
            border-top: 1px solid var(--border-color);
            margin-top: 40px;
            font-family: var(--font-sans);
            font-size: 12px;
            color: var(--ink-light);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>往期报纸</h1>
            <p>ARCHIVE · 装订成册的每日时报</p>
        </div>
        <a href="index.html" class="back-link">← 返回今日报纸</a>
'''
        
        if archives:
            html_content += '        <ul class="archive-list">\n'
            for archive in archives:
                date_display = archive["date"]
                file_link = archive["file"].replace('.json', '.html')
                html_content += f'''        <li class="archive-item">
            <div class="archive-date">{date_display}</div>
            <div class="archive-title"><a href="{file_link}">{archive["headline"]}</a></div>
            <div class="archive-meta">存档时间: {archive["archived_at"][:16].replace("T", " ")}</div>
        </li>
'''
            html_content += '        </ul>\n'
        else:
            html_content += '''        <div class="empty-state">
            <p>暂无存档报纸</p>
            <p>每天生成报纸后会自动存档到这里</p>
        </div>
'''
        
        html_content += '''        <div class="footer">
            <p>每日时报 · Daily Times Archive</p>
            <p>Generated with ❤️ by Hanako</p>
        </div>
    </div>
</body>
</html>
'''
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)
    
    def generate_all_archive_htmls(self) -> list:
        """为所有存档 JSON 生成对应的 HTML 文件"""
        generated = []
        archives = self.list_archives()
        
        for archive in archives:
            json_file = archive["file"]
            html_file = json_file.replace('.json', '.html')
            output_path = self.data_dir / html_file
            
            try:
                self.generate_archive_html(json_file, output_path)
                generated.append(str(output_path))
            except Exception as e:
                print(f"生成存档 HTML 失败 {json_file}: {e}")
        
        return generated
    
    def generate_html(self, template_path: Optional[str] = None, output_path: Optional[str] = None) -> str:
        """生成 HTML 报纸页面"""
        if template_path is None:
            template_path = Path(__file__).parent.parent / "assets" / "template.html"
        else:
            template_path = Path(template_path)
        
        if output_path is None:
            output_path = self.data_dir / "index.html"
        else:
            output_path = Path(output_path)
        
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        data = self._load_data()
        
        # 添加往期导航
        html = html.replace('<div class="nav-item" data-section="notes">笔记</div>', '<div class="nav-item" data-section="notes">笔记</div>\n            <div class="nav-item" onclick="window.location.href=\'archive.html\'">往期</div>')
        
        # 替换头条
        if data.get("headlines"):
            headline = data["headlines"][0]
            html = html.replace('<h2 class="headline-title">欢迎使用每日时报</h2>', f'<h2 class="headline-title">{headline["title"]}</h2>')
            html = html.replace('<p class="headline-summary">\n                    这是一份专为 GPR/UAV 信号处理研究者定制的学术科技报纸。每日精选国内外科技动态、AI前沿突破、雷达技术进展，以及学术研究热点，以复古报纸的形式呈现给您。\n                </p>', f'<p class="headline-summary">{headline["summary"]}</p>')
        
        # 替换四栏内容
        for section in ["domestic", "international", "gpr", "ai"]:
            if data.get(section):
                articles = self._generate_articles_html(data[section][:3])
                html = self._replace_column(html, f'data-column="{section}"', articles)
        
        # 兼容旧版
        for section in ["tech", "academic", "general"]:
            if data.get(section):
                articles = self._generate_articles_html(data[section][:3])
                html = self._replace_column(html, f'data-column="{section}"', articles)
        
        # 替换记忆心得
        if data.get("memory"):
            memory = data["memory"][0]
            html = html.replace('<p class="feature-content">\n                    "每一天都是新的开始，每一刻都值得记录。在这里，我会分享关于 GPR 信号处理、UAV 遥感技术、以及 AI 在地球物理探测中应用的思考与感悟。"\n                </p>', f'<p class="feature-content">"{memory["content"]}"</p>')
        
        # 替换笔记
        if data.get("notes"):
            notes_html = self._generate_notes_html(data["notes"][:3])
            html = self._replace_section(html, 'notes-section', notes_html)
        
        # 替换往期回顾（如果有存档）
        archives = self.list_archives()
        if archives:
            latest = archives[0]
            html = html.replace('{{ARCHIVE_DATE_1}}', latest["date"])
            html = html.replace('{{ARCHIVE_LINK_1}}', latest["file"].replace('.json', '.html'))
            html = html.replace('{{ARCHIVE_TITLE_1}}', latest["headline"])
            html = html.replace('{{ARCHIVE_EXCERPT_1}}', latest.get("excerpt", "点击查看详情..."))
        else:
            # 没有存档时显示提示
            html = html.replace('{{ARCHIVE_DATE_1}}', '今日')
            html = html.replace('{{ARCHIVE_LINK_1}}', '#')
            html = html.replace('{{ARCHIVE_TITLE_1}}', '今日首刊')
            html = html.replace('{{ARCHIVE_EXCERPT_1}}', '这是每日时报的第一期，往期内容将在这里显示。')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return str(output_path)
    
    def _generate_articles_html(self, articles: list) -> str:
        """生成文章 HTML，标题可点击跳转"""
        html = ""
        for article in articles:
            created = datetime.fromisoformat(article["created_at"])
            time_str = created.strftime("%H:%M")
            url = article.get("url", "")
            source = article.get("source", "")
            title = article["title"]
            
            # 标题可点击跳转
            if url:
                title_html = f'<a href="{url}" target="_blank" style="color: inherit; text-decoration: none;">{title}</a>'
                source_link = f'<a href="{url}" target="_blank" style="color: var(--accent-red);">{source}</a>'
            else:
                title_html = title
                source_link = source
            
            html += f'''
                <article class="article">
                    <h3 class="article-title">{title_html}</h3>
                    <p class="article-content">{article["content"]}</p>
                    <div class="article-meta">{time_str} · 来源: {source_link}</div>
                </article>
            '''
        return html
    
    def _generate_notes_html(self, notes: list) -> str:
        """生成笔记 HTML"""
        html = ''
        for note in notes:
            created = datetime.fromisoformat(note["created_at"])
            time_str = created.strftime("%H:%M")
            html += f'''
                <div class="note-item">
                    <div class="note-time">{time_str}</div>
                    <div class="note-text">{note["content"]}</div>
                </div>
            '''
        return html
    
    def _replace_column(self, html: str, column_attr: str, content: str) -> str:
        """替换栏目内容"""
        header_map = {
            'domestic': '国内科技',
            'international': '国际动态',
            'gpr': 'GPR/UAV技术',
            'ai': 'AI前沿',
            'tech': '科技动态 · Tech',
            'academic': '学术前沿 · Academic',
            'general': '综合资讯 · General'
        }
        
        for key, value in header_map.items():
            if key in column_attr:
                header_text = value
                break
        else:
            header_text = '资讯'
        
        # 尝试两种可能的 class 名
        for class_name in ['content-column', 'column']:
            start_marker = f'<div class="{class_name}" {column_attr}>'
            start_idx = html.find(start_marker)
            if start_idx != -1:
                break
        
        if start_idx == -1:
            return html
        
        start_content_idx = start_idx + len(start_marker)
        depth = 1
        pos = start_content_idx
        end_idx = start_content_idx
        
        while depth > 0 and pos < len(html):
            next_open = html.find('<div', pos)
            next_close = html.find('</div>', pos)
            
            if next_close == -1:
                break
            
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                if depth == 0:
                    end_idx = next_close
                pos = next_close + 6
        
        new_column = f'{start_marker}\n                <div class="column-header">{header_text}</div>\n                {content}\n            </div>'
        
        return html[:start_idx] + new_column + html[end_idx + 6:]
    
    def _replace_section(self, html: str, section_class: str, content: str) -> str:
        """替换区块内容"""
        import re
        pattern = f'(<section class="{section_class}" id="[^"]*">).*?(</section>)'
        replacement = f'\\1\n            {content}\n        \\2'
        return re.sub(pattern, replacement, html, flags=re.DOTALL, count=1)


def main():
    """CLI 入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='每日时报内容管理器')
    parser.add_argument('--data-dir', help='数据目录路径')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 添加头条
    add_headline = subparsers.add_parser('add-headline', help='添加头条新闻')
    add_headline.add_argument('title', help='标题')
    add_headline.add_argument('summary', help='摘要')
    add_headline.add_argument('--author', default='Hanako', help='作者')
    
    # 添加新闻
    add_news = subparsers.add_parser('add-news', help='添加新闻')
    add_news.add_argument('section', choices=['domestic', 'international', 'gpr', 'ai', 'tech', 'academic', 'general'])
    add_news.add_argument('title', help='标题')
    add_news.add_argument('content', help='内容')
    add_news.add_argument('--source', default='', help='来源')
    add_news.add_argument('--url', default='', help='链接')
    
    # 添加记忆心得
    add_memory = subparsers.add_parser('add-memory', help='添加记忆心得')
    add_memory.add_argument('content', help='内容')
    add_memory.add_argument('--author', default='Hanako', help='作者')
    
    # 添加笔记
    add_note = subparsers.add_parser('add-note', help='添加笔记')
    add_note.add_argument('content', help='内容')
    
    # 清空栏目
    clear = subparsers.add_parser('clear', help='清空栏目')
    clear.add_argument('section', choices=['headlines', 'domestic', 'international', 'gpr', 'ai', 'tech', 'academic', 'general', 'memory', 'notes', 'all'])
    
    # 生成 HTML
    generate = subparsers.add_parser('generate', help='生成 HTML 页面')
    generate.add_argument('--template', help='模板路径')
    generate.add_argument('--output', help='输出路径')
    
    # 存档管理
    archive = subparsers.add_parser('archive', help='存档管理')
    archive.add_argument('action', choices=['save', 'list', 'show', 'generate'])
    archive.add_argument('--date', help='日期或文件名')
    
    # 查看数据
    subparsers.add_parser('show', help='查看当前数据')
    
    args = parser.parse_args()
    
    manager = NewspaperManager(args.data_dir)
    
    if args.command == 'add-headline':
        id = manager.add_headline(args.title, args.summary, args.author)
        print(f"已添加头条: {id}")
    
    elif args.command == 'add-news':
        id = manager.add_news(args.section, args.title, args.content, args.source, args.url)
        print(f"已添加新闻: {id}")
    
    elif args.command == 'add-memory':
        id = manager.add_memory(args.content, args.author)
        print(f"已添加记忆心得: {id}")
    
    elif args.command == 'add-note':
        id = manager.add_note(args.content)
        print(f"已添加笔记: {id}")
    
    elif args.command == 'clear':
        if args.section == 'all':
            manager.clear_all()
            print("已清空所有内容")
        else:
            manager.clear_section(args.section)
            print(f"已清空栏目: {args.section}")
    
    elif args.command == 'generate':
        output = manager.generate_html(args.template, args.output)
        manager.generate_archive_index()
        print(f"已生成 HTML: {output}")
    
    elif args.command == 'archive':
        if args.action == 'save':
            result = manager.archive_current()
            if result:
                print(f"已存档: {result}")
            else:
                print("没有内容需要存档")
        
        elif args.action == 'list':
            archives = manager.list_archives()
            if archives:
                print(f"共有 {len(archives)} 期存档:")
                for a in archives:
                    print(f"  📰 {a['date']} - {a['headline']}")
            else:
                print("暂无存档")
        
        elif args.action == 'show':
            if not args.date:
                print("请使用 --date 指定日期或文件名")
                return
            try:
                data = manager.load_archive(args.date)
                print(f"📰 {data.get('date', args.date)} 的报纸内容:")
                if data.get('headlines'):
                    print(f"  头条: {data['headlines'][0]['title']}")
                for section in ['domestic', 'international', 'gpr', 'ai']:
                    if data.get(section):
                        print(f"  {section}: {len(data[section])} 条")
            except FileNotFoundError as e:
                print(f"错误: {e}")
        
        elif args.action == 'generate':
            if not args.date:
                print("请使用 --date 指定日期或文件名")
                return
            try:
                output = manager.generate_archive_html(args.date)
                print(f"已生成存档页面: {output}")
            except FileNotFoundError as e:
                print(f"错误: {e}")
    
    elif args.command == 'show':
        print(json.dumps(manager.get_data(), ensure_ascii=False, indent=2))
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
