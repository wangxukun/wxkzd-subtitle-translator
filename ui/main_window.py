import customtkinter as ctk
from tkinter import filedialog
import threading

from whisperx_module.whisperx_runner import WhisperXRunner


class SubtitleApp(ctk.CTk):
    """
    字幕翻译应用程序主窗口类
    继承自CTk，提供图形界面用于选择音频文件并生成字幕
    """
    def __init__(self):
        """初始化应用程序窗口和组件"""
        super().__init__()

        # 设置窗口标题和尺寸
        self.title("远路字幕翻译工具 - wxkzd subtitle translator")
        self.geometry("1100x650")

        # 存储音频文件路径
        self.audio_file_path = None
        # 初始化WhisperX运行器实例
        self.whisperx = WhisperXRunner()

        # ====== 布局设置 ======
        # 配置网格列权重，使右侧区域可扩展
        self.columnconfigure(0, weight=0)  # 左侧控制面板不扩展
        self.columnconfigure(1, weight=1)  # 右侧日志区域可扩展
        # 配置网格行权重，使内容垂直扩展
        self.rowconfigure(0, weight=1)

        # ====== 左侧操作栏 ======
        # 创建左侧控制面板框架
        control = ctk.CTkFrame(self, corner_radius=10)
        control.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

        # 添加操作面板标题标签
        ctk.CTkLabel(control, text="操作面板", font=("微软雅黑", 20)).pack(pady=20)

        # ---- 选择音频按钮 ----
        # 创建选择音频文件按钮，绑定select_audio_file方法
        ctk.CTkButton(
            control, text="选择英文音频文件",
            command=self.select_audio_file
        ).pack(pady=10)

        # 显示当前选择的音频文件路径标签
        self.audio_label = ctk.CTkLabel(control, text="未选择音频", wraplength=180)
        self.audio_label.pack(pady=5)

        # ---- 生成英文字幕按钮 ----
        # 创建生成字幕按钮，绑定run_whisperx_thread方法
        ctk.CTkButton(
            control, text="生成英文字幕（WhisperX）",
            command=self.run_whisperx_thread
        ).pack(pady=20)

        # ====== 日志输出区域 ======
        # 创建文本框用于显示操作日志
        self.log_box = ctk.CTkTextbox(self, font=("微软雅黑", 14))
        self.log_box.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # 记录初始化完成日志
        self.log("UI 初始化完成！")

    # ========== 日志方法 ==========
    def log(self, t: str):
        """
        在日志框中添加一条日志消息
        
        Args:
            t (str): 要记录的日志文本
        """
        self.log_box.insert("end", t + "\n")
        self.log_box.see("end")  # 自动滚动到底部显示最新日志

    # ========== 选择音频文件方法 ==========
    def select_audio_file(self):
        """打开文件选择对话框，让用户选择音频文件"""
        # 定义支持的音频文件类型
        filetypes = [("音频文件", "*.mp3 *.wav *.m4a *.flac *.aac"), ("所有文件", "*.*")]
        # 弹出文件选择对话框
        fp = filedialog.askopenfilename(title="选择音频文件", filetypes=filetypes)

        if fp:
            # 如果选择了文件，则更新音频路径和显示标签
            self.audio_file_path = fp
            self.audio_label.configure(text=fp)
            self.log(f"已选择音频：\n{fp}")
        else:
            # 如果未选择文件，记录相应日志
            self.log("未选择音频文件")

    # ========== 后台线程运行方法 ==========
    def run_whisperx_thread(self):
        """
        在后台线程中运行WhisperX，避免界面卡死
        """
        if not self.audio_file_path:
            # 如果没有选择音频文件，提示用户
            self.log("请先选择音频！")
            return

        # 创建并启动后台线程执行WhisperX
        t = threading.Thread(target=self.run_whisperx, daemon=True)
        t.start()

    # ========== 运行 whisperx 方法 ==========
    def run_whisperx(self):
        """
        实际调用WhisperX生成字幕的方法
        """
        # 获取音频文件路径和输出目录
        audio = self.audio_file_path
        output_dir = "output"

        # 记录开始生成字幕的日志
        self.log("[WhisperX] 开始生成英文字幕...")
        self.log("音频文件：" + audio)

        try:
            # 调用WhisperX生成字幕
            srt_path = self.whisperx.generate_subtitles(audio, output_dir)
            # 记录生成成功的日志
            self.log(f"[WhisperX] 生成完成！字幕文件：\n{srt_path}")

        except Exception as e:
            # 捕获异常并记录错误日志
            self.log("[错误] WhisperX 运行失败！")
            self.log(str(e))


def start_app():
    """
    启动应用程序的函数
    设置外观模式和主题颜色，创建并运行应用主窗口
    """
    # 设置暗色外观模式和蓝色主题
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    # 创建应用实例并启动主循环
    app = SubtitleApp()
    app.mainloop()