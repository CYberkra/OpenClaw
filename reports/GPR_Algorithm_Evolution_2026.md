<!-- Slide number: 1 -->

![](图片13.jpg)
GPR 数据处理算法优化报告PPT

![](图片8.jpg)

![](图片7.jpg)

GPR Algorithm Evolution 2026

![](图片11.jpg)

![](图片16.jpg)

![](图片10.jpg)

![](图片12.jpg)

![](图片5.jpg)

<!-- Slide number: 2 -->

![](图片24.jpg)

基础预处理与校正
01
Pre-processing

频带滤波与去噪

02
目录
Filtering & Denoising

03
背景杂波抑制对比
CONTENTS
Clutter Suppression

04
增益成像与架构趋势
Gain & Architecture

<!-- Slide number: 3 -->

![](图片17.jpg)

![](图片9.jpg)

![](图片19.jpg)
基础预处理
01

Fundamental Pre-processing

![](图片21.jpg)

<!-- Slide number: 4 -->

![](图片14.jpg)

![](图片22.jpg)

![](图片21.jpg)

![](图片2.jpg)

![](图片23.jpg)

![](图片20.jpg)
EMA vs SVD

观察-变化-结论-建议
背景杂波抑制对比

观察：EMA 侧翼出现负振幅阴影；SVD 背景更干净

变化→结论→建议：SVD 更稳健；结合 SEC 适合后处理

<!-- Slide number: 5 -->

![](图片29.jpg)

![](图片1.jpg)

![](图片4.jpg)

![](图片3.jpg)

![](图片49.jpg)

![](图片48.jpg)
频带滤波与 F-K 滤波

SNR 提升与方向性干扰抑制
IIR vs FIR：速度与相位保真权衡

1D/2D 带通：裁剪低频漂移与高频噪声

![](图片31.jpg)

F-K 倾角滤波：抑制表面波/斜向干扰

<!-- Slide number: 6 -->

![](图片11.jpg)

![](图片17.jpg)

![](图片12.jpg)
去噪与降维
02

Denoising & Subspace Methods

![](图片13.jpg)

### Notes:

<!-- Slide number: 7 -->

![](图片4.jpg)

![](图片9.jpg)

![](图片21.jpg)

![](图片8.jpg)

![](图片20.jpg)

![](图片45.jpg)

![](图片36.jpg)
优势

从随机噪声中提取主成分结构
核心思想

Hankel-SVD / MSSA

轨迹矩阵 + 奇异值分解，保留主成分重构

代价

SNR 提升显著，边缘与子波形态保持

适用场景

计算量大，窗口/阶数敏感，需经验调参

<!-- Slide number: 8 -->

![](图片1.jpg)

![](图片18.jpg)

![](图片36.jpg)

![](图片17.jpg)

![](图片54.jpg)

![](图片53.jpg)

![](图片2.jpg)
Pipeline

从单道校正到偏移成像
标准处理链路
带通滤波

零时校正
Dewow 去漂移

F-K 滤波

![拼图 纯色填充](图形25.jpg)

![头上的大脑 纯色填充](图形23.jpg)

SEC/AGC 增益
偏移成像

背景杂波抑制

Hankel-SVD 去噪

![社交网络 纯色填充](图形29.jpg)

![灯泡和齿轮 纯色填充](图形27.jpg)

<!-- Slide number: 9 -->

![](图片15.jpg)

![](图片9.jpg)

![](图片16.jpg)
增益与成像
03

Gain Control & Imaging

![](图片17.jpg)

<!-- Slide number: 10 -->

![](图片3.jpg)

![](图片18.jpg)

![](图片17.jpg)

![](图片8.jpg)

![](图片23.jpg)

![](图片16.jpg)

SEC vs AGC

深部回波补偿与动态范围管理
增益控制策略

风险：噪声与伪影被同步放大
输出：为偏移成像提供稳定幅度

优点：提升深部目标可见度
建议：与去噪/杂波抑制联合

SEC：按传播时间指数补偿
AGC：滑动窗口能量归一化

### Notes:

<!-- Slide number: 11 -->

![](图片4.jpg)

![](图片9.jpg)

![](图片21.jpg)

![](图片8.jpg)

![](图片20.jpg)

![](图片45.jpg)

![](图片36.jpg)
云计算与并行

算法库 + 可视化 + 数据管理
模块化管线

现代 GUI 架构

前后端分离，插件化算法栈

AI 辅助解释

GPU/云端批处理提升吞吐

工程化部署

AI 识别目标并给出参数建议

<!-- Slide number: 12 -->

![](图片24.jpg)

![](图片9.jpg)

总结与下一步
Thank you for watching
下一步：参数自动化与 AI 目标识别
