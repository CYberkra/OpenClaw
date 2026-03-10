# 状态映射（业务态 -> Star-Office 状态）

你给的四类工作态：`coding / debugging / reviewing / idle`。

## 推荐映射

| 你的工作态 | Star-Office 状态 | 原因 |
|---|---|---|
| coding | writing | `writing` 映射到主工作区，表示持续产出（代码/文档） |
| debugging | error | `error` 会进 Bug 区，视觉上最直观反映“正在排障” |
| reviewing | researching | 评审通常是阅读/分析/检索，`researching` 更贴近“审阅思考” |
| idle | idle | 待命态，进入休息区 |

## 可执行示例

```bash
cd research/star-office-ui
python3 set_state.py writing "coding: 实现登录流程"
python3 set_state.py error "debugging: 修复500错误"
python3 set_state.py researching "reviewing: 审查PR #42"
python3 set_state.py idle "空闲待命"
```

## 兼容说明
- 后端 canonical 状态（app.py）：`idle/writing/researching/executing/syncing/error`
- `set_state.py` 额外支持 `receiving/replying`，但前端办公区主要按上述 canonical 状态映射。
