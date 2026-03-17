# TuriX CUA Linux Installation Report

**Date:** 2026-03-17  
**Environment:** WSL2 (Linux 6.6.87.2-microsoft-standard-WSL2)  
**OpenClaw Version:** 2026.3.13  
**Python Version:** 3.10.12

---

## Installation Status

### ✅ Successfully Installed

1. **Repository Cloned**
   - Source: https://github.com/TurixAI/TuriX-CUA
   - Branch: `multi-agent-linux`
   - Location: `/home/baiiy1/.openclaw/workspace/skills/turix-cua`

2. **Virtual Environment Created**
   - Path: `skills/turix-cua/venv/`
   - Python: 3.10.12

3. **Dependencies Installed**
   - All requirements from `requirements.txt` installed
   - Key packages: pyautogui, langchain, playwright, pynput, Pillow

4. **OpenClaw Skill Configured**
   - Location: `skills/turix-cua/OpenCLaw_TuriX_skill/`
   - Linux runner script: `scripts/run_turix.sh`
   - Skill definition: `SKILL.md`

---

## Installation Steps Performed

```bash
# 1. Clone repository with Linux branch
git clone -b multi-agent-linux https://github.com/TurixAI/TuriX-CUA.git turix-cdua
cd turix-cua

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Make scripts executable
chmod +x OpenCLaw_TuriX_skill/scripts/run_turix.sh
```

---

## Environment Information

### System Details
```
OS: Linux (WSL2)
Kernel: 6.6.87.2-microsoft-standard-WSL2
Python: 3.10.12
Display: None (WSL headless)
Xvfb: Available (/usr/bin/Xvfb)
```

### OpenClaw Integration
- Skill path: `~/.openclaw/workspace/skills/turix-cua/`
- Runner script: `OpenCLaw_TuriX_skill/scripts/run_turix.sh`
- Config path: `examples/config.json`

---

## Important Limitations (WSL)

⚠️ **WSL Environment Detected**

TuriX running in **WSL cannot control the Windows desktop** directly. This is a fundamental limitation of WSL's architecture.

### Options for Desktop Automation

1. **For Windows Desktop Automation:**
   - Use the Windows branch of TuriX: `multi-agent-windows`
   - Install TuriX directly on Windows
   - Access via Windows OpenClaw installation

2. **For Linux GUI Apps in WSL:**
   - Install VcXsrv (X server) on Windows
   - Export DISPLAY=:0 in WSL
   - Install Linux GUI apps (Firefox, etc.)
   - TuriX can then control these apps

3. **For Headless Testing:**
   - Use Xvfb (virtual display)
   - Install: `sudo apt install xvfb`
   - Run: `xvfb-run ./run_turix.sh "task"`

---

## Next Steps

### 1. Configure API Keys (Required)

Before running TuriX, you **must** configure API keys:

```bash
# Edit the config file
nano skills/turix-cua/examples/config.json
```

Replace `your_api_key_here` with actual API keys from https://turixapi.io/console

### 2. Test Installation

```bash
# Dry run to validate setup
cd skills/turix-cua
./OpenCLaw_TuriX_skill/scripts/run_turix.sh --dry-run

# Run a test task (requires API keys and display)
./OpenCLaw_TuriX_skill/scripts/run_turix.sh "Take a screenshot"
```

### 3. Verify OpenClaw Integration

```bash
# Check if skill is recognized
openclaw skills info turix-linux

# Or use from OpenClaw chat
turix: Open Chrome and search for AI news
```

---

## Files Created/Modified

| File | Purpose |
|------|---------|
| `skills/turix-cua/` | Main repository |
| `skills/turix-cua/venv/` | Python virtual environment |
| `skills/turix-cua/OpenCLaw_TuriX_skill/scripts/run_turix.sh` | Linux runner script |
| `skills/turix-cua/OpenCLaw_TuriX_skill/SKILL.md` | OpenClaw skill definition |
| `skills/turix-cua/INSTALL.md` | This installation report |
| `skills/turix-cua/CONFIG.md` | Configuration documentation |
| `skills/turix-cua/EXAMPLES.md` | Usage examples |

---

## Issues Encountered and Solutions

### Issue 1: Windows PowerShell Script
**Problem:** Repository came with Windows PowerShell script (`run_turix.ps1`), not suitable for Linux.

**Solution:** Created new Linux bash script `run_turix.sh` with equivalent functionality:
- Task passing via command line
- Config file updates
- Background mode support
- Dry-run validation
- WSL detection and warnings

### Issue 2: WSL Display Limitation
**Problem:** WSL2 has no native display, preventing GUI automation.

**Solution:** 
- Added WSL detection to runner script
- Shows warning with helpful instructions
- Offers options for X server setup or Windows native version

### Issue 3: SKILL.md for macOS
**Problem:** Original SKILL.md was for macOS (`turix-mac`).

**Solution:** Created new SKILL.md specific to Linux with:
- Linux-specific instructions
- WSL considerations
- X11 display requirements
- Native Linux paths and commands

---

## Verification Checklist

- [x] Repository cloned successfully
- [x] Linux branch checked out
- [x] Virtual environment created
- [x] Dependencies installed
- [x] Runner script created and executable
- [x] Skill documentation created
- [ ] API keys configured (user action required)
- [ ] Display configured (if needed, user action)
- [ ] Test task executed (pending API keys)

---

## Support

- **TuriX Discord:** https://discord.gg/yaYrNAckb5
- **TuriX API Console:** https://turixapi.io/console
- **GitHub Issues:** https://github.com/TurixAI/TuriX-CUA/issues
