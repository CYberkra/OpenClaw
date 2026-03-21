# AI办公室/AI可视化 落地执行清单（简版）

## 本周（立即可做）
- [ ] 部署 **Langfuse**（Docker）并接入 1 条 GPR 核心链路（记录 token/耗时/失败原因）
- [ ] 部署 **n8n**，上线 3 条流程：
  - [ ] 任务日报汇总 -> Discord
  - [ ] 任务失败告警 -> Discord
  - [ ] 定时健康检查 -> Discord
- [ ] 部署 **Grafana**，建立基础看板：成功率/延迟/错误率/资源占用
- [ ] 安装并验证 **Data Formulator**，产出 2 个固定模板图（实验对比、异常分布）

## 两周内（试运行）
- [ ] 将 Langfuse 覆盖到 3 条核心 Agent 流程
- [ ] n8n 流程覆盖率提升到 >= 30%
- [ ] Grafana 告警分级：P1（立即）/P2（聚合）
- [ ] 每周产出一次“研发+运维可视化周报”（用 Data Formulator 模板）

## 一个月内（正式接入）
- [ ] 引入 **Dify**，上线“研发助手”与“运维助手”两个应用
- [ ] 确立平台分工：
  - [ ] n8n = 编排中枢
  - [ ] Dify = AI应用交付
  - [ ] Langfuse = LLM可观测
  - [ ] Grafana = 运维监控
- [ ] 建立安全基线：脱敏、最小权限、凭据集中管理、审计日志

## 中期备选（2~8周）
- [ ] 在 **RAGFlow / AnythingLLM** 二选一做知识检索层
- [ ] 在 **Superset / Metabase** 二选一做业务分析层
- [ ] 用 **ToolJet** 做内部运营面板（审批/参数开关）

## 暂缓 / 不建议
- [ ] 暂缓同时引入 Langflow + Flowise + Dify（三套编排并行）
- [ ] 不采用 Discord self-bot 类方案（合规与安全风险高）

## 推荐优先级
1. **P0**：Langfuse / n8n / Grafana
2. **P1**：Data Formulator / Dify
3. **P2**：RAGFlow(或AnythingLLM) / Superset(或Metabase) / ToolJet