# Rules Index（轻量总索引）

> 目的：这是**导航页**与**优先级页**，不存放规则正文；正文仍留在各源文件。

## 1) 规则来源清单（谁负责什么）

- `skills/user-preferences/SKILL.md`
  - **执行主源（SSOT）**：用户长期偏好、硬约束、执行细则。
- `AGENTS.md`
  - 工作区级高层操作原则、通用红线、流程摘要。
- `skills/rule-archive-lite/SKILL.md`
  - 规则历史快照与演进记录（审计/回溯用），**不作为首查执行源**。
- `USER.md`
  - 用户画像与稳定偏好事实（称呼、长期关注点等）。
- `TOOLS.md`
  - 环境映射与本地配置（路径、设备、主机、别名等）。
- `memory/YYYY-MM-DD.md`
  - 当日临时上下文、变更落地记录、执行痕迹。
- `rules/*.md`（本目录）
  - 专项规则文档（如 GUI 提交规范），按主题集中。

## 2) 生效优先级（高 → 低）

1. 用户当轮明确指令
2. `skills/user-preferences/SKILL.md`
3. `AGENTS.md`（硬规则/高层约束）
4. `skills/rule-archive-lite/SKILL.md`（历史快照）
5. 其他文档（如项目说明、一般注释）

> 冲突处理：优先“更近的用户意图 + 更安全/更高闸门”解释；不可消解时先澄清。

## 3) 什么时候查哪个文件（最小决策）

- 需要“现在就怎么执行” → 先查 `user-preferences`，再看 `AGENTS.md`
- 需要“这条规则怎么来的/历史版本” → 查 `rule-archive-lite`
- 需要“用户身份/称呼/长期偏好” → 查 `USER.md`
- 需要“路径/设备/环境映射” → 查 `TOOLS.md`
- 需要“今天发生过什么/本轮已做过什么” → 查 `memory/YYYY-MM-DD.md`
- 需要“某专项规则细节（如 GUI 提交）” → 查 `rules/` 对应文件

### 3.1) 按需加载策略（Token 防膨胀）

- 闲聊/轻问答/简单路由：默认仅加载核心骨架规则 + `rules/INDEX.md`。
- 禁止每轮预读全部长文规则。
- 命中复杂路由（多步骤、多工具、高风险、需专项验收）后，再按本索引逐项动态加载必要文档。

## 4) 变更联动原则（防漂移）

- 新增/修改**硬规则**：
  - 必改：`skills/user-preferences/SKILL.md`
  - 必留痕：`skills/rule-archive-lite/SKILL.md` + `memory/YYYY-MM-DD.md`
- 仅当日临时约束：
  - 只写：`memory/YYYY-MM-DD.md`
- 用户画像变化（称呼/长期目标等）：
  - 更新：`USER.md`
  - 若影响执行行为，再同步 `user-preferences`
- 环境/路径/设备变化：
  - 更新：`TOOLS.md`
  - 若升格为硬约束，再同步 `user-preferences` 与 `memory`
- 工作区级通用流程变化：
  - 更新：`AGENTS.md`
  - 若属于可执行硬规则，再同步 `user-preferences` + `rule-archive-lite`

## 5) 用户关键词速查（可直接说）

- 路由：`直答` / `走 manager` / `走 opencode` / `加 reviewer` / `开 CI`
- 模式：`切 strict` / `切 proactive` / `切 evolver` / `切 ralph` / `恢复 default`
- 验收：`仅到 G3` / `执行全闸门` / `跳过 CI（需理由）`

---

维护建议：仅在“规则位置、优先级、联动关系、关键词”变化时更新本页；避免把正文复制进来。