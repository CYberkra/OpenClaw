# HEARTBEAT.md

## 自动化检查（每 3 天）

- [ ] Git 未推送的 memory 变更
- [ ] 未归档的规则更新
- [ ] Skill 更新/新增

## 发现未推送变更时

自动执行：
```bash
git add memory/ rules/ skills/
git commit -m "Sync: OpenClaw auto-archive $(date +%Y-%m-%d)"
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

## 手动检查项

- [ ] 日历事件（未来 24-48h）
- [ ] 邮件/通知
- [ ] 天气（如需外出）

## 无任务时

回复：HEARTBEAT_OK
