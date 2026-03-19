# HEARTBEAT.md

## 每日自动化任务

### 磁盘清理
```bash
bash scripts/auto-cleanup.sh
```
- 清理 tmp/（>7天）
- 清理 tmp_in/（>1天）
- 清理 .cache/（>3天且>100MB）
- 清理 logs/（>30天）

### 磁盘监控
```bash
bash scripts/disk-monitor.sh
```
- 检查磁盘使用率
- 超过 80% 发送告警
- 列出 Top 10 大文件

## 每 3 天自动化任务

- [ ] Git 未推送的 memory 变更 → 自动 commit + push
- [ ] 未归档的规则更新 → 自动归档
- [ ] Skill 更新/新增 → 更新 skill-usage-guide.md

## 发现未推送变更时

自动执行：
```bash
git add memory/ rules/ skills/ docs/ examples/
git commit -m "Sync: OpenClaw auto-archive $(date '+%Y-%m-%d')"
git push memory main
git push origin main
```

汇报格式：
```
已自动推送归档：
- memory/YYYY-MM-DD.md（新增 X 条）
- 规则更新（Y 处变更）
- Commit: <hash>
```

## 手动检查项（需要时）

- [ ] 日历事件（未来 24-48h）
- [ ] 邮件/通知
- [ ] 天气（如需外出）

## 无任务时

回复：HEARTBEAT_OK

---

## 自动化脚本清单

| 脚本 | 功能 | 频率 | 位置 |
|------|------|------|------|
| auto-cleanup.sh | 清理临时文件 | 每日 | scripts/ |
| disk-monitor.sh | 磁盘空间监控 | 每日 | scripts/ |

