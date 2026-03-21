#!/bin/bash
# Auto Project Launcher Trigger Script
# 当检测到项目启动意图时，自动创建 thread 并调用 project-bootstrap

# 参数:
# $1: 用户原始消息
# $2: 当前频道ID
# $3: 当前会话ID

USER_MSG="$1"
CHANNEL_ID="$2"
SESSION_ID="$3"

# 提取项目名称
PROJECT_NAME=$(echo "$USER_MSG" | sed -E 's/.*(创建|新建|开).{0,5}(子分区|thread).{0,10}(做|处理|跟进|跟踪|执行|：|:)//i' | sed 's/^[[:space:]]*//' | head -c 50)

# 推断项目类型
if echo "$USER_MSG" | grep -qiE "(优化|实现|开发|代码|编程)"; then
    PROJECT_TYPE="coding"
elif echo "$USER_MSG" | grep -qiE "(调研|研究|文献|综述|调查)"; then
    PROJECT_TYPE="research"
elif echo "$USER_MSG" | grep -qiE "(审查|检查|评估|review)"; then
    PROJECT_TYPE="review"
else
    PROJECT_TYPE="mixed"
fi

# 推断优先级
if echo "$USER_MSG" | grep -qiE "(紧急|马上|立刻|高优先级|urgent)"; then
    PRIORITY="high"
else
    PRIORITY="normal"
fi

# 生成时间戳
TIMESTAMP=$(date +%Y%m%d%H%M%S)
EDL_ID="${TIMESTAMP}-${PROJECT_NAME// /-}-bootstrap"

# 输出配置
cat << EOF
{
  "project_name": "${PROJECT_NAME// /-}",
  "project_type": "$PROJECT_TYPE",
  "channel_id": "$CHANNEL_ID",
  "goal": "$PROJECT_NAME",
  "priority": "$PRIORITY",
  "edl_id": "$EDL_ID",
  "auto_trigger": true
}
EOF
