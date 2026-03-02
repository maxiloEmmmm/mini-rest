#!/usr/bin/env python3
"""
极简休息提醒器 - 25分钟，5分钟休息
跨平台：macOS / Windows / Linux
"""

import tkinter as tk
from tkinter import font as tkfont
import sys

class RestTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("休息提醒")
        self.root.geometry("320x160")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#FFF0F5")  # 淡粉色背景

        # 二次元配色
        self.COLOR_BG = "#FFF0F5"        # 淡粉背景
        self.COLOR_PINK = "#FFB7C5"      # 樱花粉
        self.COLOR_PURPLE = "#E6E6FA"    # 淡紫
        self.COLOR_BLUE = "#B0E0E6"      # 粉蓝
        self.COLOR_TEXT = "#6B5B73"      # 柔和紫灰
        self.COLOR_ACCENT = "#FF69B4"    # 热粉强调色

        # 配置
        self.WORK_TIME = 25 * 60      # 25分钟
        self.REST_TIME = 5 * 60       # 5分钟
        self.remaining = self.WORK_TIME
        self.is_resting = False

        # 构建界面
        self._build_ui()

        # 启动计时
        self._tick()

    def _create_rounded_button(self, parent, text, command, bg_color, fg_color="white"):
        """创建圆角风格的二次元按钮"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.COLOR_ACCENT,
            activeforeground="white"
        )
        return btn

    def _build_ui(self):
        # 时间显示区域（两行）
        self.time_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        self.time_frame.pack(pady=10)

        # 主倒计时
        self.time_label = tk.Label(
            self.time_frame,
            text=self._fmt(self.remaining),
            font=("Arial", 32, "bold"),
            bg=self.COLOR_BG,
            fg=self.COLOR_ACCENT
        )
        self.time_label.pack()

        # 闲置时间提示（默认隐藏）
        self.idle_hint = tk.Label(
            self.time_frame,
            text="",
            font=("Arial", 9),
            bg=self.COLOR_BG,
            fg="#999999"
        )
        self.idle_hint.pack()

        # 按钮区域
        self.btn_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        self.btn_frame.pack(pady=8)

        self.reset_btn = self._create_rounded_button(
            self.btn_frame,
            "重置",
            self._reset_work,
            self.COLOR_PINK
        )
        self.reset_btn.pack(side=tk.LEFT, padx=8)

        self.rest_btn = self._create_rounded_button(
            self.btn_frame,
            "休息",
            self._start_rest,
            self.COLOR_BLUE,
            self.COLOR_TEXT
        )
        self.rest_btn.pack(side=tk.LEFT, padx=8)

        # 立即开始按钮（休息中按ESC后显示）
        self.start_btn = self._create_rounded_button(
            self.root,
            "开始",
            self._end_rest,
            self.COLOR_ACCENT
        )

    def _fmt(self, seconds):
        m = seconds // 60
        s = seconds % 60
        return f"{m:02d}:{s:02d}"

    def _tick(self):
        if self.remaining > 0:
            self.remaining -= 1
            self.time_label.config(text=self._fmt(self.remaining))

            # 距离休息还有5分钟时提醒
            if self.remaining == 5 * 60 and not self.is_resting:
                self._show_reminder()

            if self.remaining == 0:
                if self.is_resting:
                    # 休息结束，开始闲置计时
                    self._start_idle()
                else:
                    self._start_rest()

        self.root.after(1000, self._tick)

    def _show_reminder(self):
        """显示5分钟后休息的提醒（顶部小窗口，3秒后自动关闭，显示在活跃屏幕）"""
        reminder = tk.Toplevel()
        reminder.configure(bg=self.COLOR_PINK)  # 樱花粉背景
        reminder.attributes('-topmost', True)
        reminder.overrideredirect(True)  # 无边框
        reminder.resizable(False, False)

        # 小窗口尺寸
        width, height = 220, 45

        # 获取主窗口位置
        self.root.update_idletasks()
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()

        # 计算提醒窗口位置：主窗口水平居中，垂直在主窗口上方或屏幕顶部
        x = root_x + (root_width - width) // 2
        y = max(0, root_y - height - 10)  # 主窗口上方10像素，或屏幕顶部

        reminder.geometry(f"{width}x{height}+{x}+{y}")

        # 显示文字
        tk.Label(
            reminder,
            text="5分钟后休息",
            font=("Arial", 12, "bold"),
            bg=self.COLOR_PINK,
            fg="white"
        ).pack(expand=True)

        # 3秒后自动关闭
        self.root.after(3000, reminder.destroy)

    def _start_idle(self):
        """休息结束，开始闲置计时（从0递增）"""
        self.is_resting = False
        self.is_idle = True
        self.idle_time = 0
        self.time_label.config(fg="#FF8FA3", text="+00:00")
        self.idle_hint.config(text="点击或移动开始工作", fg="#CCCCCC")  # 提示文字

        # 关闭休息窗口
        if hasattr(self, 'rest_window') and self.rest_window.winfo_exists():
            self.rest_window.destroy()
        self.root.deiconify()
        self.root.attributes('-topmost', True)

        # 隐藏原按钮
        self.btn_frame.pack_forget()

        # 绑定事件等待用户操作（任意键、点击、移动）
        self.root.bind('<Key>', lambda e: self._end_idle())
        self.root.bind('<Button>', lambda e: self._end_idle())
        self.root.bind('<Motion>', lambda e: self._end_idle())

        # 启动闲置计时
        self._tick_idle()

    def _tick_idle(self):
        """闲置计时递增"""
        if not self.is_idle:
            return
        self.idle_time += 1
        m = self.idle_time // 60
        s = self.idle_time % 60
        self.time_label.config(text=f"+{m:02d}:{s:02d}", fg="#FF8FA3")
        self.idle_hint.config(text="")  # 清除闲置提示
        self.root.after(1000, self._tick_idle)

    def _end_idle(self):
        """结束闲置，开始25分钟倒计时"""
        self.is_idle = False
        self.root.unbind('<Key>')
        self.root.unbind('<Button>')
        self.root.unbind('<Motion>')
        self.start_btn.pack_forget()  # 隐藏立即开始按钮
        self.btn_frame.pack(pady=5)  # 显示正常按钮
        self.is_resting = False
        self.remaining = self.WORK_TIME

        # 设置工作倒计时显示（二次元粉色）
        self.time_label.config(fg=self.COLOR_ACCENT, text=self._fmt(self.remaining))

        # 显示闲置时长提示（如果>0，工作中一直显示）
        if self.idle_time > 0:
            m = self.idle_time // 60
            s = self.idle_time % 60
            self.idle_hint.config(text=f"闲置了 {m}分{s}秒", fg="#999999")

        # 自动最小化窗口
        self.root.iconify()

    def _start_rest(self):
        """开始休息 - 全屏粉色窗口"""
        self.is_resting = True
        self.remaining = self.REST_TIME

        # 最小化主窗口
        self.root.iconify()

        # 隐藏主窗口
        self.root.withdraw()

        # 创建全屏休息窗口（二次元柔和风格）
        self.rest_window = tk.Toplevel()
        self.rest_window.configure(bg="#FFE4E1")  # 柔和的蜜桃粉
        self.rest_window.attributes('-fullscreen', True)
        self.rest_window.attributes('-topmost', True)
        self.rest_window.bind('<Key>', lambda e: None)  # 拦截键盘
        self.rest_window.bind('<Button>', lambda e: None)  # 拦截鼠标
        self.rest_window.bind('<Escape>', self._exit_fullscreen)  # ESC退出全屏但保持休息

        # 阻止关闭
        self.rest_window.protocol("WM_DELETE_WINDOW", lambda: None)

        # 二次元风格字体（较小较柔和）
        big_font = tkfont.Font(family="Arial", size=42, weight="bold")

        # 剩余时间显示（带柔和阴影效果）
        self.rest_time_label = tk.Label(
            self.rest_window,
            text=self._fmt(self.remaining),
            font=big_font,
            bg="#FFE4E1",
            fg="#FF8FA3"  # 柔和的粉色
        )
        self.rest_time_label.place(relx=0.5, rely=0.5, anchor="center")

        # 更新休息窗口时间
        self._update_rest_window()

    def _update_rest_window(self):
        """更新休息窗口的倒计时显示"""
        if not self.is_resting or not hasattr(self, 'rest_window'):
            return
        if self.rest_window.winfo_exists() and self.remaining > 0:
            self.rest_time_label.config(text=self._fmt(self.remaining))
            # 同时更新主窗口（如果可见）
            if self.start_btn.winfo_viewable():
                self.time_label.config(text=self._fmt(self.remaining))
            self.rest_window.after(1000, self._update_rest_window)

    def _exit_fullscreen(self, event=None):
        """ESC退出全屏，显示主窗口和立即开始按钮"""
        if hasattr(self, 'rest_window') and self.rest_window.winfo_exists():
            self.rest_window.destroy()
        self.root.deiconify()
        self.root.attributes('-topmost', True)
        # 显示休息倒计时和立即开始按钮（二次元蓝色）
        self.time_label.config(fg=self.COLOR_BLUE, text=self._fmt(self.remaining))
        self.start_btn.pack(pady=5)
        self.btn_frame.pack_forget()

    def _end_rest(self):
        """结束休息，开始25分钟倒计时（立即开始，不算闲置）"""
        if hasattr(self, 'rest_window') and self.rest_window.winfo_exists():
            self.rest_window.destroy()

        self.is_resting = False
        self.is_idle = False
        self.remaining = self.WORK_TIME
        self.idle_time = 0  # 重置闲置时间
        self.time_label.config(fg=self.COLOR_ACCENT, text=self._fmt(self.remaining))
        self.idle_hint.config(text="")  # 清除闲置提示
        self.start_btn.pack_forget()  # 隐藏立即开始按钮
        self.btn_frame.pack(pady=5)  # 显示正常按钮
        self.root.deiconify()
        self.root.attributes('-topmost', True)

        # 最小化窗口
        self.root.iconify()

    def _reset_work(self):
        """重置25分钟工作时间"""
        self.is_resting = False
        self.is_idle = False
        self.remaining = self.WORK_TIME
        self.time_label.config(fg=self.COLOR_ACCENT, text=self._fmt(self.remaining))
        self.idle_hint.config(text="")  # 清除闲置提示
        self.start_btn.pack_forget()  # 隐藏立即开始按钮
        self.btn_frame.pack(pady=5)  # 显示正常按钮

        # 如果休息窗口还在，关闭它
        if hasattr(self, 'rest_window') and self.rest_window.winfo_exists():
            self.rest_window.destroy()
            self.root.deiconify()

        # 最小化窗口
        self.root.iconify()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = RestTimer()
    app.run()
