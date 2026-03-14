# 组会PPT子分区

用途：专门用于**长期制造组会汇报 PPT**，避免材料分散、版本混乱、每次从零开始。

## 目录结构

- `README.md`：本分区说明
- `WORKFLOW.md`：固定工作流
- `BRIEF_TEMPLATE.md`：每次组会任务输入模板
- `deck.md`：当前正在制作的主稿（Markdown 源）
- `history/`：历次组会归档
- `assets/`：图片、图标、引用图、Logo
- `data/`：表格、实验结果、原始摘要
- `exports/`：导出的 html/ppt/pdf 等产物
- `notes/`：口播备注、老师反馈、改稿意见

## 设计原则

1. **一切围绕组会汇报**：不和别的项目材料混放。
2. **Markdown 为单一事实源**：默认用 `deck.md` 写内容。
3. **默认 html-presentation 路线**：
   - Markdown → HTML
   - 命令：`python3 scripts/md2ppt.py reports/group-meeting-ppt/deck.md -o reports/group-meeting-ppt/exports/group-meeting-ppt.html`
4. **每次汇报都留归档**：方便复用、追溯、拼接历史成果。
5. **先内容框架，后视觉润色**：先保证逻辑，再补图和排版。

## 推荐使用方式

每次你只要在这个线程里告诉我：

- 本次组会日期
- 汇报主题
- 想突出哪些结果
- 是否要压缩到 5 / 8 / 10 页
- 是否偏“进展汇报 / 问题汇报 / 结果展示 / 答辩风格”

我就会直接基于这个分区继续迭代，不再重新搭框架。

## 默认页面骨架

1. 标题页
2. 本周目标 / 背景
3. 当前进展
4. 关键结果（图/表）
5. 问题与分析
6. 下一步计划
7. 备份页（可选）

## 命名规范

建议归档目录命名：

- `history/2026-03-14_weekly/`
- `history/2026-03-21_result-review/`
- `history/2026-04-02_midterm-prep/`

导出文件建议命名：

- `group-meeting-ppt_2026-03-14.html`
- `group-meeting-ppt_2026-03-14.pdf`
- `group-meeting-ppt_2026-03-14.pptx`

## 约定

- 这个子分区默认服务于 **组会长期汇报**。
- 新一期汇报开始时，先复制 `BRIEF_TEMPLATE.md` 填写需求。
- 完成后把关键材料沉淀到 `history/`，形成可复用资产池。
