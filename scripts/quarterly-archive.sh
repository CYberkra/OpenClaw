#!/bin/bash
# OpenClaw 旧文件自动归档脚本
# 建议：每季度运行一次

set -e

WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
ARCHIVE_DIR="$WORKSPACE_DIR/archive"
QUARTER=$(date +%Y-Q%q)

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始季度归档 (${QUARTER})..."

# 1. 归档旧 memory 文件（90天前）
echo "  📁 归档旧 memory 文件..."
mkdir -p "$ARCHIVE_DIR/$QUARTER/memory"
find "$WORKSPACE_DIR/memory" -name "2026-*.md" -mtime +90 -exec mv {} "$ARCHIVE_DIR/$QUARTER/memory/" \; 2>/dev/null || true
echo "    ✓ 已归档 $(ls "$ARCHIVE_DIR/$QUARTER/memory/" 2>/dev/null | wc -l) 个文件"

# 2. 归档旧报告（60天前）
echo "  📁 归档旧报告..."
mkdir -p "$ARCHIVE_DIR/$QUARTER/reports"
find "$WORKSPACE_DIR/reports" -name "*.md" -mtime +60 -exec mv {} "$ARCHIVE_DIR/$QUARTER/reports/" \; 2>/dev/null || true
find "$WORKSPACE_DIR/reports" -name "*.html" -mtime +60 -exec mv {} "$ARCHIVE_DIR/$QUARTER/reports/" \; 2>/dev/null || true
echo "    ✓ 已归档 $(ls "$ARCHIVE_DIR/$QUARTER/reports/" 2>/dev/null | wc -l) 个文件"

# 3. 清理 tmp 目录（30天前）
echo "  🗑️ 清理 tmp 目录..."
find "$WORKSPACE_DIR/tmp" -type f -mtime +30 -delete 2>/dev/null || true
echo "    ✓ 清理完成"

# 4. 生成归档清单
cat > "$ARCHIVE_DIR/$QUARTER/MANIFEST.md" << EOF
# 归档清单 ${QUARTER}

归档时间: $(date '+%Y-%m-%d %H:%M:%S')

## 归档内容

- memory/: $(ls "$ARCHIVE_DIR/$QUARTER/memory/" 2>/dev/null | wc -l) 个文件
- reports/: $(ls "$ARCHIVE_DIR/$QUARTER/reports/" 2>/dev/null | wc -l) 个文件

## 存储位置

- $ARCHIVE_DIR/$QUARTER/

---
*自动生成*
EOF

echo "  ✓ 归档清单已生成: $ARCHIVE_DIR/$QUARTER/MANIFEST.md"

# 提交变更
cd "$WORKSPACE_DIR"
git add "$ARCHIVE_DIR/$QUARTER"
git commit -m "chore: 季度归档 ${QUARTER}" || true
git push memory main || true
git push origin main || true

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 季度归档完成"
