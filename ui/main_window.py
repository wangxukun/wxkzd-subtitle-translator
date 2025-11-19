import customtkinter as ctk
from tkinter import filedialog
import threading

from whisperx_module.whisperx_runner import WhisperXRunner


class SubtitleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("远路字幕翻译工具 - wxkzd subtitle translator")
        self.geometry("1100x650")

        self.audio_file_path = None
        self.whisperx = WhisperXRunner()

        # ====== 布局 ======
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ====== 左侧操作栏 ======
        control = ctk.CTkFrame(self, corner_radius=10)
        control.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

        ctk.CTkLabel(control, text="操作面板", font=("微软雅黑", 20)).pack(pady=20)

        # ---- 选择音频 ----
        ctk.CTkButton(
            control, text="选择英文音频文件",
            command=self.select_audio_file
        ).pack(pady=10)

        self.audio_label = ctk.CTkLabel(control, text="未选择音频", wraplength=180)
        self.audio_label.pack(pady=5)

        # ---- 生成英文字幕 ----
        ctk.CTkButton(
            control, text="生成英文字幕（WhisperX）",
            command=self.run_whisperx_thread
        ).pack(pady=20)

        # ====== 日志输出 ======
        self.log_box = ctk.CTkTextbox(self, font=("微软雅黑", 14))
        self.log_box.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.log("UI 初始化完成！")

    # ========== 日志 ==========
    def log(self, t: str):
        self.log_box.insert("end", t + "\n")
        self.log_box.see("end")

    # ========== 选择音频文件 ==========
    def select_audio_file(self):
        filetypes = [("音频文件", "*.mp3 *.wav *.m4a *.flac *.aac"), ("所有文件", "*.*")]
        fp = filedialog.askopenfilename(title="选择音频文件", filetypes=filetypes)

        if fp:
            self.audio_file_path = fp
            self.audio_label.configure(text=fp)
            self.log(f"已选择音频：\n{fp}")
        else:
            self.log("未选择音频文件")

    # ========== 后台线程：避免卡死界面 ==========
    def run_whisperx_thread(self):
        if not self.audio_file_path:
            self.log("请先选择音频！")
            return

        t = threading.Thread(target=self.run_whisperx, daemon=True)
        t.start()

    # ========== 运行 whisperx ==========
    def run_whisperx(self):
        audio = self.audio_file_path
        output_dir = "output"

        self.log("[WhisperX] 开始生成英文字幕...")
        self.log("音频文件：" + audio)

        try:
            srt_path = self.whisperx.generate_subtitles(audio, output_dir)
            self.log(f"[WhisperX] 生成完成！字幕文件：\n{srt_path}")

        except Exception as e:
            self.log("[错误] WhisperX 运行失败！")
            self.log(str(e))


def start_app():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = SubtitleApp()
    app.mainloop()
