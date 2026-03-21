# repos/ 独立管理策略（2026-03-21）

- 根仓库（workspace）忽略 `repos/`，避免嵌套仓状态污染主仓。
- `repos/` 下每个项目按**各自仓库**独立提交与推送。
- 主仓只存汇总产物（reports/memory/rules 等），不直接纳管子项目源码树。
- 若需记录某次子仓变更，在主仓 `reports/` 写变更摘要并附 commit hash。
