# 故障排查手册

> 常见问题及解决方案速查

---

## 🔴 严重问题

### 1. Git Push 失败（403/401）

**症状**：
```
fatal: unable to access 'https://github.com/...': The requested URL returned error: 403
```

**原因**：
- Token 过期或权限不足
- GitHub Push Protection 触发

**解决方案**：
```bash
# 检查 Token 状态
gh auth status

# 重新登录
gh auth login

# 或使用 Personal Access Token
git remote set-url origin https://TOKEN@github.com/user/repo.git
```

**预防措施**：
- 使用 Git Credential Manager 存储 Token
- 定期更新 Token（设置提醒）

---

### 2. Discord 消息发送失败

**症状**：
- 消息在 Discord 中不显示
- 长消息被截断

**原因**：
- Discord 消息长度限制（2000字符）
- 格式问题

**解决方案**：
```markdown
# 消息超过长度限制时：
1. 拆分为多条短消息
2. 或使用文件附件

# 示例
if (message.length > 1500) {
    send_as_file(message);
} else {
    send_message(message);
}
```

---

### 3. Skill 调用失败

**症状**：
```
Error: Skill 'xxx' not found or failed to load
```

**原因**：
- SKILL.md 格式错误
- 缺少必要字段（name, description）
- 依赖未安装

**解决方案**：
```bash
# 检查 Skill 格式
head -20 skills/xxx/SKILL.md

# 验证 YAML frontmatter
# 必须包含:
# ---
# name: skill-name
# description: Skill description
# ---

# 检查依赖
# 查看 SKILL.md 中的 requires 字段
```

---

## 🟡 一般问题

### 4. 路由决策困难

**症状**：
- 不知道用哪个 skill
- 多个 skill 似乎都适用

**解决方案**：
1. 查阅 `rules/routing-cheat-sheet.md`
2. 使用默认选择规则：
   - 犹豫 → `subagent-manager`
   - 代码 → `opencode`
   - 文档 → `markdown-converter`

---

### 5. Token 用量过高

**症状**：
- 对话很快达到上下文限制
- 成本上升

**解决方案**：
```markdown
1. 启用按需加载（已配置）
2. 精简 skill 描述
3. 使用 `qmd search` 替代 `qmd get`
4. 复杂任务用 subagent 分担
```

---

### 6. 子代理超时/失败

**症状**：
```
Sub-agent timeout after 600s
```

**原因**：
- 任务过于复杂
- 网络问题
- 子代理崩溃

**解决方案**：
```markdown
1. 拆解任务为更小步骤
2. 增加 timeout 参数
3. 检查子代理日志
4. 手动重试失败步骤
```

---

## 🟢 优化建议

### 7. 提升响应速度

**方法**：
```markdown
1. 使用 Flash 模型处理简单任务
2. 缓存频繁查询的结果
3. 预加载常用 skill
4. 减少不必要的文件读取
```

### 8. 减少磁盘占用

**方法**：
```bash
# 运行自动清理
./scripts/auto-cleanup.sh

# 监控磁盘使用
./scripts/disk-monitor.sh

# 手动清理大文件
find . -type f -size +10M -ls
```

---

## 📞 获取帮助

当以上方法都无效时：

1. **查看日志**：
   ```bash
   tail -n 50 logs/openclaw.log
   ```

2. **检查状态**：
   ```bash
   openclaw status
   git status
   ```

3. **重启服务**：
   ```bash
   openclaw gateway restart
   ```

4. **联系支持**：
   - 记录错误信息
   - 记录复现步骤
   - 提供相关日志片段

---

## 🔧 常用诊断命令

```bash
# 检查 workspace 状态
git status
git log --oneline -5
du -sh .

# 检查 OpenClaw 状态
openclaw status
openclaw config list

# 检查 skill 列表
ls skills/

# 检查磁盘使用
df -h
du -sh tmp/ logs/ .cache/

# 检查网络连接
ping github.com
curl -I https://api.github.com
```

---

*最后更新：2026-03-19*
