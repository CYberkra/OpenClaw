# E 盘清理盘点建议（仅分析，不执行删除）

生成时间：2026-03-10 19:xx (Asia/Shanghai)

## 1) 容量总览

基于 `df`：

- 总容量：`157,329,387,520 B`（约 **146.5 GiB / 147G**）
- 已用：`138,657,841,152 B`（约 **129.1 GiB / 130G**）
- 剩余：`18,671,546,368 B`（约 **17.4 GiB / 18G**）
- 使用率：**89%**

> 目前可用空间虽有 ~18G，但打包阶段（临时文件、缓存、重复构建）容易瞬时吃空间，建议先清理低风险项。

---

## 2) 大目录扫描结论（深度 1~3，重点）

### /mnt/e/Openclaw 关键体量

- `/mnt/e/Openclaw`：约 **17G**
- `/mnt/e/Openclaw/.openclaw/extensions`：约 **2.3G**
  - 其中 `discord-voice`：约 **2.2G**
- `/mnt/e/Openclaw/stt-local`：约 **1.9G**
- `/mnt/e/Openclaw/backups`：约 **142M**

### /mnt/e/Openclaw/.openclaw/workspace 关键体量

- `workspace` 总计：约 **13G**
- `.venvs/cuda-test`：约 **5.1G**
- `repos/GPR_GUI`：约 **3.4G**
- `tmp`：约 **2.6G**
  - `tmp/temp_repository`：约 **1.2G**
  - `tmp/temp_repository_publish`：约 **816M**
  - `tmp/openclaw-skills`：约 **412M**
  - `tmp/openclaw-skills-voice`：约 **206M**
- `.venv`：约 **533M**
- `isolated/GPR_GUI_evolve`：约 **308M**

### /mnt/e/Openclaw/.openclaw/workspace/repos/GPR_GUI 关键体量

- `repos/GPR_GUI` 总计：约 **3.4G**
- `.local_quarantine`：约 **1.6G**
- `.venv_build`：约 **628M**
- `.venv_winbuild`：约 **538M**
- `dist`：约 **323M**
- `build`：约 **173M**（含 `GPR_GUI_Qt_exp_20260310_ecdbd5a.exe` 约 **141M**）
- `.git`：约 **196M**

---

## 3) Top 10 可清理候选项（非破坏性建议）

> 说明：以下“可释放”按当前目录体积粗估；实际以是否仍在使用为准。

| # | 路径 | 估算体积 | 风险 | 建议动作 |
|---|---|---:|---|---|
| 1 | `/mnt/e/Openclaw/.openclaw/workspace/.venvs/cuda-test` | 5.1G | 中 | **迁移到其他盘**或删除后按需重建（大体积虚拟环境） |
| 2 | `/mnt/e/Openclaw/.openclaw/workspace/tmp` | 2.6G | 低 | 删除临时目录（建议先留最近1-2天） |
| 3 | `/mnt/e/Openclaw/.openclaw/extensions/discord-voice` | 2.2G | 中 | 迁移到其他盘或清理历史模型/缓存 |
| 4 | `/mnt/e/Openclaw/.openclaw/workspace/repos/GPR_GUI/.local_quarantine` | 1.6G | 低 | 删除隔离副本（通常为中间副本） |
| 5 | `/mnt/e/$RECYCLE.BIN` | 1.4G | 低 | 清空回收站 |
| 6 | `/mnt/e/Openclaw/.openclaw/workspace/repos/GPR_GUI/.venv_build` | 628M | 中 | 删除后重建（Linux构建环境） |
| 7 | `/mnt/e/Openclaw/.openclaw/workspace/repos/GPR_GUI/.venv_winbuild` | 538M | 中 | 删除后重建（Windows构建环境） |
| 8 | `/mnt/e/Openclaw/.openclaw/workspace/.venv` | 533M | 中 | 删除后重建（全局项目环境） |
| 9 | `/mnt/e/Openclaw/.openclaw/workspace/repos/GPR_GUI/dist` | 323M | 低 | 删除旧产物；保留当前确认可用版本 |
|10| `/mnt/e/Openclaw/.openclaw/workspace/isolated/GPR_GUI_evolve` | 308M | 中 | 若非当前活跃分支，归档/迁移 |

### 额外候选（可选）

- `/mnt/e/Openclaw/.openclaw/workspace/repos/GPR_GUI/build`：173M（低，旧构建中间件可删）
- `/mnt/e/Openclaw/.openclaw/workspace/repos/GPR_GUI/.git`：196M（中，`git gc`/浅克隆/归档旧分支）
- `/mnt/e/Openclaw/stt-local`：1.9G（中，若近期不做本地语音识别可迁移）
- `/mnt/e/2026_探地雷达VNA`：11G（中-高，建议仅归档迁移，不建议直接删）

---

## 4) 不要删（关键项）

1. `repos/GPR_GUI` 中**当前主源码**（`.py`、`assets`、配置文件、版本控制信息）
2. `dist/build` 内**当前已验证可运行的可执行版本**（至少保留1份）
3. `workspace/reports` 下**近期报告与截图**（尤其最近 1~2 周）
4. 当前正在使用的 Python 环境（若不确定，先记录 `pip freeze` 再处理）

---

## 5) 两套执行方案（建议）

## A. 保守清理（低风险优先）

仅做低风险项：

- 清空 `$RECYCLE.BIN`：1.4G
- 清理 `workspace/tmp`：2.6G
- 清理 `GPR_GUI/.local_quarantine`：1.6G
- 清理 `GPR_GUI/dist`：0.3G
- （可选）清理 `GPR_GUI/build`：0.17G

**预计释放：约 5.9G ~ 6.1G**

## B. 激进清理（含中风险）

在保守方案基础上追加：

- 清理 `.venvs/cuda-test`：5.1G
- 清理 `.venv_build + .venv_winbuild + workspace/.venv`：约1.7G
- 迁移 `extensions/discord-voice`：2.2G
- （可选）迁移 `stt-local`：1.9G

**预计释放：约 14.9G（不含 stt-local） ~ 16.8G（含 stt-local）**

> 结论：要确保“打包期间余量充足”，建议至少执行到 **激进方案前3项**，即可稳定超过 **10GB** 目标。

---

## 6) 建议的实际落地顺序（避免误删）

1. 先做低风险：`$RECYCLE.BIN` → `tmp` → `.local_quarantine` → `dist/build`
2. 再做中风险：`.venv*`（确认可重建）
3. 最后再考虑迁移大目录：`discord-voice` / `stt-local` / 课程资料归档目录
4. 每一步后复查一次磁盘余量，确认达到目标即停止

---

> 本文档仅为盘点建议，**未执行任何删除/改动操作**。