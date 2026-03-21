# OpenViking 本地 Embedding 最小 PoC（CPU/低侵入）

- 时间：2026-03-11
- 目标：在**不污染现有记忆体系**前提下，完成 OpenViking 本地 embedding 可行性验证。
- 结论（先看）：✅ **可跑通**。采用本地 CPU embedding（`BAAI/bge-small-en-v1.5`）+ OpenAI 兼容本地服务，OpenViking 能启动、入库并返回语义检索结果。

---

## 1) 方案选择（轻量、本地、CPU 优先）

本 PoC 选型：
- Embedding 模型：`BAAI/bge-small-en-v1.5`（384 维，轻量，CPU 可用）
- 运行方式：`fastembed` 本地推理 + FastAPI 提供 OpenAI 兼容接口（`/v1/embeddings`）
- OpenViking 对接方式：`provider=openai`，`api_base=http://127.0.0.1:8008/v1`

说明：
- OpenViking 当前配置校验要求 `embedding.dense` 与 `vlm` 均存在，因此额外提供了本地 `chat/completions` stub（仅用于通过配置与最小流程，不依赖外部 key）。
- 全流程不依赖云端 embedding API key（`api_key` 使用本地占位值）。

---

## 2) 隔离运行（避免污染现有记忆）

隔离目录：`/tmp/openviking_local_poc`

- 虚拟环境：`/tmp/openviking_local_poc/.venv`
- OpenViking 数据目录：`/tmp/openviking_local_poc/ov_workspace`
- 配置文件：`/tmp/openviking_local_poc/ov.conf`
- 本地模型服务脚本：`/tmp/openviking_local_poc/local_model_server.py`

未改动：
- `~/.openclaw` 现有主配置/主记忆
- 现有 `memory/*.md` / `MEMORY.md`

---

## 3) 最小配置（ov.conf）

> 实测可用版本（端口做了隔离）：

```json
{
  "storage": {
    "workspace": "/tmp/openviking_local_poc/ov_workspace",
    "vectordb": { "name": "context", "backend": "local" },
    "agfs": { "port": 18331, "log_level": "warn", "backend": "local" }
  },
  "server": { "host": "127.0.0.1", "port": 19331 },
  "embedding": {
    "dense": {
      "provider": "openai",
      "api_base": "http://127.0.0.1:8008/v1",
      "api_key": "local-dev",
      "model": "BAAI/bge-small-en-v1.5",
      "dimension": 384
    }
  },
  "vlm": {
    "provider": "openai",
    "api_base": "http://127.0.0.1:8008/v1",
    "api_key": "local-dev",
    "model": "qwen2.5vl-stub"
  }
}
```

---

## 4) 启动步骤（最小）

```bash
# 0) 准备隔离目录
POC=/tmp/openviking_local_poc
python3 -m venv $POC/.venv
source $POC/.venv/bin/activate
pip install -U pip
pip install openviking fastapi uvicorn fastembed

# 1) 启动本地模型服务（OpenAI 兼容 /v1）
python $POC/local_model_server.py

# 2) 启动 OpenViking（隔离配置）
openviking-server --config $POC/ov.conf --host 127.0.0.1 --port 19331

# 3) 健康检查
curl http://127.0.0.1:19331/health
```

---

## 5) PoC 检索验证结果

### 5.1 入库样本

在 `viking://resources/poc2` 下导入两份文本：
- `doc_fruit.md`：苹果/香蕉/水果/早餐
- `doc_gpu.md`：CUDA/NVIDIA/GPU 并行计算

### 5.2 检索查询与结果（Top 命中）

- Query: `水果 早餐`
  - Top1: `viking://resources/poc2/doc_fruit/doc_fruit.md`（score≈0.687）
- Query: `GPU 并行计算`
  - Top1: `viking://resources/poc2/doc_gpu/doc_gpu.md`（score≈0.661）
- Query: `香蕉`
  - Top1: `viking://resources/poc2/doc_fruit/doc_fruit.md`（score≈0.666）

结论：
- ✅ 语义检索方向正确，目标文档可被稳定命中到 Top1。

---

## 6) 主观效果评价（PoC 级）

**优点**
- 本地 CPU 可运行，成本低、无需外部 embedding key。
- 对 OpenViking 配置侵入小（仅 `provider=openai` + 本地兼容端点）。
- 在小样本检索上能体现基础语义区分能力。

**不足/注意点**
- 首次模型下载有冷启动时间（HF 拉取模型）。
- 导入时出现过早期连接拒绝日志（模型服务尚未完全 ready 时触发），建议在正式流程中加入 ready check 再入库。
- 本 PoC 为“最小可行”，VLM 采用 stub，仅用于通过配置与流程；生产建议换成真实本地/云模型并评估抽取质量。

---

## 7) 回滚与清理

```bash
# 停服务（按实际 PID）
pkill -f local_model_server.py
pkill -f "openviking-server --config /tmp/openviking_local_poc/ov.conf"

# 清理隔离目录（可选）
rm -rf /tmp/openviking_local_poc
```

因为全程在 `/tmp/openviking_local_poc` 隔离运行，不影响现有 OpenClaw 主记忆链路。

---

## 8) 建议下一步（低风险）

1. 给本地模型服务加 `health/ready`，并在 OpenViking 启动后做 `ready gate` 再执行入库。  
2. 将检索评测扩展到 20~50 条真实记忆样本，记录 Recall@K/误召回率。  
3. 若通过评测，再考虑接入 OpenClaw 的旁路环境（非主 memory slot）。
