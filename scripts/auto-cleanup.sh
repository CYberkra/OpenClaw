#!/bin/bash
# OpenClaw Workspace 自动清理脚本
# 建议：每日运行（通过 cron 或 heartbeat）

set -e

WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
LOG_FILE="$WORKSPACE_DIR/logs/cleanup.log"
RETENTION_DAYS=7

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始自动清理..." | tee -a "$LOG_FILE"

# 1. 清理 tmp/ 目录（保留最近 $RETENTION_DAYS 天）
if [ -d "$WORKSPACE_DIR/tmp" ]; then
    find "$WORKSPACE_DIR/tmp" -type f -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
    find "$WORKSPACE_DIR/tmp" -type d -empty -delete 2>/dev/null || true
    echo "  ✓ 清理 tmp/ 目录（>${RETENTION_DAYS}天）" | tee -a "$LOG_FILE"
fi

# 2. 清理 tmp_in/ 目录（临时输入文件）
if [ -d "$WORKSPACE_DIR/tmp_in" ]; then
    find "$WORKSPACE_DIR/tmp_in" -type f -mtime +1 -delete 2>/dev/null || true
    echo "  ✓ 清理 tmp_in/ 目录（>1天）" | tee -a "$LOG_FILE"
fi

# 3. 清理 .cache/ 目录（超过 100MB 时）
if [ -d "$WORKSPACE_DIR/.cache" ]; then
    CACHE_SIZE=$(du -sm "$WORKSPACE_DIR/.cache" | cut -f1)
    if [ "$CACHE_SIZE" -gt 100 ]; then
        find "$WORKSPACE_DIR/.cache" -type f -mtime +3 -delete 2>/dev/null || true
        echo "  ✓ 清理 .cache/ 目录（>${CACHE_SIZE}MB，保留3天）" | tee -a "$LOG_FILE"
    fi
fi

# 4. 清理 logs/ 目录（保留 30 天）
if [ -d "$WORKSPACE_DIR/logs" ]; then
    find "$WORKSPACE_DIR/logs" -type f -mtime +30 -delete 2>/dev/null || true
    echo "  ✓ 清理 logs/ 目录（>30天）" | tee -a "$LOG_FILE"
fi

# 5. 统计清理后磁盘使用情况
DISK_USAGE=$(du -sh "$WORKSPACE_DIR" | cut -f1)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 清理完成，当前 workspace 大小: $DISK_USAGE" | tee -a "$LOG_FILE"

exit 0
