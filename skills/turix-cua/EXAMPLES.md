# TuriX Usage Examples

This document provides practical examples for using TuriX CUA with OpenClaw on Linux.

---

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Web Browser Tasks](#web-browser-tasks)
3. [File Management](#file-management)
4. [Working with Skills](#working-with-skills)
5. [Background Tasks](#background-tasks)
6. [Resuming Tasks](#resuming-tasks)
7. [From OpenClaw Chat](#from-openclaw-chat)
8. [Troubleshooting Examples](#troubleshooting-examples)

---

## Basic Usage

### Simple Task

```bash
cd ~/.openclaw/workspace/skills/turix-cua
./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Open Firefox and go to google.com"
```

### Screenshot Task

```bash
./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Take a screenshot of the desktop"
```

### Dry Run (Test Config)

```bash
./OpenCLaw_TuriX_skill/scripts/run_turix.sh --dry-run
```

---

## Web Browser Tasks

### Search and Navigate

```bash
./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Open Chrome, go to github.com, and search for 'machine learning'"
```

### GitHub Actions

```bash
./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Go to GitHub, find the TurixAI/TuriX-CUA repo, and star it"
```

### Form Filling

```bash
./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Open Firefox, go to google.com, search for 'weather in Beijing'"
```

---

## File Management

### Create Folders

```bash
./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Open file manager, go to Documents, create a new folder called 'Projects'"
```

### Take and Save Screenshot

```bash
./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Take a screenshot and save it to the Desktop"
```

---

## Working with Skills

Skills are markdown playbooks that help TuriX perform specific tasks better.

### Enable Skills

Skills are enabled by default (`use_skills: true`).

### Using Built-in Skills

```bash
# The planner will automatically select relevant skills
./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Search for turix-cua on GitHub and star it"
# → Uses 'github-web-actions' skill
```

### Create Custom Skill

1. Create a file in `skills/` directory:

```bash
nano skills/my-custom-task.md
```

2. Add content:

```markdown
---
name: my-custom-task
description: When performing my specific workflow
---

# My Custom Task

## Steps
1. Open the application
2. Navigate to Settings
3. Click on the specific option
4. Save changes

## Important Notes
- Wait for loading indicators
- Confirm before saving
- Check the result
```

3. Use it:

```bash
./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Do my custom task"
```

---

## Background Tasks

Run tasks without blocking the terminal:

```bash
# Run in background
./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Search AI news and summarize" --background

# Check progress
tail -f ~/.openclaw/workspace/skills/turix-cua/.turix_tmp/logging.log

# Check if still running
ps aux | grep "python.*main.py"
```

---

## Resuming Tasks

If a task is interrupted, resume it:

```bash
# First, assign an agent ID when starting
# (Edit config.json: "agent_id": "my-task-001")

# Then resume
./OpenCLaw_TuriX_skill/scripts/run_turix.sh --resume my-task-001
```

---

## From OpenClaw Chat

Once configured, you can invoke TuriX directly from OpenClaw chat:

### Direct Invocation

```
turix: Open Chrome and go to YouTube
turix: Take a screenshot of the desktop
turix: Open file manager and create a folder called Work
```

### With OpenClaw exec

```python
# From an OpenClaw agent
exec(command='''
./skills/turix-cua/OpenCLaw_TuriX_skill/scripts/run_turix.sh "Open Firefox and search for AI news"
''', workdir='/home/baiiy1/.openclaw/workspace', timeout=300)
```

---

## Troubleshooting Examples

### Test Display

```bash
# Check if display is available
echo $DISPLAY

# Test with x11-apps
sudo apt install x11-apps
xclock
```

### Check Logs

```bash
# Real-time log monitoring
tail -f ~/.openclaw/workspace/skills/turix-cua/.turix_tmp/logging.log

# View all logs
ls -la ~/.openclaw/workspace/skills/turix-cua/.turix_tmp/
```

### Verify Installation

```bash
# Check Python
python3 --version  # Should be 3.10+

# Check virtual environment
ls -la ~/.openclaw/workspace/skills/turix-cua/venv/

# Check config
cat ~/.openclaw/workspace/skills/turix-cua/examples/config.json | grep -v api_key
```

### Kill Stuck Process

```bash
# Find TuriX process
ps aux | grep "python.*main.py"

# Kill it
pkill -f "python.*main.py"
```

---

## WSL-Specific Examples

### Setup for WSL

```bash
# Install VcXsrv on Windows first
# Then in WSL:

# Add to ~/.bashrc
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
export LIBGL_ALWAYS_INDIRECT=1

# Reload
source ~/.bashrc

# Install Firefox
sudo apt update
sudo apt install firefox

# Test
turix: Open Firefox and go to google.com
```

### Headless Mode in WSL

```bash
# Install Xvfb
sudo apt install xvfb

# Run with virtual display
xvfb-run -a ./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Take a screenshot"
```

---

## Example: Complete Workflow

### Research and Document

```bash
#!/bin/bash
# research_workflow.sh

TURIX_ROOT="$HOME/.openclaw/workspace/skills/turix-cua"

# Step 1: Search for AI news
echo "Starting research..."
$TURIX_ROOT/OpenCLaw_TuriX_skill/scripts/run_turix.sh \
    "Open Chrome, search for 'AI news 2026', open the first 3 results" \
    --background

# Wait for completion
sleep 30

# Step 2: Check logs
echo "Task progress:"
tail -20 $TURIX_ROOT/.turix_tmp/logging.log
```

---

## Tips for Better Results

### ✅ Good Task Descriptions

```bash
# Be specific about the app
./run_turix.sh "Open Firefox, not Chrome"

# Break complex tasks
./run_turix.sh "Open file manager"
./run_turix.sh "Create a new folder called Projects"

# Include verification
./run_turix.sh "Open settings and check if dark mode is enabled"
```

### ❌ Avoid

```bash
# Vague instructions
./run_turix.sh "Help me"

# System-level tasks without warning
./run_turix.sh "Delete all files"

# Impossible tasks
./run_turix.sh "Hack into the system"
```

---

## Advanced Examples

### With Custom Config

```bash
# Edit config directly, don't pass task
nano examples/config.json

# Then run without task (uses config)
./OpenCLaw_TuriX_skill/scripts/run_turix.sh
```

### Disable Features

```bash
# No planning (faster, less intelligent)
./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Simple task" --no-plan

# No skills
./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Task" --no-skills
```

### Monitor Multiple Tasks

```bash
# Terminal 1: Run task
./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Long task" --background

# Terminal 2: Monitor
watch -n 5 'ls -lt ~/.openclaw/workspace/skills/turix-cua/.turix_tmp/*.txt'
```
