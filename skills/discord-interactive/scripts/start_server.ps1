# Daily Newspaper Service
# 使用 NSSM 或 Windows Service Wrapper 安装为 Windows 服务

# 安装步骤:
# 1. 下载 NSSM: https://nssm.cc/download
# 2. 以管理员身份运行:
#    nssm install DailyNewspaper
# 3. 配置:
#    Path: uv
#    Arguments: run python C:\Users\Linn\.openclaw\workspace\skills\daily-newspaper\scripts\server.py
#    Working directory: C:\Users\Linn\.openclaw\daily-newspaper

# 或者直接使用 Python 后台运行:
# uv run python scripts/server.py

# 启动服务器脚本 (前台运行 - 用于开发)
uv run python scripts/server.py

# 后台运行 (使用 PowerShell)
# Start-Process -WindowStyle Hidden -FilePath "uv" -ArgumentList "run", "python", "scripts/server.py"
