#!/bin/bash
# OpenClaw 磁盘空间监控脚本
# 建议：每日检查（通过 cron 或 heartbeat）

set -e

WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
ALERT_THRESHOLD=80  # 磁盘使用率超过 80% 告警
LOG_FILE="$WORKSPACE_DIR/logs/disk-monitor.log"

# 获取磁盘使用率（Windows WSL 或 Linux）
get_disk_usage() {
    if command -v wsl.exe &> /dev/null; then
        # WSL 环境
        df -h "$WORKSPACE_DIR" | awk 'NR==2 {print $5}' | sed 's/%//'
    else
        # Linux 环境
        df -h "$WORKSPACE_DIR" | awk 'NR==2 {print $5}' | sed 's/%//'
    fi
}

# 获取 workspace 大小
get_workspace_size() {
    du -sh "$WORKSPACE_DIR" 2>/dev/null | cut -f1
}

# 获取大文件列表（Top 10）
get_large_files() {
    find "$WORKSPACE_DIR" -type f -exec du -h {} + 2>/dev/null | sort -rh | head -10
}

DISK_USAGE=$(get_disk_usage)
WORKSPACE_SIZE=$(get_workspace_size)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# 记录日志
echo "[$TIMESTAMP] 磁盘检查 - 使用率: ${DISK_USAGE}%, Workspace: $WORKSPACE_SIZE" | tee -a "$LOG_FILE"

# 检查是否超过阈值
if [ "$DISK_USAGE" -gt "$ALERT_THRESHOLD" ]; then
    ALERT_MSG="⚠️ 磁盘空间告警: 使用率 ${DISK_USAGE}% (阈值: ${ALERT_THRESHOLD}%)

Workspace 大小: $WORKSPACE_SIZE

Top 10 大文件:
$(get_large_files)

建议操作:
1. 运行清理脚本: ./scripts/auto-cleanup.sh
2. 归档旧报告到外部存储
3. 检查是否有重复下载的大文件"

    echo "$ALERT_MSG" | tee -a "$LOG_FILE"
    
    # 如果有 Discord webhook，可以发送告警
    if [ -n "$DISCORD_WEBHOOK_URL" ]; then
        curl -s -X POST "$DISCORD_WEBHOOK_URL" \
            -H "Content-Type: application/json" \
            -d "{\"content\": \"$ALERT_MSG\"}" || true
    fi
    
    exit 1
else
    echo "  ✓ 磁盘空间正常 (${DISK_USAGE}%)" | tee -a "$LOG_FILE"
    exit 0
fi
