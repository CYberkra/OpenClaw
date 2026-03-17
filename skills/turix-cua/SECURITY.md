# Security: API Keys

**IMPORTANT**: This directory contains API keys in `config.json`.

**DO NOT commit this file to git!**

## .gitignore Protection

The following files are excluded from git:
- `examples/config.json` (contains API keys)
- `*.log` (conversation logs)
- `.turix_tmp/` (temporary output)

## Setup Instructions

1. Copy `examples/config.json` to `examples/config.json.local`
2. Edit `config.json.local` with your actual API keys
3. Never commit files with real API keys

## API Key Source

Get your API key from: https://turixapi.io/console
