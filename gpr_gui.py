#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易 GPR 数据处理 GUI（基于 Tkinter + Matplotlib）
功能：
1) 读取你们当前格式 CSV（前4行头信息 + [lon,lat,elev,amp,flag] 数据）
2) 显示基本信息（文本框）
3) 绘制 B-scan 图像
4) 提供常用处理：dewow / set zero-time / AGC / background removal / running average / compensating gain
"""

from __future__ import annotations

import csv
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


@dataclass
class GPRData:
    raw_path: str
    header: Dict[str, float]
    matrix: np.ndarray               # shape: [samples, traces]
    trace_meta: np.ndarray           # shape: [traces, 3] -> [lon, lat, elev]
    flag_matrix: np.ndarray          # shape: [samples, traces]


class GPRProcessor:
    @staticmethod
    def dewow(data: np.ndarray, window: int = 23) -> np.ndarray:
        if window < 1:
            raise ValueError("window must >= 1")
        samples, _ = data.shape
        if window >= samples:
            return data - np.mean(data, axis=0, keepdims=True)

        out = np.zeros_like(data, dtype=float)
        half = int(window / 2)

        avg = np.mean(data[0:half + 1, :], axis=0)
        out[0:half + 1, :] = data[0:half + 1, :] - avg

        for s in range(half, samples - half):
            win = data[s - half:s + half + 1, :]
            out[s, :] = data[s, :] - np.mean(win, axis=0)

        avg = np.mean(data[samples - half:samples, :], axis=0)
        out[samples - half:samples, :] = data[samples - half:samples, :] - avg
        return out

    @staticmethod
    def set_zero_time(data: np.ndarray, total_time_ns: float, new_zero_time_ns: float) -> Tuple[np.ndarray, float]:
        new_zero_time_ns = abs(float(new_zero_time_ns))
        if total_time_ns <= 0:
            raise ValueError("total_time_ns must > 0")
        if new_zero_time_ns >= total_time_ns:
            raise ValueError("new_zero_time_ns must be smaller than total_time_ns")

        samples = data.shape[0]
        twtt = np.linspace(0, total_time_ns, samples)
        zero_idx = int(np.abs(twtt - new_zero_time_ns).argmin())
        cut = data[zero_idx:, :]
        new_total = total_time_ns - new_zero_time_ns
        return cut, new_total

    @staticmethod
    def agc_gain(data: np.ndarray, window: int = 151, eps: float = 1e-8) -> np.ndarray:
        if window < 1:
            raise ValueError("window must >= 1")

        samples, _ = data.shape
        out = np.zeros_like(data, dtype=float)
        if window >= samples:
            energy = np.maximum(np.linalg.norm(data, axis=0), eps)
            return data / energy

        half = int(window / 2)
        energy = np.maximum(np.linalg.norm(data[0:half + 1, :], axis=0), eps)
        out[0:half + 1, :] = data[0:half + 1, :] / energy

        for s in range(half, samples - half):
            win = data[s - half:s + half + 1, :]
            energy = np.maximum(np.linalg.norm(win, axis=0), eps)
            out[s, :] = data[s, :] / energy

        energy = np.maximum(np.linalg.norm(data[samples - half:samples, :], axis=0), eps)
        out[samples - half:samples, :] = data[samples - half:samples, :] / energy
        return out

    @staticmethod
    def subtracting_average_2d(data: np.ndarray, ntraces: int = 51) -> np.ndarray:
        if ntraces < 1:
            raise ValueError("ntraces must >= 1")

        samples, traces = data.shape
        if ntraces >= traces:
            return data - np.mean(data, axis=1, keepdims=True)

        out = np.zeros_like(data, dtype=float)
        half = int(ntraces / 2)

        avg_tr = np.mean(data[:, 0:half + 1], axis=1, keepdims=True)
        out[:, 0:half + 1] = data[:, 0:half + 1] - avg_tr

        for t in range(half, traces - half):
            win = data[:, t - half:t + half + 1]
            avg_tr = np.mean(win, axis=1)
            out[:, t] = data[:, t] - avg_tr

        avg_tr = np.mean(data[:, traces - half:traces], axis=1, keepdims=True)
        out[:, traces - half:traces] = data[:, traces - half:traces] - avg_tr
        return out

    @staticmethod
    def running_average_2d(data: np.ndarray, ntraces: int = 9) -> np.ndarray:
        if ntraces < 1:
            raise ValueError("ntraces must >= 1")

        samples, traces = data.shape
        if ntraces == 1:
            return data.copy()
        if ntraces >= traces:
            return np.repeat(np.mean(data, axis=1, keepdims=True), traces, axis=1)

        out = np.zeros_like(data, dtype=float)
        half = int(ntraces / 2)

        avg_tr = np.mean(data[:, 0:half + 1], axis=1, keepdims=True)
        out[:, 0:half + 1] = np.repeat(avg_tr, half + 1, axis=1)

        for t in range(half, traces - half):
            win = data[:, t - half:t + half + 1]
            out[:, t] = np.mean(win, axis=1)

        avg_tr = np.mean(data[:, traces - half:traces], axis=1, keepdims=True)
        out[:, traces - half:traces] = np.repeat(avg_tr, half, axis=1)
        return out

    @staticmethod
    def compensating_gain(data: np.ndarray, gain_start_db: float = 0.0, gain_end_db: float = 24.0) -> np.ndarray:
        samples, traces = data.shape
        gain_db = np.linspace(gain_start_db, gain_end_db, samples)
        real_gain = 10 ** (gain_db / 20.0)
        gain = np.tile(real_gain[:, None], (1, traces))
        return data * gain


class GPRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GPR 简易处理GUI")
        self.geometry("1300x840")

        self.gpr: Optional[GPRData] = None
        self.current_data: Optional[np.ndarray] = None
        self.current_total_time_ns: Optional[float] = None

        self._build_ui()

    def _build_ui(self):
        left = ttk.Frame(self)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        right = ttk.Frame(self)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        # File controls
        f_file = ttk.LabelFrame(left, text="文件")
        f_file.pack(fill=tk.X, pady=4)

        ttk.Button(f_file, text="打开CSV", command=self.open_csv).pack(fill=tk.X, padx=6, pady=6)
        ttk.Button(f_file, text="保存当前矩阵CSV", command=self.save_current_matrix).pack(fill=tk.X, padx=6, pady=6)

        # Parameters
        f_param = ttk.LabelFrame(left, text="处理参数")
        f_param.pack(fill=tk.X, pady=4)

        self.var_dewow = tk.StringVar(value="23")
        self.var_zero = tk.StringVar(value="5.7")
        self.var_agc = tk.StringVar(value="151")
        self.var_subavg = tk.StringVar(value="51")
        self.var_runavg = tk.StringVar(value="9")
        self.var_gain_start = tk.StringVar(value="0")
        self.var_gain_end = tk.StringVar(value="24")

        self._row_entry(f_param, "dewow window", self.var_dewow)
        self._row_entry(f_param, "new zero time(ns)", self.var_zero)
        self._row_entry(f_param, "agc window", self.var_agc)
        self._row_entry(f_param, "subtract ntraces", self.var_subavg)
        self._row_entry(f_param, "running ntraces", self.var_runavg)
        self._row_entry(f_param, "gain start(db)", self.var_gain_start)
        self._row_entry(f_param, "gain end(db)", self.var_gain_end)

        # Actions
        f_action = ttk.LabelFrame(left, text="处理操作")
        f_action.pack(fill=tk.X, pady=4)

        ttk.Button(f_action, text="重置为原始数据", command=self.reset_data).pack(fill=tk.X, padx=6, pady=4)
        ttk.Button(f_action, text="dewow", command=self.apply_dewow).pack(fill=tk.X, padx=6, pady=4)
        ttk.Button(f_action, text="set zero-time", command=self.apply_zero_time).pack(fill=tk.X, padx=6, pady=4)
        ttk.Button(f_action, text="AGC", command=self.apply_agc).pack(fill=tk.X, padx=6, pady=4)
        ttk.Button(f_action, text="subtracting average 2D", command=self.apply_subavg).pack(fill=tk.X, padx=6, pady=4)
        ttk.Button(f_action, text="running average 2D", command=self.apply_runavg).pack(fill=tk.X, padx=6, pady=4)
        ttk.Button(f_action, text="compensating gain", command=self.apply_comp_gain).pack(fill=tk.X, padx=6, pady=4)
        ttk.Button(f_action, text="一键推荐流程", command=self.apply_recommended_pipeline).pack(fill=tk.X, padx=6, pady=6)

        # Info text
        f_info = ttk.LabelFrame(left, text="基本信息")
        f_info.pack(fill=tk.BOTH, expand=True, pady=4)

        self.info_text = tk.Text(f_info, height=20, width=44)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Plot
        fig = Figure(figsize=(9, 7), dpi=100)
        self.ax = fig.add_subplot(111)
        self.ax.set_title("B-scan")
        self.ax.set_xlabel("Trace")
        self.ax.set_ylabel("Time Sample")

        self.canvas = FigureCanvasTkAgg(fig, master=right)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, right, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(fill=tk.X)

    @staticmethod
    def _row_entry(parent, label, var):
        row = ttk.Frame(parent)
        row.pack(fill=tk.X, padx=6, pady=2)
        ttk.Label(row, text=label, width=18).pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=var, width=12).pack(side=tk.RIGHT)

    def log_info(self, text: str):
        self.info_text.insert(tk.END, text + "\n")
        self.info_text.see(tk.END)

    def set_info(self, text: str):
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, text)

    def open_csv(self):
        path = filedialog.askopenfilename(title="选择GPR CSV", filetypes=[("CSV", "*.csv"), ("All", "*.*")])
        if not path:
            return
        try:
            self.gpr = self._parse_gpr_csv(path)
            self.current_data = self.gpr.matrix.copy()
            self.current_total_time_ns = float(self.gpr.header.get("Time windows (ns)", self.gpr.matrix.shape[0] - 1))
            self._refresh_info_panel()
            self.plot_bscan(self.current_data)
            self.log_info(f"[OK] 已加载文件: {path}")
        except Exception as e:
            messagebox.showerror("读取失败", str(e))

    def _parse_gpr_csv(self, path: str) -> GPRData:
        with open(path, "r", encoding="utf-8", errors="ignore", newline="") as f:
            reader = csv.reader(f)
            rows = [r for r in reader if r]

        if len(rows) < 10:
            raise ValueError("CSV内容过短，可能不是预期格式")

        # parse header
        header = {}
        for i in range(4):
            row = rows[i]
            k, v = self._parse_header_row(row)
            if k:
                header[k] = v

        n_samples = int(header.get("Number of Samples", 0))
        n_traces = int(header.get("Number of Traces", 0))

        data_rows = rows[4:]
        if n_samples <= 0 or n_traces <= 0:
            # fallback infer
            n_samples = int(header.get("Number of Samples", 801))
            n_traces = len(data_rows) // n_samples

        expected = n_samples * n_traces
        if len(data_rows) < expected:
            raise ValueError(f"数据行不足，期望 >= {expected} 行，实际 {len(data_rows)}")

        data_rows = data_rows[:expected]

        arr = np.array([[float(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4])] for r in data_rows], dtype=float)
        arr = arr.reshape((n_traces, n_samples, 5))  # [trace, sample, fields]

        trace_meta = arr[:, 0, 0:3]                 # [n_traces, 3]
        amp = arr[:, :, 3].T                        # [n_samples, n_traces]
        flag = arr[:, :, 4].T

        return GPRData(raw_path=path, header=header, matrix=amp, trace_meta=trace_meta, flag_matrix=flag)

    @staticmethod
    def _parse_header_row(row) -> Tuple[str, float]:
        text = ",".join(row)
        if "=" not in text:
            return "", 0.0
        left, right = text.split("=", 1)
        key = left.strip()
        val_str = right.split(",")[0].strip()
        try:
            val = float(val_str)
        except Exception:
            val = 0.0
        return key, val

    def _refresh_info_panel(self):
        if self.gpr is None or self.current_data is None:
            return
        h = self.gpr.header
        samples, traces = self.current_data.shape
        txt = []
        txt.append(f"文件: {os.path.basename(self.gpr.raw_path)}")
        txt.append(f"原始路径: {self.gpr.raw_path}")
        txt.append("\n[Header]")
        for k, v in h.items():
            txt.append(f"- {k}: {v}")
        txt.append("\n[Current Matrix]")
        txt.append(f"- shape: {self.current_data.shape}")
        txt.append(f"- min/max: {np.min(self.current_data):.6f} / {np.max(self.current_data):.6f}")
        txt.append(f"- mean/std: {np.mean(self.current_data):.6f} / {np.std(self.current_data):.6f}")

        lon0, lat0, h0 = self.gpr.trace_meta[0]
        lon1, lat1, h1 = self.gpr.trace_meta[-1]
        txt.append("\n[Track Meta]")
        txt.append(f"- traces: {traces}")
        txt.append(f"- samples per trace: {samples}")
        txt.append(f"- first trace (lon,lat,elev): ({lon0:.7f}, {lat0:.7f}, {h0:.3f})")
        txt.append(f"- last  trace (lon,lat,elev): ({lon1:.7f}, {lat1:.7f}, {h1:.3f})")
        txt.append(f"- current total time(ns): {self.current_total_time_ns}")

        self.set_info("\n".join(txt))

    def plot_bscan(self, data: np.ndarray):
        self.ax.clear()
        vmax = np.percentile(np.abs(data), 99)
        vmax = max(vmax, 1e-9)
        self.ax.imshow(data, aspect="auto", cmap="seismic", vmin=-vmax, vmax=vmax, origin="upper")
        self.ax.set_title("B-scan")
        self.ax.set_xlabel("Trace")
        self.ax.set_ylabel("Time Sample")
        self.canvas.draw_idle()

    def _check_loaded(self):
        if self.current_data is None:
            messagebox.showwarning("提示", "请先加载CSV")
            return False
        return True

    def reset_data(self):
        if self.gpr is None:
            messagebox.showwarning("提示", "请先加载CSV")
            return
        self.current_data = self.gpr.matrix.copy()
        self.current_total_time_ns = float(self.gpr.header.get("Time windows (ns)", self.current_data.shape[0] - 1))
        self.plot_bscan(self.current_data)
        self._refresh_info_panel()
        self.log_info("[OK] 已重置为原始数据")

    def apply_dewow(self):
        if not self._check_loaded():
            return
        w = int(self.var_dewow.get())
        self.current_data = GPRProcessor.dewow(self.current_data, w)
        self.plot_bscan(self.current_data)
        self._refresh_info_panel()
        self.log_info(f"[OK] dewow(window={w})")

    def apply_zero_time(self):
        if not self._check_loaded():
            return
        z = float(self.var_zero.get())
        self.current_data, self.current_total_time_ns = GPRProcessor.set_zero_time(
            self.current_data, float(self.current_total_time_ns), z
        )
        self.plot_bscan(self.current_data)
        self._refresh_info_panel()
        self.log_info(f"[OK] set_zero_time(new_zero_time_ns={z})")

    def apply_agc(self):
        if not self._check_loaded():
            return
        w = int(self.var_agc.get())
        self.current_data = GPRProcessor.agc_gain(self.current_data, w)
        self.plot_bscan(self.current_data)
        self._refresh_info_panel()
        self.log_info(f"[OK] agc(window={w})")

    def apply_subavg(self):
        if not self._check_loaded():
            return
        n = int(self.var_subavg.get())
        self.current_data = GPRProcessor.subtracting_average_2d(self.current_data, n)
        self.plot_bscan(self.current_data)
        self._refresh_info_panel()
        self.log_info(f"[OK] subtracting_average_2D(ntraces={n})")

    def apply_runavg(self):
        if not self._check_loaded():
            return
        n = int(self.var_runavg.get())
        self.current_data = GPRProcessor.running_average_2d(self.current_data, n)
        self.plot_bscan(self.current_data)
        self._refresh_info_panel()
        self.log_info(f"[OK] running_average_2D(ntraces={n})")

    def apply_comp_gain(self):
        if not self._check_loaded():
            return
        gs = float(self.var_gain_start.get())
        ge = float(self.var_gain_end.get())
        self.current_data = GPRProcessor.compensating_gain(self.current_data, gs, ge)
        self.plot_bscan(self.current_data)
        self._refresh_info_panel()
        self.log_info(f"[OK] compensating_gain(start_db={gs}, end_db={ge})")

    def apply_recommended_pipeline(self):
        if not self._check_loaded():
            return
        try:
            self.apply_dewow()
            self.apply_zero_time()
            self.apply_agc()
            self.apply_subavg()
            self.apply_runavg()
            self.log_info("[OK] 一键推荐流程完成")
        except Exception as e:
            messagebox.showerror("流程执行失败", str(e))

    def save_current_matrix(self):
        if not self._check_loaded():
            return
        out = filedialog.asksaveasfilename(
            title="保存当前矩阵CSV",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("All", "*.*")],
        )
        if not out:
            return
        np.savetxt(out, self.current_data, delimiter=",")
        self.log_info(f"[OK] 已保存矩阵: {out}")
        messagebox.showinfo("完成", f"已保存:\n{out}")


if __name__ == "__main__":
    app = GPRApp()
    app.mainloop()
