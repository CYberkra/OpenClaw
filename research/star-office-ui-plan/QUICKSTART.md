# Star-Office-UI QUICKSTART（10分钟最小落地）

> 目标：仅在本机跑通，不改生产配置，不要求公网。

## 1) 获取代码
```bash
git clone https://github.com/ringhyacinth/Star-Office-UI.git research/star-office-ui
cd research/star-office-ui
```

## 2) 安装依赖（Python 3.10+）
```bash
python3 -m pip install -r backend/requirements.txt
```
依赖仅两项：`flask==3.0.2`、`pillow==10.4.0`。

## 3) 初始化状态文件
```bash
cp -n state.sample.json state.json
```

## 4) 启动后端
```bash
cd backend
python3 app.py
```
默认访问：<http://127.0.0.1:19000>

## 5) 验证状态切换
另开终端：
```bash
cd research/star-office-ui
python3 set_state.py writing "启动后自检中"
python3 set_state.py researching "读取README并整理配置"
python3 set_state.py idle "待命中"
```

## 6) 可选：接口烟雾测试
```bash
cd research/star-office-ui
python3 scripts/smoke_test.py --base-url http://127.0.0.1:19000
```

---

## 关键配置提炼（来自 README / 脚本）

### 部署方式
- **本地最简部署**：Python + Flask 直接运行（本方案）。
- **公网可选**：`cloudflared tunnel --url http://127.0.0.1:19000`
- **桌面宠物可选**：`desktop-pet/`（Tauri，非必须）

### 状态上报机制
1. **主 Agent 本地状态**：
   - `set_state.py` 写入 `state.json`（默认 `STAR_OFFICE_STATE_FILE` 可覆盖路径）
   - 后端 `GET /status` 读取并展示
2. **访客 Agent 远程上报**：
   - `office-agent-push.py` 通过 `POST /join-agent` 加入
   - 之后每 15 秒 `POST /agent-push` 推送状态

### JOIN_KEY / AGENT_NAME / OFFICE_URL
- 出现在 `office-agent-push.py`（访客接入核心三元组）：
  - `JOIN_KEY`：办公室分配的 join key
  - `AGENT_NAME`：显示名
  - `OFFICE_URL`：办公室地址（如 `https://office.hyacinth.im` 或你的自建地址）
- `join-keys.json` 首次启动可由 `join-keys.sample.json` 自动生成。
