# GUI 性能优化简报（GPR_GUI）

- 时间：2026-03-09
- 仓库：`/mnt/e/Openclaw/.openclaw/workspace/repos/GPR_GUI`
- 目标：定位 GUI 卡顿热点并实施低风险优化，保持功能/输出兼容

## 1) 热点定位

基于代码路径检查，主要瓶颈集中在：

1. **绘图刷新风暴**
   - 多个控件 (`crop/cmap/grid/...`) 直接绑定 `_refresh_plot -> plot_data`，连续操作时会触发高频重绘。
2. **批处理主线程阻塞**
   - `run_batch` 原为同步串行，方法多时 UI 容易“卡住”。
3. **核心方法重复 I/O**
   - core 方法执行后先产出 CSV/PNG，再由 GUI `_save_outputs` 再次落盘，存在冗余写入链路。
4. **显示降采样重复索引计算**
   - 每次刷新都重复 `linspace` 计算索引。
5. **core 模块反复 import / CSV 读取路径未优化**
   - 每步动态 import，CSV 读取未显式走 dense numeric 优化参数。

## 2) 已落地优化（不改变功能行为）

### A. 绘图刷新去抖（Debounce）
- 新增 `QTimer(singleShot)`，`_refresh_plot` 改为 30ms 合并触发，实际重绘在 `_do_refresh_plot`。
- `canvas.draw()` 改为 `canvas.draw_idle()`，减少同步阻塞重绘。

### B. 批处理异步化（主线程解耦）
- `run_batch` 从同步执行改为构建任务列表后走既有 `ProcessingWorker + QThread`。
- 处理逻辑仍按选中顺序串行执行，**功能顺序不变**，但 UI 可响应。

### C. 核心 I/O 链路减冗余
- `ProcessingWorker` 内 core 中间产物改写到 `__tmp_*` 文件，避免与最终输出路径冲突。
- 保留 `_save_outputs` 的最终导出行为（兼容当前输出语义），减少重复落盘开销。

### D. 避免重复计算
- 新增 `_get_downsample_indices` 缓存（LRU-like 简易缓存，超 64 清空）。
- `_downsample_data` / `_downsample_for_display` 复用索引，降低反复刷新开销。

### E. 轻量读取优化
- 新增 `_read_matrix_csv_fast`：优先 `pandas.read_csv(..., na_filter=False, low_memory=False)`，异常回退 `np.loadtxt`。
- core 步骤中 CSV 回读统一走该函数。
- core 模块函数通过 `_get_core_func` 做缓存，避免重复 import。

## 3) 最小性能基准（前后对比，3项）

执行脚本：`python3 tools/gui_perf_benchmark.py`

结果：

1. **CSV 读取**：old=0.1124s, new=0.1050s, **1.07x**
2. **绘图刷新风暴（20次触发）**：old=0.2150s, new=0.0105s, **20.57x**
3. **批处理核心 I/O**：old=0.6394s, new=0.6337s, **1.01x**

> 注：第 2 项收益主要来自刷新合并与非阻塞绘制策略，对交互顺滑度影响最大。

## 4) 兼容性说明

- 方法参数、方法执行顺序、最终导出入口保持不变。
- 批处理从“同步执行”改为“异步执行”，属于交互层改进，不改变处理结果语义。
- 输出文件仍通过 `_save_outputs` 统一生成，保证与原有报告/导出流程兼容。

## 5) 风险与建议

### 已识别风险
1. **时序风险（低）**：异步批处理期间用户若再次触发处理，依赖现有“忙碌态”保护。
2. **临时文件风险（低）**：`output` 下新增 `__tmp_*` 中间文件，异常中断时可能残留。
3. **基准代表性（中）**：当前基准为 micro-benchmark，建议再用真实大 CSV 做一次端到端验证。

### 建议
- 后续可增加：启动时清理 `output/__tmp_*`。
- 对超大数据加载可进一步引入后台加载 worker（当前未改，以降低行为变更风险）。

## 6) 变更文件

- `app_qt.py`
- `tools/gui_perf_benchmark.py`
