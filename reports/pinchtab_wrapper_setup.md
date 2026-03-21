# PinchTab 接入试点（受控）实施说明

> 目标：新增 **PinchTab HTTP sidecar** 作为并行能力，不替代现有 `browser` 工具链。

## 0. 结论先行

已完成试点最小实现：
1. 最小 `pinchtab-wrapper`（HTTP sidecar）与安全默认值 ✅
2. Discord 输出脱敏钩子 ✅
3. 启动 / 配置 / 回滚步骤 ✅
4. 明确并行关系（不替代现有 browser）✅
5. 环境变量 / 端口 / 权限清单 ✅

实现文件：
- `scripts/pinchtab_wrapper/pinchtab_wrapper.py`
- `scripts/pinchtab_wrapper/discord_redact.py`
- `scripts/pinchtab_wrapper/.env.example`
- `reports/pinchtab_wrapper_daemon.md`（常驻 + 自动重启 + token透传 + 实测记录）

---

## 1) 最小架构（受控）

```text
OpenClaw 主流程
   ├─ 现有 browser 工具（保持不变）
   └─ 新增并行路径：PinchTab wrapper (127.0.0.1:39091)
          └─ 转发到 PinchTab 上游 (127.0.0.1:39090)
```

**设计原则：**
- 默认仅本机回环地址（`127.0.0.1`）监听，避免外网暴露。
- 默认启用 `X-Wrapper-Token` 鉴权。
- 默认仅允许白名单路径前缀 + 白名单 HTTP 方法。
- 超时 + body 大小限制，避免资源滥用。
- 最小日志（不打印请求体/敏感头）。

---

## 2) 安全默认值（已落地）

`pinchtab_wrapper.py` 默认行为：
- 监听：`127.0.0.1:39091`
- 上游：`http://127.0.0.1:39090`
- 鉴权：`PINCHTAB_REQUIRE_TOKEN=1`
- 方法白名单：`GET,POST`
- 路径白名单：`/health,/v1/`
- 超时：`15s`
- 最大请求体：`65536 bytes`

**建议生产收口：**
- `PINCHTAB_WRAPPER_TOKEN` 使用高熵随机值（>=32 chars）。
- 如无必要，不把 `PINCHTAB_WRAPPER_HOST` 改为 `0.0.0.0`。
- 若必须对外开放，需叠加反向代理 + mTLS / IP allowlist。

---

## 3) Discord 输出脱敏钩子

实现：`scripts/pinchtab_wrapper/discord_redact.py`

能力：
- 文本脱敏：`Bearer token`、`cookie`、`set-cookie`、`api_key/secret/token/password`、常见 key 前缀（`sk-`、`ghp_`、`xox*`）。
- JSON 递归脱敏：对 payload 的敏感字段和嵌套内容统一替换为 `***REDACTED***`。

### 接入点建议

在实际调用 `message.send(channel=discord, ...)` 前执行：
1. `redact_message_for_discord(message, components_json)`
2. 用返回值覆盖发送内容。

示例（伪代码）：

```python
from scripts.pinchtab_wrapper.discord_redact import redact_message_for_discord

safe = redact_message_for_discord(message=raw_text, components_json=raw_components)
# message.send(channel="discord", message=safe.get("message"), components=safe.get("components"))
```

---

## 4) 启动 / 配置 / 验证

### 4.1 准备配置

```bash
cd /home/baiiy1/.openclaw/workspace
cp scripts/pinchtab_wrapper/.env.example scripts/pinchtab_wrapper/.env
# 编辑 .env，至少修改 PINCHTAB_WRAPPER_TOKEN
```

### 4.2 启动 wrapper

```bash
set -a
source scripts/pinchtab_wrapper/.env
set +a
python3 scripts/pinchtab_wrapper/pinchtab_wrapper.py
```

### 4.3 健康检查

```bash
curl -s http://127.0.0.1:39091/healthz | jq .
```

### 4.4 鉴权检查（应返回 401）

```bash
curl -i http://127.0.0.1:39091/v1/test
```

### 4.5 带 token 请求

```bash
curl -i -H "X-Wrapper-Token: $PINCHTAB_WRAPPER_TOKEN" \
  http://127.0.0.1:39091/v1/test
```

---

## 5) 回滚步骤（快速）

> 目标：不影响现有 browser 能力。

1. 停止 `pinchtab_wrapper.py` 进程。
2. 删除/注释所有调用 `http://127.0.0.1:39091` 的新增配置。
3. 保留现有 `browser` 路径不变（无需改动）。
4. 可选：归档 `scripts/pinchtab_wrapper/` 到备份目录。

**回滚判断标准：**
- 所有自动化改回仅使用既有 `browser` 工具。
- Discord 输出流程继续可用（若独立接入了脱敏钩子，可保留，不冲突）。

---

## 6) 并行能力声明（关键）

- PinchTab wrapper 是**并行试点能力**，用于补充某些 HTTP 化控制场景。
- 现有 `browser` 工具链是主路径，**不被替换**。
- 调度建议：
  - 常规 Web 自动化：优先 `browser`。
  - 需要受控 HTTP sidecar 接入时：按白名单路由到 `pinchtab-wrapper`。

---

## 7) 环境变量 / 端口 / 权限清单

### 7.1 环境变量

- `PINCHTAB_UPSTREAM`：PinchTab 上游地址（默认 `http://127.0.0.1:39090`）
- `PINCHTAB_WRAPPER_HOST`：wrapper 监听地址（默认 `127.0.0.1`）
- `PINCHTAB_WRAPPER_PORT`：wrapper 端口（默认 `39091`）
- `PINCHTAB_REQUIRE_TOKEN`：是否启用 token 鉴权（默认 `1`）
- `PINCHTAB_WRAPPER_TOKEN`：访问 token（必填，建议 >=32 字符）
- `PINCHTAB_TIMEOUT_SEC`：上游超时秒数（默认 `15`）
- `PINCHTAB_MAX_BODY_BYTES`：请求体上限（默认 `65536`）
- `PINCHTAB_ALLOWED_METHODS`：允许方法（默认 `GET,POST`）
- `PINCHTAB_ALLOWED_PATH_PREFIXES`：允许路径前缀（默认 `/health,/v1/`）

### 7.2 端口

- `39090/tcp`：PinchTab 上游（本机）
- `39091/tcp`：PinchTab wrapper（本机）

### 7.3 权限

最小权限原则：
- 仅需本机用户态运行 Python3。
- 无 root 必需项。
- 无文件系统写入必需项（除日志输出到 stdout）。
- 不需要公网监听权限（默认回环）。

---

## 8) 风险与后续建议

- 当前为最小试点，未实现：
  - token 轮换自动化
  - 结构化审计日志落盘
  - 细粒度 RBAC
- 若要推进到生产：
  1. 接入 systemd（守护 + 重启策略）
  2. 增加 Prometheus 指标与审计日志
  3. 将脱敏规则外置配置并加单元测试
  4. 引入 mTLS 或网关鉴权
