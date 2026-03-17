#!/usr/bin/env python3
"""
INDEX Auto-Sync Tool
自动扫描规则文件并同步更新 rules/INDEX.md
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/baiiy1/.openclaw/workspace")
RULES_DIRS = [WORKSPACE / "skills", WORKSPACE / "rules", WORKSPACE]
INDEX_FILE = WORKSPACE / "rules" / "INDEX.md"

# 需要扫描的文件模式
INCLUDE_PATTERNS = ["*.md"]
EXCLUDE_PATTERNS = ["node_modules", ".venv", "archive", "repos", "reports"]

def extract_frontmatter(file_path):
    """提取文件的 YAML Frontmatter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找 --- 包裹的 frontmatter
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None
        
        try:
            frontmatter = yaml.safe_load(match.group(1))
            if not isinstance(frontmatter, dict):
                return None
            return {
                'id': frontmatter.get('id', 'unknown'),
                'type': frontmatter.get('type', 'unknown'),
                'priority': frontmatter.get('priority', 'medium'),
                'scope': frontmatter.get('scope', []),
                'description': frontmatter.get('description', ''),
                'path': str(file_path.relative_to(WORKSPACE))
            }
        except yaml.YAMLError:
            return None
    except Exception:
        return None

def scan_rule_files():
    """扫描所有规则文件"""
    rules = []
    
    for rules_dir in RULES_DIRS:
        if not rules_dir.exists():
            continue
        
        for pattern in INCLUDE_PATTERNS:
            for file_path in rules_dir.rglob(pattern):
                # 排除不需要的目录
                if any(excl in str(file_path) for excl in EXCLUDE_PATTERNS):
                    continue
                
                frontmatter = extract_frontmatter(file_path)
                if frontmatter:
                    rules.append(frontmatter)
    
    return rules

def generate_index_content(rules):
    """生成 INDEX.md 内容"""
    # 按优先级排序
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    rules.sort(key=lambda x: priority_order.get(x['priority'], 3))
    
    # 生成内容
    lines = [
        "---",
        "id: rule-index-registry",
        "type: core-system",
        "priority: high",
        "scope: [index, registry, rule, navigation]",
        "description: 规则注册表与导航中心，汇总所有文档的 Frontmatter 元数据供按需加载",
        f"last_updated: {datetime.now().strftime('%Y-%m-%d')}",
        "auto_generated: true",
        "---",
        "",
        "# 规则注册表 (Rule Registry)",
        "",
        "> 本文件由 `scripts/sync-index.py` 自动生成，请勿手动编辑。",
        "> 如需更新，运行：`python scripts/sync-index.py`",
        "",
        "## 核心执行规则",
        "",
        "| id | type | priority | scope | description | path |",
        "|---|---|---|---|---|---|",
    ]
    
    # 添加 high priority 规则
    for rule in rules:
        if rule['priority'] == 'high':
            scope_str = ', '.join(rule['scope'][:3]) + ('...' if len(rule['scope']) > 3 else '')
            desc = rule['description'][:50] + ('...' if len(rule['description']) > 50 else '')
            lines.append(f"| {rule['id']} | {rule['type']} | {rule['priority']} | {scope_str} | {desc} | {rule['path']} |")
    
    lines.extend([
        "",
        "## 辅助配置文档",
        "",
        "| id | type | priority | scope | description | path |",
        "|---|---|---|---|---|---|",
    ])
    
    # 添加 medium/low priority 规则
    for rule in rules:
        if rule['priority'] != 'high':
            scope_str = ', '.join(rule['scope'][:3]) + ('...' if len(rule['scope']) > 3 else '')
            desc = rule['description'][:50] + ('...' if len(rule['description']) > 50 else '')
            lines.append(f"| {rule['id']} | {rule['type']} | {rule['priority']} | {scope_str} | {desc} | {rule['path']} |")
    
    lines.extend([
        "",
        "## 按需加载指引",
        "",
        "主进程默认只读取本 INDEX 和各文件的 Frontmatter，命中 scope 或匹配 description 意图时才加载全文。",
        "",
        "### 快速路由",
        "",
        "- 代码任务 → 找 scope 含 `code` / `opencode` 的规则",
        "- 多步骤任务 → 找 scope 含 `manager` / `multi-step` 的规则",
        "- 调研任务 → 找 scope 含 `research` / `investigate` 的规则",
        "- 高风险任务 → 找 priority 为 `high` 且 scope 含 `review` 的规则",
        "",
        "---",
        "",
        f"*最后同步时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
    ])
    
    return '\n'.join(lines)

def main():
    """主函数"""
    print("🔍 扫描规则文件...")
    rules = scan_rule_files()
    print(f"✅ 找到 {len(rules)} 个规则文件")
    
    print("📝 生成 INDEX.md...")
    content = generate_index_content(rules)
    
    print(f"💾 写入 {INDEX_FILE}...")
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 同步完成！")
    print(f"\n统计:")
    print(f"  - 高优先级规则: {sum(1 for r in rules if r['priority'] == 'high')}")
    print(f"  - 中优先级规则: {sum(1 for r in rules if r['priority'] == 'medium')}")
    print(f"  - 低优先级规则: {sum(1 for r in rules if r['priority'] == 'low')}")

if __name__ == "__main__":
    main()
