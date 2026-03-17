---
name: turix-linux
description: Computer Use Agent (CUA) for Linux automation using TuriX. Use when you need to perform visual tasks on the Linux desktop, such as opening apps, clicking buttons, or navigating UIs that don't have a CLI or API.
triggers:
  - turix
  - desktop
  - automation
  - gui
  - click
  - screenshot
---

# TuriX-Linux Skill

This skill allows OpenClaw to control the Linux desktop visually using the TuriX Computer Use Agent.

## When to Use

- When asked to perform actions on the Linux desktop (e.g., "Open Firefox and search for AI news").
- When navigating applications that lack command-line interfaces.
- For multi-step visual workflows (e.g., "Find the latest invoice in my email and upload it to the portal").
- When you need the agent to plan, reason, and execute complex tasks autonomously.

## Key Features

### 🤖 Multi-Model Architecture
TuriX uses a sophisticated multi-model system:
- **Brain**: Understands the task and generates step-by-step plans
- **Actor**: Executes precise UI actions based on visual understanding
- **Planner**: Coordinates high-level task decomposition (when `use_plan: true`)
- **Memory**: Maintains context across task steps

### 📋 Skills System
Skills are markdown playbooks that guide the agent for specific domains:
- `github-web-actions`: GitHub navigation, repo search, starring
- `browser-tasks`: General web browser operations
- Custom skills can be added to the `skills/` directory

### 🔄 Resume Capability
The agent can resume interrupted tasks by setting a stable `agent_id`.

## Prerequisites

### 1. Python Environment
Requires Python 3.10+:
```bash
cd skills/turix-cua
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. API Configuration
Edit `examples/config.json` and configure your API keys:
```json
{
  "brain_llm": {
    "provider": "turix",
    "api_key": "your_api_key_here",
    "base_url": "https://turixapi.io/v1",
    "model_name": "gemini-3-flash-preview"
  }
}
```

Get API keys from: https://turixapi.io/console

### 3. Linux Display (X11)
TuriX requires a display to capture screenshots and control the desktop.

**For native Linux:**
- Ensure you have a running X11 session
- The agent will use the active display

**For WSL:**
TuriX in WSL cannot directly control Windows desktop. Options:
1. Use Windows native TuriX (`multi-agent-windows` branch)
2. Install an X server (VcXsrv) and Linux GUI apps

## Running TuriX

### Basic Task
```bash
./skills/turix-cua/OpenCLaw_TuriX_skill/scripts/run_turix.sh "Open Chrome and go to github.com"
```

### Resume Interrupted Task
```bash
./skills/turix-cua/OpenCLaw_TuriX_skill/scripts/run_turix.sh --resume my-task-001
```

### Background Mode
```bash
./skills/turix-cua/OpenCLaw_TuriX_skill/scripts/run_turix.sh "Search AI news" --background
```

### Dry Run (Check Config)
```bash
./skills/turix-cua/OpenCLaw_TuriX_skill/scripts/run_turix.sh --dry-run
```

## Tips for Effective Tasks

**✅ Good Examples:**
- "Open Firefox, go to google.com, search for 'TuriX AI'"
- "Open Settings, change the wallpaper"
- "Open file manager, navigate to Documents, create a new folder"

**❌ Avoid:**
- Vague instructions: "Help me" or "Fix this"
- Impossible actions: "Delete all files"
- Tasks requiring root permissions without warning

**💡 Best Practices:**
1. Be specific about the target application
2. Break complex tasks into clear steps
3. Do not mention precise screen coordinates

## Hotkeys

- **Force Stop**: `Ctrl+Shift+2` - Immediately stops the agent

## Monitoring & Logs

Logs are saved to `.turix_tmp/logging.log` in the project directory:
```bash
tail -f skills/turix-cua/.turix_tmp/logging.log
```

Check also:
- `brain_llm_interactions.log_brain_*.txt` - Brain model conversations
- `actor_llm_interactions.log_actor_*.txt` - Actor model conversations

## Troubleshooting

### Common Issues

| Error | Solution |
|-------|----------|
| `No display found` | Ensure X11 is running or use Xvfb for headless |
| `API key invalid` | Check config.json and verify API keys |
| `Module not found` | Activate venv: `source venv/bin/activate` |
| `Permission denied` | Run script with `bash` or make executable |

### Checking if TuriX is Running

```bash
# Check process
ps aux | grep "python.*main.py" | grep -v grep

# Check logs
tail -f skills/turix-cua/.turix_tmp/logging.log
```

## Architecture

```
User Request
     ↓
[OpenClaw] → [TuriX Skill] → [run_turix.sh] → [TuriX Agent]
                                              ↓
                    ┌─────────────────────────┼─────────────────────────┐
                    ↓                         ↓                         ↓
               [Planner]                 [Brain]                  [Memory]
                    ↓                         ↓                         ↓
                                         [Actor] ───→ [Controller] ───→ [Linux UI]
```

## Advanced Configuration

Edit `examples/config.json` for advanced options:

| Option | Description | Default |
|--------|-------------|---------|
| `use_plan` | Enable planning for complex tasks | true |
| `use_skills` | Enable skill selection | true |
| `max_steps` | Maximum steps limit | 100 |
| `max_actions_per_step` | Actions per step | 5 |
| `force_stop_hotkey` | Custom stop hotkey | "ctrl+shift+2" |
| `memory_budget` | Memory context size | 2000 |

## WSL Specific Notes

When running in WSL:
- TuriX runs in the Linux environment
- Cannot directly control Windows applications
- For Windows desktop automation, use the Windows branch

To use Linux GUI apps in WSL:
1. Install VcXsrv on Windows
2. In WSL: `export DISPLAY=:0`
3. Install GUI apps: `sudo apt install firefox`
