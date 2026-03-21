# PinchTab CLI 安装与最小端到端验证报告

- 时间：2026-03-11 22:16~22:23 (Asia/Shanghai)
- 主机：WSL2 Linux
- 目标：安装并启动 PinchTab CLI，按安全参数运行，并验证 `/health` 与 `/snapshot`

## 1) 官方安装方式（README / refs）
已阅读官方 README（`pinchtab/pinchtab`）：

- macOS/Linux 一键安装：
  ```bash
  curl -fsSL https://pinchtab.com/install.sh | bash
  ```
- npm 全局安装：
  ```bash
  npm install -g pinchtab
  ```

同时参考了 skill 内文档：
- `SKILL.md`
- `references/env.md`
- `references/api.md`

## 2) 安装 CLI（系统可用路径）
由于系统全局 npm 目录无写权限（`/usr/lib/node_modules` EACCES），改为用户前缀安装：

```bash
npm install -g pinchtab --prefix ~/.local
```

验证：
```bash
~/.local/bin/pinchtab --version
# pinchtab 0.7.8
```

> 可执行文件位置：`/home/baiiy1/.local/bin/pinchtab`

## 3) 安全参数启动
按要求使用：
- `BRIDGE_BIND=127.0.0.1`
- `BRIDGE_TOKEN`
- `BRIDGE_PROFILE`
- `BRIDGE_PORT=9867`

实际启动命令：

```bash
BRIDGE_BIND=127.0.0.1 \
BRIDGE_TOKEN='ibA40XJjFLO_0XxgfYKS8oqjs7UHuJD8' \
BRIDGE_PROFILE='/home/baiiy1/.pinchtab/automation-profile' \
BRIDGE_PORT=9867 \
CHROME_BINARY='/home/baiiy1/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome' \
~/.local/bin/pinchtab
```

说明：
- 本机无系统 Chrome/Chromium，先通过 Playwright 下载 Chromium 并显式指定 `CHROME_BINARY`。
- 服务日志显示 `BRIDGE_*` 为兼容变量（提示建议改 `PINCHTAB_*`），但可正常工作。

## 4) `/health` 与 `/snapshot` 最小验证

### 4.1 健康检查
```bash
curl -sS -H 'Authorization: Bearer ibA40XJjFLO_0XxgfYKS8oqjs7UHuJD8' \
  http://127.0.0.1:9867/health
```
返回：
```json
{"mode":"dashboard","status":"ok"}
```

### 4.2 打开页面并抓取 snapshot
先导航：
```bash
curl -sS -X POST 'http://127.0.0.1:9867/navigate' \
  -H 'Authorization: Bearer ibA40XJjFLO_0XxgfYKS8oqjs7UHuJD8' \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","newTab":true}'
```
返回（节选）：
```json
{"tabId":"B8DBF9D8375F2EEA1A47467CDB882DC9","title":"Example Domain","url":"https://example.com/"}
```

调用 snapshot：
```bash
curl -sS 'http://127.0.0.1:9867/snapshot?format=compact&filter=interactive&tabId=B8DBF9D8375F2EEA1A47467CDB882DC9' \
  -H 'Authorization: Bearer ibA40XJjFLO_0XxgfYKS8oqjs7UHuJD8'
```
返回（节选）：
```text
# Example Domain | https://example.com/ | 1 nodes
e0:link "Learn more"
```

✅ `/health` 通过，`/snapshot` 通过（含真实页面节点）。

## 5) 停止命令
前台运行时：`Ctrl+C`

后台运行时（示例）：
```bash
pkill -f '^.*pinchtab.*$'
```

更稳妥（按端口）：
```bash
fuser -k 9867/tcp
```

---

## 附：本次遇到的问题与处理

1. **npm 全局安装权限不足（EACCES）**
   - 处理：改用 `--prefix ~/.local`。

2. **首次实例启动超时 / 无系统 Chrome**
   - 错误示例：`chrome/chromium not found`
   - 处理：安装 Playwright Chromium，并设置 `CHROME_BINARY`。

3. **首次 `/navigate` 返回实例未就绪（503）**
   - 处理：待实例拉起后重试 navigate；成功后按 `tabId` 调用 snapshot。
