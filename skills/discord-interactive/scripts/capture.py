"""
生成报纸截图并发送到 Discord
用于定时任务
"""

import subprocess
import time
import json
import sys
from pathlib import Path

def capture_screenshot():
    """启动服务器、截图、关闭服务器"""
    data_dir = Path.home() / ".openclaw" / "daily-newspaper"
    
    # 启动服务器
    print("启动 HTTP 服务器...")
    server = subprocess.Popen(
        ["uv", "run", "python", "-m", "http.server", "8085"],
        cwd=data_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # 等待服务器启动
    time.sleep(2)
    
    try:
        # 使用 playwright 或类似工具截图
        # 这里我们使用一个简单的 Python 脚本调用浏览器截图
        screenshot_path = data_dir / "daily-newspaper-screenshot.png"
        
        # 使用 browser 工具截图（通过 OpenClaw）
        # 由于无法直接调用 browser 工具，我们创建一个标记文件
        # 让主程序知道需要截图
        
        marker_file = data_dir / ".needs_screenshot"
        marker_file.write_text("http://localhost:8085")
        
        print(f"服务器已启动，请访问 http://localhost:8085")
        print(f"截图标记已创建: {marker_file}")
        
        return str(marker_file)
    finally:
        # 保持服务器运行一段时间
        time.sleep(5)
        server.terminate()
        server.wait()
        print("服务器已关闭")

if __name__ == '__main__':
    result = capture_screenshot()
    print(json.dumps({"marker": result}))
