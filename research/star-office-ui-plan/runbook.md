# Star-Office-UI Runbook（最小故障排查）

## 0) 快速体检
```bash
cd research/star-office-ui
python3 scripts/smoke_test.py --base-url http://127.0.0.1:19000
```

---

## 1) 连不上（页面打不开 / API 不通）

### 现象
- 浏览器访问 `http://127.0.0.1:19000` 失败
- `curl http://127.0.0.1:19000/health` 不返回 200

### 排查
1. 后端是否启动：
   ```bash
   cd research/star-office-ui/backend
   python3 app.py
   ```
2. 端口是否被占用（默认19000）：
   ```bash
   ss -ltnp | grep 19000 || true
   ```
3. 若你改了端口，所有调用统一改成新地址（set_state/smoke/push）。

---

## 2) 状态不刷新（UI 不变）

### 现象
- 执行 `set_state.py` 成功，但页面状态不更新

### 排查
1. 确认写入的是同一个 `state.json`：
   ```bash
   cd research/star-office-ui
   python3 set_state.py writing "状态刷新测试"
   cat state.json
   ```
2. 若使用自定义路径，设置：
   ```bash
   export STAR_OFFICE_STATE_FILE=/absolute/path/to/state.json
   ```
3. 强制刷新浏览器（避免缓存）并检查 `/status`：
   ```bash
   curl -s http://127.0.0.1:19000/status
   ```

---

## 3) 访客接入失败（JOIN_KEY / 权限问题）

### 现象
- `office-agent-push.py` join 失败
- 返回 403/404 或提示 key 无效

### 排查
1. 检查服务端 `join-keys.json` 是否存在/包含该 key。
2. `JOIN_KEY/AGENT_NAME/OFFICE_URL` 三项是否填写。
3. `OFFICE_URL` 是否可达，协议是否正确（http vs https）。
4. 若 `/status` 需鉴权，设置 `OFFICE_LOCAL_STATUS_TOKEN`（仅本地状态拉取时需要）。

---

## 4) 权限/环境问题（pip/python）

### 现象
- 依赖安装失败、`ModuleNotFoundError`

### 排查
1. Python 版本必须 3.10+：
   ```bash
   python3 --version
   ```
2. 重新安装依赖：
   ```bash
   cd research/star-office-ui
   python3 -m pip install -r backend/requirements.txt
   ```
3. 使用虚拟环境（推荐）：
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r backend/requirements.txt
   ```
