# Star-Office Assets（可直接接入）

本目录用于“先复用、后定制”的素材接入准备，不改生产配置。

## 推荐优先级（按落地速度）
1. Office Space Tileset（CC0）
2. Pixel Art Lab/Office Tiles（CC-BY 3.0）
3. LPC Expanded（sit/walk/idle）
4. shadcn/ui Badge（状态UI）
5. Socket.IO（presence）

## 下载方式（建议）
1. 打开 `manifest.example.json` 中的 `sourceUrl`
2. 下载后解压到对应 `localPath`
3. 若资源要求署名（如 CC-BY），在项目后续 `THIRD_PARTY_NOTICES.md` 补充作者与链接

## 建议目录约定
- `assets/star-office/tiles/`：地图与家具贴图
- `assets/star-office/characters/`：人物动作帧
- `assets/star-office/ui/`：状态图标/徽章资源

## 接入提示
- MVP 仅使用 `idle/walk/sit` 三组动作即可。
- `state-ui-mapping.example.json` 已给出 reviewing/idle/debugging/coding 到动作与图标的映射模板。
- 实时层先用 Socket.IO，若后续需要多人协同文档/强一致，再升级 Yjs Awareness。
