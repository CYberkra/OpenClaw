# 探地雷达 (GPR) 信号处理技术报告
- 生成日期：2026-03-02
- 数据：A8-NEW-1.csv (801×79)
- 主题：背景抑制 + AGC 改进

---

## 目录
- 背景与原始流程
- 调研与改进方法
- 处理链与消融对比
- 指标定义
- 问题与下一步

---

## 原始流程（Baseline）
> 处理链路
- readcsv → reshape(801,79)
- AGC → 背景抑制 → 输出 PNG

> 核心脚本
- agcGain.py
- subtracting_average_2D.py
- read_file_data.py

---

## 原始方法的痛点
- AGC 增益无上限 → 噪声放大
- 背景抑制窗口固定 → 适应性差
- 第 79 道 NaN → 指标失真

> 💡 Tip
后续优先处理 NaN trace 与参数消融。

---

## 调研结论（15 篇初筛）
| 编号 | 方法 | 核心思路 | 可实现要点 |
|---|---|---|---|
| 4 | F-K 域杂波抑制 | 角度阻带滤波 | 10°–65° 抑制 |
| 5 | WNNM | 加权核范数 | 替代 SVD |
| 6 | Learned RPCA | 学习式低秩分解 | 降低迭代开销 |
| 9 | Hankel-SVD | 滑窗矩阵 SVD | 去噪稳健 |
| 13 | DTVM | 方向性 TV | 方向权重选择 |

---

## 复刻改进 A：SVD 低秩背景抑制
```python
U, S, Vt = svd(agc_output, full_matrices=False)
rank = 1
background = U[:, :rank] @ diag(S[:rank]) @ Vt[:rank, :]
output = agc_output - background
```
- **效果**：SNR 11.64 dB；SSIM 0.995
- **速度**：0.65s（比基线快 44%）

---

## 复刻改进 B：AGC + 增益上限
```python
window = 301
gain_cap = 10
# AGC 限幅 → subtracting_average_2D
```
- **效果**：SNR 8.33 dB；SSIM 0.210
- **结论**：当前参数下性能下降，需要调参

---

## 完整 6 步处理链（GPR_GUI）
<!-- two-column -->
> Step 1–3
- compensatingGain
- dewow (window=23)
- set_zero_time (5.7ns)
<!-- right -->
> Step 4–6
- agcGain (window=151)
- subtracting_average_2D (ntraces=79)
- running_average_2D (ntraces=9)
<!-- end -->

---

## 消融指标对比
| 方法 | SNR (dB) | 对比度 | SSIM | 耗时 (s) |
|---|---:|---:|---:|---:|
| Baseline | 11.97 | 4.26 | 1.000 | 1.16 |
| SVD 背景抑制 | 11.64 | 4.04 | 0.995 | 0.65 |
| AGC 改进 | 8.33 | 2.65 | 0.210 | 0.71 |

> 💡 Tip
SVD 方案在速度与质量之间更平衡。

---

## 指标定义
- **SNR**：`20*log10(RMS_target/RMS_noise)`
- **对比度**：`(max_target - min_target)/(max_noise - min_noise)`
- **SSIM**：min-max 归一化后全局 SSIM

---

## 待解决问题
- NaN trace：第 79 道需剔除/填补
- SVD 秩选择：rank=1 为经验值
- AGC 参数：窗口与 cap 需系统消融
- 文献精读：需外网获取细节

---

## 输出与交付
- 报告：`reports/GPR_技术报告_2026-03-02.md`
- PPT：`reports/探地雷达_背景抑制与AGC改进_汇报_2026-03-02.pptx`
- 图像：`repos/GPR_GUI/output/A8-NEW-1_*.png`

> 💡 Tip
建议：优先产出 SVD 方案的参数消融实验。
