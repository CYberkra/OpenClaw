# Star-Office 接入计划 v2（尽量套用现成资源）

## 目标与原则
- 目标：在不改生产配置、不动核心脚本逻辑前提下，准备“可直接接入”的资产与状态映射。
- 原则：**先拼装后定制**，优先 CC0/MIT/Apache2 资源；只在必要处做轻量适配。

## 架构建议（MVP）
1. **地图层**：办公室 tileset（CC0 优先）
2. **角色层**：LPC（含 sit/walk/idle）
3. **UI层**：现成 Badge/Indicator 组件映射 agent state
4. **同步层**：Socket.IO Presence（MVP）→ Yjs/Supabase（升级）

## 分阶段落地

### Phase 0（当天可完成）— 素材落库与声明
- 建立 `research/star-office-assets/manifest.example.json`
- 建立状态映射 `state-ui-mapping.example.json`
- 下载 1 套办公室 tiles + 1 套人物 sprites，先不替换线上资源
- 产出 attribution 草案（后续进入 LICENSES/THIRD_PARTY）

**验收标准**
- manifest 中每条都有：source/license/localPath/useCase
- state mapping 覆盖 reviewing/idle/debugging/coding

### Phase 1（1-2 天）— 前端最小接入
- 读取 manifest 自动装载贴图（本地静态目录）
- 用现有 UI 框架接入 Badge/Indicator（不改核心业务逻辑，仅新增展示层）
- 角色状态机最小集：idle/walk/sit（debugging/coding 可先复用 sit + icon）

**验收标准**
- 可本地预览 1 个房间 + 2 个角色状态变化
- 状态切换 < 150ms（本地）

### Phase 2（2-4 天）— Presence 联调
- 先接 Socket.IO 房间同步（join/leave/stateUpdate）
- 广播 payload 统一：`{userId, state, deskId, ts}`
- UI 显示在线点 + 名字 + 状态色

**验收标准**
- 5~20 并发角色状态更新稳定
- 断线重连后状态恢复

### Phase 3（按需）— 升级同步能力
- 需要冲突无损合并时引入 Yjs Awareness
- 或迁移至 Supabase Realtime 减少自建运维

## 推荐技术栈组合

### 组合 A（最稳妥、最低成本）
- 美术：OpenGameArt CC0/CC-BY
- UI：shadcn/ui Badge
- 实时：Socket.IO
- 适用：快速演示、内部版本

### 组合 B（中期可扩展）
- 美术：Kenney + LPC Expanded
- UI：Mantine Indicator
- 实时：Yjs + y-websocket
- 适用：多人长连接 + presence + 后续协作编辑

## 风险与规避
1. **许可证混用风险（CC-BY-SA/GPL）**
   - 规避：优先 CC0/MIT；LPC 类资源单独隔离并记录来源。
2. **动作帧规格不一致**
   - 规避：统一导出帧尺寸（如 32x32 或 48x48）与命名约定。
3. **实时层过早复杂化**
   - 规避：MVP 先 Socket.IO 事件流，不提前引 CRDT。

## 本轮新增文件（最小准备）
- `research/star-office-assets/README.md`
- `research/star-office-assets/manifest.example.json`
- `research/star-office-assets/state-ui-mapping.example.json`
- `reports/star_office_resource_catalog.md`
- `reports/star_office_integration_plan_v2.md`

## 立即可执行命令（<=3）
```bash
mkdir -p assets/star-office/{tiles,characters,ui}
```
```bash
cp research/star-office-assets/manifest.example.json assets/star-office/manifest.json
```
```bash
python3 -m http.server 4173 --directory .
```
