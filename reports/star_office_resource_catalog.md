# Star-Office 资源复用清单（v2）

目标：优先复用开源/现成资源，避免从零制作美术与实时协作底座。

> 说明：以下“可商用限制”按公开许可证与常见条款做工程视角整理，最终上线前建议二次法务确认。

## A. 像素办公室地图 / tileset

| 资源 | 类型 | 许可证 | 链接 | 可商用限制 | 接入难度 |
|---|---|---|---|---|---|
| OpenGameArt - Office Space Tileset | 办公场景 tileset | CC0 | https://opengameart.org/content/office-space-tileset | 可商用；可修改；无需署名（建议保留来源记录） | 低 |
| OpenGameArt - Pixel Art Lab/Office Tiles | 实验室/办公室 tileset | CC-BY 3.0 | https://opengameart.org/content/pixel-art-laboffice-tiles | 可商用；**必须署名**原作者；衍生可闭源 | 低 |
| Kenney - Top-down 资产集合（含现代场景可拼办公室） | 2D top-down 素材包 | CC0 | https://www.kenney.nl/assets/tag:top-down | 可商用；可改造；无需署名 | 低 |
| Kenney - Top-down Shooter（可拆室内道具/地面） | top-down tiles & props | CC0 | https://kenney.nl/assets/top-down-shooter | 可商用；可修改；无强制署名 | 低 |

## B. 像素人物 sprite（行走/坐下/闲置）

| 资源 | 动作覆盖 | 许可证 | 链接 | 可商用限制 | 接入难度 |
|---|---|---|---|---|---|
| LPC Expanded: Sit, Run, Jump, & More | **sit / run / walk / idle 可扩展** | 常见为 CC-BY-SA 3.0 / GPLv3（以页面标注为准） | https://opengameart.org/content/lpc-expanded-sit-run-jump-more | 可商用；需署名；若采用 SA/GPL 资源需注意传播条款 | 中 |
| Universal LPC Spritesheet Generator | 组合式角色生成（含多方向基础动作） | CC-BY-SA 3.0（项目说明） | https://github.com/LiberatedPixelCup/Universal-LPC-Spritesheet-Character-Generator | 可商用；需署名；SA 条款对再分发有要求 | 中 |
| OpenGameArt - Walk Cycles 集合（含 worker 风格条目） | walk / idle（部分条目） | 混合（CC0/CC-BY/OGA-BY，按子条目） | https://opengameart.org/content/walk-cycles-0 | 可商用通常可行；需逐条核验许可证 | 中 |

## C. 可视化状态 UI 组件（状态徽标/在线态/标签）

| 资源 | 适配框架 | 许可证 | 链接 | 可商用限制 | 接入难度 |
|---|---|---|---|---|---|
| shadcn/ui（Badge 等） | React / Next.js | MIT | https://github.com/shadcn-ui/ui | 可商用；允许修改与闭源集成；保留许可声明 | 低 |
| Mantine（Badge/Indicator） | React | MIT | https://mantine.dev/core/badge/ | 可商用；可闭源；保留许可文本 | 低 |
| Chakra UI（Badge/Avatar 状态） | React | MIT | https://github.com/chakra-ui/chakra-ui | 可商用；可闭源；保留许可 | 低 |

## D. 多人 presence / 实时同步方案

| 资源 | 能力 | 许可证 | 链接 | 可商用限制 | 接入难度 |
|---|---|---|---|---|---|
| Yjs + Awareness + y-websocket | CRDT 文档同步 + 在线态广播 | MIT | https://docs.yjs.dev/getting-started/adding-awareness | 可商用；可自托管；许可宽松 | 中 |
| Socket.IO | 实时事件/房间/Presence 基础层 | MIT | https://github.com/socketio/socket.io | 可商用；可自托管 | 低 |
| Supabase Realtime | Broadcast/Presence/DB change | Apache-2.0（服务端） | https://github.com/supabase/realtime | 可商用；自托管可行；云服务按套餐计费 | 中 |
| Colyseus | 房间状态同步（多人房间） | MIT | https://colyseus.io/ | 可商用；可自托管 | 中 |
| Liveblocks | 现成协作能力（presence/comment等） | 客户端多数 Apache-2.0 + 平台服务条款 | https://liveblocks.io/ | SDK 可商用；托管服务按定价，需遵守服务条款 | 低-中 |

---

## 快速结论（按“可直接套用”优先）

1. **最省事全开源路径**：`Kenney/OpenGameArt(CC0或CC-BY) + shadcn/ui + Socket.IO`。
2. **动作丰富角色路径**：优先 LPC Expanded（直接有 sit），再按项目需要裁切方向帧。
3. **可演进实时路径**：MVP 先 Socket.IO，后续若出现离线并发编辑冲突再升级 Yjs。
4. **商用上线要点**：仅保留“许可清单 + attribution 文件”即可覆盖大多数开源素材合规。