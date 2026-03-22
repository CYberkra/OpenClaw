@echo off
echo 🌸 启动每日时报服务器...
echo 📰 访问地址: http://localhost:8090
echo.
cd /d C:\Users\Linn\.openclaw\daily-newspaper
start http://localhost:8090
uv run python C:\Users\Linn\.openclaw\workspace\skills\daily-newspaper\scripts\server.py
pause
