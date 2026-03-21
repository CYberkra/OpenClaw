# PinchTab Runtime Status

- 时间: 2026-03-11 22:41 (Asia/Shanghai)
- 目录: `/mnt/e/Openclaw/.openclaw/workspace/scripts/pinchtab_wrapper`

## 已完成配置

1. 已将 `.env.example` 覆盖复制为 `.env`
2. 已生成并写入强随机 token：
   - `BRIDGE_TOKEN`
   - `PINCHTAB_WRAPPER_TOKEN`
3. 已设置：
   - `BRIDGE_BIND=127.0.0.1`
   - `BRIDGE_PORT=9867`
   - `BRIDGE_PROFILE=~/.pinchtab/automation-profile`
4. 已设置：
   - `PINCHTAB_FORWARD_AUTH=1`
   - `PINCHTAB_UPSTREAM=http://127.0.0.1:9867`
   - `PINCHTAB_WRAPPER_PORT=39091`
5. 已启动 daemon，并清理冲突旧进程后重启成功。

## 当前监听

- `127.0.0.1:9867` -> `pinchtab`
- `127.0.0.1:39091` -> `pinchtab_wrapper.py`

## 健康检查

- 直连 upstream（携带 Bearer）：`http://127.0.0.1:9867/health` -> `{"mode":"dashboard","status":"ok"}`
- wrapper 转发（携带 `X-Wrapper-Token` + `Authorization: Bearer ...`）：`http://127.0.0.1:39091/health` -> `{"mode":"dashboard","status":"ok"}`

> 说明：由于开启了 `PINCHTAB_FORWARD_AUTH=1`，访问 wrapper 需要同时提供 wrapper token 和上游 Bearer，若缺少上游 Bearer，/health 会返回 upstream unauthorized。

## 运行命令

在目录 `/mnt/e/Openclaw/.openclaw/workspace/scripts/pinchtab_wrapper` 执行：

```bash
./pinchtab_daemon.sh start
./pinchtab_daemon.sh stop
./pinchtab_daemon.sh restart
./pinchtab_daemon.sh status
./pinchtab_daemon.sh logs 80
```

## Tokens（请立即保存到安全位置）

- `BRIDGE_TOKEN`: `SY0D8rJIYg9xHfNPPe-IjrCGTVTkJLkSuuV0t5XiKpba_xTvG33le_8YlKBrCMtmP4AOwBj9RA-7fMpDF8Odpg`
- `PINCHTAB_WRAPPER_TOKEN`: `SyyY9ADeFNNEUI0A095CwanG_AZvOImXy0aKOgUxfEfvpqIGIB8jcf-3JPUsnrnJgzAamib6stcD90ea3LOvdA`

## 示例调用

```bash
WRAPPER_TOKEN='(你的 PINCHTAB_WRAPPER_TOKEN)'
BRIDGE_TOKEN='(你的 BRIDGE_TOKEN)'

curl -sS \
  -H "X-Wrapper-Token: ${WRAPPER_TOKEN}" \
  -H "Authorization: Bearer ${BRIDGE_TOKEN}" \
  http://127.0.0.1:39091/health
```
