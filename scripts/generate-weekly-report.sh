#!/bin/bash
# OpenClaw 周报自动生成脚本
# 建议：每周日运行（通过 cron 或 heartbeat）

set -e

WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
REPORTS_DIR="$WORKSPACE_DIR/reports"
WEEK_START=$(date -d "last sunday" +%Y-%m-%d 2>/dev/null || date -v-sun +%Y-%m-%d)
WEEK_END=$(date +%Y-%m-%d)
WEEK_NUM=$(date +%U)
YEAR=$(date +%Y)

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 生成周报..."

# 收集本周 memory 文件
WEEKLY_MEMORIES=$(find "$WORKSPACE_DIR/memory" -name "2026-*.md" -newer "$WORKSPACE_DIR/memory/2026-01-01.md" 2>/dev/null | sort || echo "")

# 统计本周完成的任务
cat > "$REPORTS_DIR/weekly_report_${YEAR}_W${WEEK_NUM}.md" << EOF
# 周报 ${YEAR} 第 ${WEEK_NUM} 周 (${WEEK_START} ~ ${WEEK_END})

## 本周概况

| 指标 | 数值 |
|------|------|
| 日期范围 | ${WEEK_START} ~ ${WEEK_END} |
| 记忆文件数 | $(echo "$WEEKLY_MEMORIES" | wc -l) |

## 完成的任务

EOF

# 提取每个 memory 文件的关键信息
for file in $WEEKLY_MEMORIES; do
    if [ -f "$file" ]; then
        DATE=$(basename "$file" .md)
        echo "### ${DATE}" >> "$REPORTS_DIR/weekly_report_${YEAR}_W${WEEK_NUM}.md"
        echo "" >> "$REPORTS_DIR/weekly_report_${YEAR}_W${WEEK_NUM}.md"
        
        # 提取主要条目（## 开头的行）
        grep "^## " "$file" | head -5 | sed 's/^## /- /' >> "$REPORTS_DIR/weekly_report_${YEAR}_W${WEEK_NUM}.md" || echo "- 记录了日常进展" >> "$REPORTS_DIR/weekly_report_${YEAR}_W${WEEK_NUM}.md"
        
        echo "" >> "$REPORTS_DIR/weekly_report_${YEAR}_W${WEEK_NUM}.md"
    fi
done

# 添加下周计划模板
cat >> "$REPORTS_DIR/weekly_report_${YEAR}_W${WEEK_NUM}.md" << EOF
## 代码提交统计

\`\`\`bash
cd $WORKSPACE_DIR
git log --oneline --since="${WEEK_START}" --until="${WEEK_END}" | wc -l
\`\`\`

## 下周计划

- [ ] 任务1
- [ ] 任务2
- [ ] 任务3

---
*自动生成于 $(date '+%Y-%m-%d %H:%M:%S')*
EOF

echo "  ✓ 周报已生成: reports/weekly_report_${YEAR}_W${WEEK_NUM}.md"

# 推送到 GitHub
cd "$WORKSPACE_DIR"
git add "$REPORTS_DIR/weekly_report_${YEAR}_W${WEEK_NUM}.md"
git commit -m "docs: 自动生成周报 ${YEAR} 第 ${WEEK_NUM} 周" || true
git push memory main || true
git push origin main || true

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 周报生成完成"
