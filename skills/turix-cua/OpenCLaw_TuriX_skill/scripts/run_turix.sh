#!/bin/bash
# TuriX Linux Runner Script for OpenClaw
# Usage: ./run_turix.sh "Your task description" [--background] [--dry-run]

set -e

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TURIX_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CONFIG_PATH="$TURIX_ROOT/examples/config.json"
MAIN_PY="$TURIX_ROOT/examples/main.py"

# Default values
TASK=""
BACKGROUND=false
DRY_RUN=false
RESUME=false
AGENT_ID=""
USE_PLAN=true
USE_SKILLS=true

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Help message
show_help() {
    echo "TuriX Linux Runner"
    echo ""
    echo "Usage: $0 [OPTIONS] \"Task description\""
    echo ""
    echo "Options:"
    echo "  --background    Run in background"
    echo "  --dry-run       Validate config without running"
    echo "  --resume ID     Resume with specific agent ID"
    echo "  --no-plan       Disable planner"
    echo "  --no-skills     Disable skills"
    echo "  -h, --help      Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 \"Open Firefox and search for OpenClaw\""
    echo "  $0 --background \"Take a screenshot\""
    echo "  $0 --resume my-task-001"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --background)
            BACKGROUND=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --resume)
            RESUME=true
            if [[ -n "$2" && ! "$2" =~ ^-- ]]; then
                AGENT_ID="$2"
                shift 2
            else
                echo -e "${RED}Error: --resume requires an agent ID${NC}"
                exit 1
            fi
            ;;
        --no-plan)
            USE_PLAN=false
            shift
            ;;
        --no-skills)
            USE_SKILLS=false
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
        *)
            TASK="$1"
            shift
            ;;
    esac
done

# Check if running in WSL
IS_WSL=false
if grep -qi microsoft /proc/version 2>/dev/null; then
    IS_WSL=true
fi

# Check for required files
if [[ ! -f "$CONFIG_PATH" ]]; then
    echo -e "${RED}Error: config.json not found at $CONFIG_PATH${NC}"
    exit 1
fi

if [[ ! -f "$MAIN_PY" ]]; then
    echo -e "${RED}Error: main.py not found at $MAIN_PY${NC}"
    exit 1
fi

# Check if API keys are configured
if grep -q "your_api_key_here" "$CONFIG_PATH"; then
    echo -e "${YELLOW}Warning: API keys not configured in config.json${NC}"
    echo "Please edit $CONFIG_PATH and add your API keys"
    echo "Get API keys from: https://turixapi.io/console"
    exit 1
fi

# Dry run - just validate
if [[ "$DRY_RUN" == true ]]; then
    echo -e "${GREEN}✓ Config validation passed${NC}"
    echo "  Config: $CONFIG_PATH"
    echo "  TuriX Root: $TURIX_ROOT"
    echo "  Task: ${TASK:-'(not specified)'}}"
    echo "  Resume: $RESUME"
    echo "  Use Plan: $USE_PLAN"
    echo "  Use Skills: $USE_SKILLS"
    
    if [[ "$IS_WSL" == true ]]; then
        echo ""
        echo -e "${YELLOW}Note: Running in WSL environment${NC}"
        echo "  TuriX cannot control Windows desktop from WSL."
        echo "  For Windows desktop automation, use the Windows branch:"
        echo "    git checkout multi-agent-windows"
        echo "  Or install TuriX directly on Windows."
    fi
    exit 0
fi

# Check if we have a virtual environment
VENV_PYTHON="$TURIX_ROOT/venv/bin/python"
if [[ ! -f "$VENV_PYTHON" ]]; then
    echo -e "${YELLOW}Virtual environment not found, trying system Python...${NC}"
    PYTHON_CMD="python3"
else
    PYTHON_CMD="$VENV_PYTHON"
fi

# Check if Python is available
if ! command -v "$PYTHON_CMD" &> /dev/null; then
    echo -e "${RED}Error: Python not found${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | grep -oP '\d+\.\d+')
REQUIRED_VERSION="3.10"
if [[ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]]; then
    echo -e "${RED}Error: Python $PYTHON_VERSION is installed, but Python 3.10+ is required${NC}"
    exit 1
fi

echo -e "${GREEN}TuriX Linux Runner${NC}"
echo "===================="
echo "Config: $CONFIG_PATH"
echo "Python: $($PYTHON_CMD --version)"
echo ""

# WSL Warning
if [[ "$IS_WSL" == true ]]; then
    echo -e "${YELLOW}⚠ WSL Environment Detected${NC}"
    echo "TuriX running in WSL cannot control the Windows desktop."
    echo "For Windows automation, please use the Windows native version."
    echo ""
    echo "If you have an X server (VcXsrv) installed on Windows:"
    echo "  1. Start VcXsrv on Windows"
    echo "  2. Export DISPLAY=:0 in WSL"
    echo "  3. Install Linux GUI apps: sudo apt install firefox"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# Update config with task if provided
if [[ -n "$TASK" ]]; then
    echo "Setting task: $TASK"
    
    # Use Python to safely update JSON
    $PYTHON_CMD << PYEOF
import json
import os

config_path = "$CONFIG_PATH"

with open(config_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data['agent']['task'] = """$TASK"""
data['agent']['resume'] = $([ "$RESUME" == true ] && echo "true" || echo "false")
data['agent']['use_plan'] = $([ "$USE_PLAN" == true ] && echo "true" || echo "false")
data['agent']['use_skills'] = $([ "$USE_SKILLS" == true ] && echo "true" || echo "false")

if "$RESUME" and "$AGENT_ID":
    data['agent']['agent_id'] = "$AGENT_ID"

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✓ Config updated")
PYEOF
fi

# Change to examples directory
cd "$TURIX_ROOT/examples"

# Run TuriX
export PYTHONPATH="$TURIX_ROOT:$PYTHONPATH"

if [[ "$BACKGROUND" == true ]]; then
    echo -e "${GREEN}Starting TuriX in background...${NC}"
    nohup $PYTHON_CMD "$MAIN_PY" > "$TURIX_ROOT/.turix_tmp/turix.out" 2>&1 &
    PID=$!
    echo "PID: $PID"
    echo "Output: $TURIX_ROOT/.turix_tmp/turix.out"
    echo "Logs: $TURIX_ROOT/.turix_tmp/logging.log"
    echo ""
    echo "To check progress:"
    echo "  tail -f $TURIX_ROOT/.turix_tmp/logging.log"
else
    echo -e "${GREEN}Starting TuriX...${NC}"
    echo "Press Ctrl+C to stop"
    echo ""
    $PYTHON_CMD "$MAIN_PY"
fi
