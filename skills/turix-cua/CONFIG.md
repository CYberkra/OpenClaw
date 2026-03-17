# TuriX Configuration Guide

This document explains how to configure TuriX CUA for Linux/WSL environments.

---

## Quick Start

1. **Copy the example config:**
   ```bash
   cd skills/turix-cua
   cp examples/config.json examples/config.json.backup
   ```

2. **Edit the config:**
   ```bash
   nano examples/config.json
   ```

3. **Set your API keys** (see API Configuration below)

---

## Configuration File Structure

The main config file is at `examples/config.json`:

```json
{
  "logging_level": "INFO",
  "output_dir": ".turix_tmp",
  "brain_enable_thinking": false,
  "working_dir_base": "../turix/trainingdata/task",
  "cleanup_previous_runs": true,

  "brain_llm": { ... },
  "actor_llm": { ... },
  "memory_llm": { ... },
  "planner_llm": { ... },

  "agent": { ... }
}
```

---

## API Configuration (Required)

### Getting API Keys

1. Visit: https://turixapi.io/console
2. Create an account or sign in
3. Generate API keys
4. Copy the key to your config

### Model Configuration

Each LLM section (brain, actor, memory, planner) supports:

```json
{
  "provider": "turix",
  "api_key": "your_api_key_here",
  "base_url": "https://turixapi.io/v1",
  "model_name": "model-name"
}
```

### Supported Providers

| Provider | Description |
|----------|-------------|
| `turix` | TuriX hosted models (recommended) |
| `openai` | OpenAI API |
| `anthropic` | Anthropic Claude API |
| `ollama` | Local Ollama instance |
| `google` | Google Gemini API |

### Recommended Model Setup

**For best results on Linux:**
```json
{
  "brain_llm": {
    "provider": "turix",
    "api_key": "your_key",
    "base_url": "https://turixapi.io/v1",
    "model_name": "gemini-3-flash-preview"
  },
  "actor_llm": {
    "provider": "turix",
    "api_key": "your_key",
    "base_url": "https://turixapi.io/v1",
    "model_name": "turix-actor"
  }
}
```

### Using Ollama (Free, Local)

For a completely free setup using local models:

1. Install Ollama: https://ollama.com
2. Pull a vision model:
   ```bash
   ollama pull llava
   # or
   ollama pull llama3.2-vision
   ```
3. Configure TuriX:
   ```json
   {
     "brain_llm": {
       "provider": "ollama",
       "base_url": "http://localhost:11434",
       "model_name": "llava"
     }
   }
   ```

---

## Agent Configuration

The `agent` section controls task execution:

```json
{
  "agent": {
    "task": "Your task description",
    "memory_budget": 2000,
    "summary_memory_budget": 8000,
    "use_search": false,
    "use_skills": true,
    "skills_dir": "skills",
    "skills_max_chars": 4000,
    "use_plan": true,
    "max_actions_per_step": 5,
    "max_steps": 100,
    "target_screen": 1,
    "force_stop_hotkey": "ctrl+shift+2",
    "resume": false,
    "agent_id": null
  }
}
```

### Key Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `task` | string | - | The task to execute |
| `use_plan` | boolean | true | Enable multi-step planning |
| `use_skills` | boolean | true | Enable skill system |
| `max_steps` | int | 100 | Maximum steps per task |
| `max_actions_per_step` | int | 5 | Actions per step |
| `memory_budget` | int | 2000 | Context memory size |
| `resume` | boolean | false | Resume from previous run |
| `agent_id` | string | null | Stable ID for resuming |

---

## Linux Display Configuration

### Native Linux (X11)

TuriX requires an X11 display. On most desktop Linux distributions, this works automatically.

Check your display:
```bash
echo $DISPLAY
# Should output something like :0 or :1
```

### Headless/Server Setup

For headless servers, use Xvfb (virtual framebuffer):

```bash
# Install Xvfb
sudo apt install xvfb

# Run TuriX with virtual display
xvfb-run -a ./run_turix.sh "Your task"

# Or start Xvfb manually
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
./run_turix.sh "Your task"
```

### WSL with VcXsrv

To use Linux GUI apps in WSL:

1. **Install VcXsrv on Windows:**
   - Download from: https://sourceforge.net/projects/vcxsrv/
   - Install and run "XLaunch"
   - Select "Multiple windows" and "Start no client"
   - **Important:** Check "Disable access control"

2. **Configure WSL:**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
   export LIBGL_ALWAYS_INDIRECT=1
   ```

3. **Test display:**
   ```bash
   # Install a GUI app
   sudo apt install x11-apps
   
   # Test
   xclock
   # Should see a clock window on Windows
   ```

4. **Install browser:**
   ```bash
   sudo apt install firefox
   ```

---

## Permissions

### Linux Permissions

TuriX needs access to:
- Display (X11)
- Input devices (keyboard/mouse simulation)
- Screenshot capabilities

These usually work automatically on desktop Linux.

### WSL Permissions

In WSL, permissions depend on Windows host:
- No special setup needed for basic operation
- For full desktop control, use Windows native version

---

## Logging Configuration

Control log verbosity:

```json
{
  "logging_level": "INFO"
}
```

Levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`

Log location: `.turix_tmp/logging.log`

View logs:
```bash
tail -f skills/turix-cua/.turix_tmp/logging.log
```

---

## Advanced Configuration

### Custom Skills Directory

Add your own skill files:

```json
{
  "agent": {
    "use_skills": true,
    "skills_dir": "skills",
    "skills_max_chars": 4000
  }
}
```

Create skill files in `skills/` directory:
```markdown
---
name: my-skill
description: When doing X task
---
# Instructions for the agent
...
```

### Memory Configuration

Adjust for longer/complex tasks:

```json
{
  "agent": {
    "memory_budget": 4000,
    "summary_memory_budget": 16000
  }
}
```

### Hotkey Configuration

Change the emergency stop key:

```json
{
  "agent": {
    "force_stop_hotkey": "ctrl+shift+q"
  }
}
```

---

## Configuration Validation

Test your config without running:

```bash
./OpenCLaw_TuriX_skill/scripts/run_turix.sh --dry-run
```

This checks:
- API keys are set
- Config file is valid JSON
- Required paths exist
- Python version compatibility

---

## Troubleshooting

### "API key not configured"

**Solution:** Edit `examples/config.json` and replace `your_api_key_here` with actual keys.

### "No display found"

**Solutions:**
- Native Linux: Ensure you're in a graphical session
- Headless: Use `xvfb-run`
- WSL: Set up VcXsrv as described above

### "Permission denied"

**Solution:** Make scripts executable:
```bash
chmod +x OpenCLaw_TuriX_skill/scripts/run_turix.sh
```

### Config changes not taking effect

**Solution:** The runner script updates config.json. Either:
- Pass task via command line (script updates config)
- Or edit config directly and don't pass task
