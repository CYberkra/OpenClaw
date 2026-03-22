"""
Daily Newspaper API - 通过 skill 接口管理报纸
提供 HTTP API 用于编辑和更新报纸内容
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
from urllib.parse import parse_qs, urlparse

class NewspaperAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/api/status':
            self.send_json({"status": "ok", "service": "daily-newspaper-api"})
        elif path == '/api/regenerate':
            # 重新生成报纸
            try:
                result = subprocess.run(
                    ['uv', 'run', 'python', 'scripts/manager.py', 'generate'],
                    cwd='C:/Users/Linn/.openclaw/workspace/skills/daily-newspaper',
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                self.send_json({"status": "success", "output": result.stdout})
            except Exception as e:
                self.send_json({"status": "error", "message": str(e)}, 500)
        else:
            self.send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/api/add-news':
            # 添加新闻
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            # TODO: 调用 manager.py 添加新闻
            self.send_json({"status": "success", "message": "News added", "data": data})
        else:
            self.send_json({"error": "Not found"}, 404)
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def log_message(self, format, *args):
        # 静默日志
        pass

def run_api_server(port=8091):
    server = HTTPServer(('localhost', port), NewspaperAPIHandler)
    print(f"Daily Newspaper API running at http://localhost:{port}")
    server.serve_forever()

if __name__ == '__main__':
    run_api_server()
