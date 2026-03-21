# PinchTab + Wrapper 常驻与安全加固（完成记录）

日期：2026-03-11

## 已完成项

1. **上游 token 透传**（wrapper 转发 `Authorization: Bearer ...`）✅  
   - 文件：`scripts/pinchtab_wrapper/pinchtab_wrapper.py`
   - 新增环境变量：
     - `PINCHTAB_FORWARD_AUTH=1`（默认开启）
     - `PINCHTAB_UPSTREAM_BEARER_TOKEN=`（来访无 Bearer 时可回退固定上游 token）
   - 行为：
     - 来访带 `Authorization: Bearer xxx` → 透传给上游 PinchTab
     - 若未带且配置了 `PINCHTAB_UPSTREAM_BEARER_TOKEN` → 用固定 Bearer 转发

2. **常驻方案（自动重启）** ✅
   - **systemd 单元**：
     - `scripts/pinchtab_wrapper/systemd/pinchtab.service`
     - `scripts/pinchtab_wrapper/systemd/pinchtab-wrapper.service`
   - **可替代后台脚本（无 systemd 场景）**：
     - `scripts/pinchtab_wrapper/pinchtab_daemon.sh`
     - 支持：`start|stop|restart|status|logs`
     - 内置 supervisor 循环（进程退出 2 秒后重启）

3. **.env 配置模板** ✅
   - 文件：`scripts/pinchtab_wrapper/.env.example`
   - 已加入随机 token 生成指引：
     - `openssl rand -base64 48 | tr -d '\n'`
     - `python3 -c "import secrets; print(secrets.token_urlsafe(48))"`
   - 同时包含 PinchTab 本体关键变量：`BRIDGE_BIND/PORT/TOKEN/PROFILE`

4. **启动/停止/重启验证** ✅（使用 fallback 脚本实测）
   - `./pinchtab_daemon.sh start`：pinchtab + wrapper 均启动
   - `./pinchtab_daemon.sh restart`：可正常重启
   - `./pinchtab_daemon.sh stop`：可正常停止
   - 鉴权验证：
     - 无 `X-Wrapper-Token` 调 `/v1/tabs` 返回 `401 unauthorized`（wrapper 拦截）
   - 透传验证：
     - 带 `X-Wrapper-Token` + `Authorization: Bearer $BRIDGE_TOKEN` 时，不再返回 `missing_token`，转为上游业务响应（本次为 `404 page not found`），说明 Bearer 已成功透传

---

## 使用命令

### A) fallback（推荐，WSL/无 systemd 直接可用）

```bash
cd /mnt/e/Openclaw/.openclaw/workspace/scripts/pinchtab_wrapper
cp -n .env.example .env
# 编辑 .env：至少替换 PINCHTAB_WRAPPER_TOKEN 和 BRIDGE_TOKEN

./pinchtab_daemon.sh start
./pinchtab_daemon.sh status
./pinchtab_daemon.sh logs 120
./pinchtab_daemon.sh restart
./pinchtab_daemon.sh stop
```

### B) systemd（支持 systemd 的 Linux）

```bash
cd /mnt/e/Openclaw/.openclaw/workspace/scripts/pinchtab_wrapper
cp -n .env.example .env

mkdir -p ~/.config/systemd/user
cp systemd/pinchtab.service ~/.config/systemd/user/
cp systemd/pinchtab-wrapper.service ~/.config/systemd/user/

systemctl --user daemon-reload
systemctl --user enable --now pinchtab.service pinchtab-wrapper.service
systemctl --user status pinchtab.service pinchtab-wrapper.service

# 管理命令
systemctl --user restart pinchtab.service pinchtab-wrapper.service
systemctl --user stop pinchtab-wrapper.service pinchtab.service
journalctl --user -u pinchtab.service -u pinchtab-wrapper.service -f
```

---

## 关键文件清单

- `scripts/pinchtab_wrapper/pinchtab_wrapper.py`（新增 Authorization/Bearer 透传）
- `scripts/pinchtab_wrapper/.env.example`（增强模板 + 随机 token 指引）
- `scripts/pinchtab_wrapper/pinchtab_daemon.sh`（fallback 常驻脚本）
- `scripts/pinchtab_wrapper/systemd/pinchtab.service`
- `scripts/pinchtab_wrapper/systemd/pinchtab-wrapper.service`

## 安全建议（保留）

- 默认仅监听 `127.0.0.1`
- 维持 `PINCHTAB_REQUIRE_TOKEN=1`
- 使用 48+ 字符高熵 token
- 非必要不开放 `0.0.0.0`
