#!/bin/bash
# OpenClaw Memory.md 定期整理脚本
# 建议：每月运行一次（通过 cron 或 heartbeat）

set -e

WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
MEMORY_FILE="$WORKSPACE_DIR/MEMORY.md"
ARCHIVE_DIR="$WORKSPACE_DIR/archive/memory-snapshots"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始整理 Memory.md..."

# 创建归档目录
mkdir -p "$ARCHIVE_DIR"

# 备份当前 Memory.md
if [ -f "$MEMORY_FILE" ]; then
    cp "$MEMORY_FILE" "$ARCHIVE_DIR/MEMORY_$(date +%Y%m%d).md"
    echo "  ✓ 已备份到 $ARCHIVE_DIR/MEMORY_$(date +%Y%m%d).md"
fi

# 统计信息
echo "  📊 Memory.md 统计:"
echo "    - 行数: $(wc -l < "$MEMORY_FILE" || echo 0)"
echo "    - 大小: $(du -h "$MEMORY_FILE" | cut -f1 || echo 0)"

# 检查是否需要清理（超过 500 行则建议归档旧内容）
LINE_COUNT=$(wc -l < "$MEMORY_FILE" || echo 0)
if [ "$LINE_COUNT" -gt 500 ]; then
    echo "  ⚠️ Memory.md 超过 500 行，建议归档旧内容"
    
    # 提取归档建议
    echo "    建议归档以下内容："
    grep "^## " "$MEMORY_FILE" | tail -20 | head -10 | sed 's/^## /    - /' || echo "    - 无明确标题段落"
fi

# 检查重复主题（简单启发式：检查重复的二级标题）
echo "  🔍 检查重复主题..."
DUPLICATE_TOPICS=$(grep "^## " "$MEMORY_FILE" | sort | uniq -d | head -5)
if [ -n "$DUPLICATE_TOPICS" ]; then
    echo "    发现可能重复的主题："
    echo "$DUPLICATE_TOPICS" | sed 's/^## /    - /'
else
    echo "    ✓ 未发现明显重复"
fi

# 整理建议
cat >> "$MEMORY_FILE" << EOF

---

## 整理记录 $(date +%Y-%m-%d)

- 备份位置: archive/memory-snapshots/MEMORY_$(date +%Y%m%d).md
- 行数: $LINE_COUNT
- 状态: $(if [ "$LINE_COUNT" -gt 500 ]; then echo "⚠️ 建议归档"; else echo "✓ 正常"; fi)

EOF

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Memory.md 整理完成"

# 提交变更
cd "$WORKSPACE_DIR"
git add "$MEMORY_FILE" "$ARCHIVE_DIR"
git commit -m "chore: 月度 Memory.md 整理 ($(date +%Y-%m-%d))" || true
git push memory main || true
git push origin main || true
