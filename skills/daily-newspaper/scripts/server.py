"""
Daily Newspaper Web Server
持久化 HTTP 服务器，用于提供报纸内容
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8090
DIRECTORY = Path.home() / ".openclaw" / "daily-newspaper"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def log_message(self, format, *args):
        # 简化日志输出
        print(f"[{self.log_date_time_string()}] {args[0]}")

def run_server():
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🌸 每日时报服务器启动")
        print(f"📰 访问地址: http://localhost:{PORT}")
        print(f"📂 服务目录: {DIRECTORY}")
        print(f"按 Ctrl+C 停止服务器\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 服务器已停止")

if __name__ == '__main__':
    run_server()
