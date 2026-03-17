#!/usr/bin/env python3
"""
规则健康检查工具
自动检查规则体系的完整性和一致性
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict

# 配置
WORKSPACE = Path("/home/baiiy1/.openclaw/workspace")
RULES_DIRS = [WORKSPACE / "skills", WORKSPACE / "rules", WORKSPACE]
INDEX_FILE = WORKSPACE / "rules" / "INDEX.md"

# 排除的目录
EXCLUDE_PATTERNS = ["node_modules", ".venv", "archive", "repos", "reports", ".cache"]

# 必需的 Frontmatter 字段
REQUIRED_FIELDS = ['id', 'type', 'priority', 'scope', 'description']
VALID_TYPES = ['core-system', 'agent-profile', 'tool-spec', 'skill-detail']
VALID_PRIORITIES = ['high', 'medium', 'low']

def extract_frontmatter(file_path):
    """提取文件的 YAML Frontmatter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None, "缺少 Frontmatter"
        
        try:
            frontmatter = yaml.safe_load(match.group(1))
            if not isinstance(frontmatter, dict):
                return None, "Frontmatter 格式错误"
            return frontmatter, None
        except yaml.YAMLError as e:
            return None, f"YAML 解析错误: {e}"
    except Exception as e:
        return None, f"文件读取错误: {e}"

def scan_rule_files():
    """扫描所有规则文件"""
    rules = []
    
    for rules_dir in RULES_DIRS:
        if not rules_dir.exists():
            continue
        
        for file_path in rules_dir.rglob("*.md"):
            if any(excl in str(file_path) for excl in EXCLUDE_PATTERNS):
                continue
            
            frontmatter, error = extract_frontmatter(file_path)
            rules.append({
                'path': file_path.relative_to(WORKSPACE),
                'frontmatter': frontmatter,
                'error': error
            })
    
    return rules

def check_frontmatter(rules):
    """检查 Frontmatter 格式"""
    errors = []
    warnings = []
    
    for rule in rules:
        path = rule['path']
        fm = rule['frontmatter']
        error = rule['error']
        
        if error:
            errors.append(f"❌ {path}: {error}")
            continue
        
        # 检查必需字段
        for field in REQUIRED_FIELDS:
            if field not in fm or fm[field] is None:
                errors.append(f"❌ {path}: 缺少必需字段 '{field}'")
        
        # 检查 type 有效性
        if 'type' in fm and fm['type'] not in VALID_TYPES:
            warnings.append(f"⚠️  {path}: type '{fm['type']}' 不是标准值 {VALID_TYPES}")
        
        # 检查 priority 有效性
        if 'priority' in fm and fm['priority'] not in VALID_PRIORITIES:
            errors.append(f"❌ {path}: priority '{fm['priority']}' 无效，应为 {VALID_PRIORITIES}")
        
        # 检查 scope 是否为列表
        if 'scope' in fm and not isinstance(fm['scope'], list):
            errors.append(f"❌ {path}: scope 必须是列表类型")
    
    return errors, warnings

def check_id_uniqueness(rules):
    """检查 ID 唯一性"""
    errors = []
    id_map = defaultdict(list)
    
    for rule in rules:
        if rule['frontmatter'] and 'id' in rule['frontmatter']:
            id_map[rule['frontmatter']['id']].append(rule['path'])
    
    for id_val, paths in id_map.items():
        if len(paths) > 1:
            errors.append(f"❌ ID 重复 '{id_val}': {', '.join(str(p) for p in paths)}")
    
    return errors

def check_broken_links(rules):
    """检查 broken links"""
    warnings = []
    existing_files = set()
    
    # 收集所有存在的文件
    for rule in rules:
        existing_files.add(rule['path'])
    
    # 检查 INDEX 中的链接
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            index_content = f.read()
        
        # 简单的路径匹配
        for rule in rules:
            path_str = str(rule['path'])
            if path_str not in index_content and rule['frontmatter']:
                if rule['frontmatter'].get('priority') == 'high':
                    warnings.append(f"⚠️  {path_str}: 高优先级规则未在 INDEX 中引用")
    
    return warnings

def generate_report(errors, warnings, total_rules):
    """生成检查报告"""
    lines = [
        "=" * 60,
        "规则健康检查报告",
        "=" * 60,
        "",
        f"扫描规则文件: {total_rules} 个",
        "",
    ]
    
    if errors:
        lines.extend([
            f"❌ 错误: {len(errors)} 个 (必须修复)",
            "-" * 40,
        ])
        for error in errors[:10]:  # 最多显示 10 个
            lines.append(error)
        if len(errors) > 10:
            lines.append(f"... 还有 {len(errors) - 10} 个错误")
        lines.append("")
    else:
        lines.extend([
            "✅ 未发现错误",
            "",
        ])
    
    if warnings:
        lines.extend([
            f"⚠️  警告: {len(warnings)} 个 (建议优化)",
            "-" * 40,
        ])
        for warning in warnings[:10]:
            lines.append(warning)
        if len(warnings) > 10:
            lines.append(f"... 还有 {len(warnings) - 10} 个警告")
        lines.append("")
    else:
        lines.extend([
            "✅ 未发现警告",
            "",
        ])
    
    lines.extend([
        "=" * 60,
        "检查完成",
        "=" * 60,
    ])
    
    return '\n'.join(lines)

def main():
    """主函数"""
    print("🔍 扫描规则文件...")
    rules = scan_rule_files()
    print(f"✅ 扫描完成: {len(rules)} 个文件")
    
    print("📝 检查 Frontmatter 格式...")
    fm_errors, fm_warnings = check_frontmatter(rules)
    
    print("🔍 检查 ID 唯一性...")
    id_errors = check_id_uniqueness(rules)
    
    print("🔗 检查 Broken Links...")
    link_warnings = check_broken_links(rules)
    
    # 合并结果
    all_errors = fm_errors + id_errors
    all_warnings = fm_warnings + link_warnings
    
    # 生成报告
    report = generate_report(all_errors, all_warnings, len(rules))
    print("\n" + report)
    
    # 返回状态码
    return 1 if all_errors else 0

if __name__ == "__main__":
    exit(main())
