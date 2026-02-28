# GPR 简易GUI（建议版）

文件：`gpr_gui.py`

## 功能
- 读取你们当前格式 CSV（前4行头信息 + 5列数据）
- 文本框显示头信息与当前矩阵统计
- 绘制双图对比（原始 B-scan vs 当前处理后 B-scan）
- 支持 A-scan 单道波形查看
- 支持常用处理：
  - dewow
  - set zero-time
  - AGC
  - subtracting average 2D
  - running average 2D
  - compensating gain
- 一键推荐流程（dewow → zero-time → AGC → 背景抑制 → 平滑）
- 导出当前处理结果矩阵 CSV

## 运行
```bash
python3 gpr_gui.py
```

## 依赖
```bash
pip install numpy matplotlib
```

如果中文字体显示异常（方块/乱码），在 Ubuntu/WSL 执行：
```bash
sudo apt update
sudo apt install -y fonts-noto-cjk
```

## 输入格式说明（与你当前数据一致）
前4行：
- Number of Samples = xxx
- Time windows (ns) = xxx
- Number of Traces = xxx
- Trace interval (m) = xxx

后续每行5列：
- 经度, 纬度, 高程, 振幅值, 标记位

程序会自动重组为 `samples × traces` 的 B-scan 矩阵。
