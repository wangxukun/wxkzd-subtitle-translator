import customtkinter as ctk
from tkinter import filedialog
import threading
from PIL import Image
import os

from numpy.ma.core import left_shift
from pygments.lexer import default
from whisperx import align

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
        self.title("远路字幕 - wxkzd subtitle")
        self.wm_iconbitmap("res/img/icon.ico")
        self.geometry("1100x650")

        # 设置窗口最小尺寸
        self.minsize(500, 250)

        # 存储音频文件路径
        self.audio_file_path = None
        # 初始化WhisperX运行器实例
        self.whisperx = WhisperXRunner()

        # ====== 布局设置 ======
        # 配置网格列权重，使右侧区域可扩展
        self.columnconfigure(0, weight=0)  # 左侧控制面板不扩展
        self.columnconfigure(1, weight=1)  # 右侧日志区域可扩展
        # 配置网格行权重，使内容垂直扩展
        self.rowconfigure(0, weight=0)  # 控制按钮区域
        self.rowconfigure(1, weight=1)  # 主要内容区域可扩展

        # ====== 左侧操作栏 ======
        # 创建左侧控制面板框架
        self.control = ctk.CTkScrollableFrame(master = self, width=230, corner_radius=0)
        self.control.grid(row=0, column=0, sticky="nsew", rowspan=2)
        self.control.columnconfigure(0, weight=1)  # 使内容可扩展
        
        # ====== Logo 和标题区域 ======
        # 加载Logo图片
        logo_path = os.path.join(os.path.dirname(__file__), "..", "res", "img", "icon-light.png")
        if os.path.exists(logo_path):
            logo_image = ctk.CTkImage(light_image=Image.open(logo_path),
                                      dark_image=Image.open(logo_path),
                                      size=(40, 40))
            # 创建Logo和标题框架
            logo_frame = ctk.CTkFrame(self.control, fg_color="transparent")
            logo_frame.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
            logo_frame.columnconfigure(1, weight=1)  # 让标题可扩展
            
            # 添加Logo标签
            logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="")
            logo_label.grid(row=0, column=0, padx=(0, 10))
            
            # 添加标题
            title_label = ctk.CTkLabel(logo_frame, text="远路字幕", font=("微软雅黑", 20, "bold"))
            title_label.grid(row=0, column=1, sticky="w")

        # 转录语言框架
        self.frm_transcription_language= ctk.CTkFrame(self.control, fg_color="transparent", border_width=2, border_color="gray")
        self.frm_transcription_language.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.frm_transcription_language.columnconfigure(0, weight=1)  # 使按钮可扩展

        ## '转录语言'选项菜单
        self.lbl_transcription_language = ctk.CTkLabel(
            master=self.frm_transcription_language,
            text="转录语言",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.lbl_transcription_language.grid(row=0, column=0, padx=0, pady=(10, 0))
        ## '选择源语言'选项菜单
        self.lbl_original_language = ctk.CTkLabel(
            master=self.frm_transcription_language,
            text="源语言",
            font=ctk.CTkFont(size=10, weight="bold"),
        )
        self.lbl_original_language.grid(row=1, column=0, padx=5, pady=(10, 10), sticky="w")

        self.omn_transcription_language = ctk.CTkOptionMenu(
            master=self.frm_transcription_language,
            values=["English", "简体中文"],
        )
        self.omn_transcription_language.grid(row=2, column=0, padx=30, pady=(0, 20))

        # ---- 生成英文字幕按钮 ----
        # 创建生成字幕按钮，绑定run_whisperx_thread方法
        ctk.CTkButton(
            self.frm_transcription_language, text="生成英文字幕", fg_color="green",
            command=self.run_whisperx_thread
        ).grid(row=3, column=0, padx=30,pady=20, sticky="ew")

        # WhisperX 选项框架
        self.frm_whisperx_options= ctk.CTkFrame(self.control, fg_color="transparent", border_width=2, border_color="gray")
        self.frm_whisperx_options.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.frm_whisperx_options.columnconfigure(0, weight=1)  # 使按钮可扩展
        self.frm_whisperx_options.columnconfigure(1, weight=1)  # 使按钮可扩展
        
        ## 'WhisperX 选项'标签
        self.lbl_whisperx_options = ctk.CTkLabel(
            master=self.frm_whisperx_options,
            text="WhisperX 选项",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.lbl_whisperx_options.grid(row=0, column=0, columnspan=2, padx=0, pady=(10, 0))

        ## '字幕生成类型'标签
        self.lbl_subtitle_type= ctk.CTkLabel(
            master=self.frm_whisperx_options,
            text="字幕生成类型",
            font=ctk.CTkFont(size=10, weight="bold"),
        )
        self.lbl_subtitle_type.grid(row=1, column=0, columnspan=2, padx=5, pady=(10, 0), sticky="w")

        ## 添加CTkCheckBox【输出字幕文件类型】
        self.chk_output_file_type_srt = ctk.CTkCheckBox(self.frm_whisperx_options, text=".srt", onvalue="srt", offvalue="")
        self.chk_output_file_type_srt.grid(row=2, column=0, padx=(30, 10), pady=(5, 5), sticky="w")
        self.chk_output_file_type_txt = ctk.CTkCheckBox(self.frm_whisperx_options, text=".vtt", onvalue="vtt", offvalue="")
        self.chk_output_file_type_txt.grid(row=2, column=1, padx=(10, 20), pady=(5, 5), sticky="w")
        self.chk_output_file_type_srt = ctk.CTkCheckBox(self.frm_whisperx_options, text=".json", onvalue="json", offvalue="")
        self.chk_output_file_type_srt.grid(row=3, column=0, padx=(30, 10), pady=(5, 20), sticky="w")
        self.chk_output_file_type_txt = ctk.CTkCheckBox(self.frm_whisperx_options, text=".txt", onvalue="txt", offvalue="")
        self.chk_output_file_type_txt.grid(row=3, column=1, padx=(10, 20), pady=(5, 20), sticky="w")

        ## '区分说话人'标签
        self.lbl_subtitle_type= ctk.CTkLabel(
            master=self.frm_whisperx_options,
            text="区分说话人",
            font=ctk.CTkFont(size=10, weight="bold"),
        )
        self.lbl_subtitle_type.grid(row=4, column=0, columnspan=2, padx=5, pady=(10, 0), sticky="w")
        ## 添加CTkCheckBox【区分说话人】
        self.chk_speaker= ctk.CTkCheckBox(self.frm_whisperx_options, text="分辨", onvalue="speaker", offvalue="")
        self.chk_speaker.grid(row=5, column=0, columnspan=2, padx=(30, 10), pady=(5, 20), sticky="w")

        # 高级选项框架
        self.frm_advanced_options= ctk.CTkFrame(self.control, fg_color="transparent", border_width=2, border_color="gray")
        self.frm_advanced_options.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.frm_advanced_options.columnconfigure(0, weight=1)  # 使按钮可扩展
        ## '高级选项'选项菜单
        self.lbl_advanced_options = ctk.CTkLabel(
            master=self.frm_advanced_options,
            text="高级选项",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.lbl_advanced_options.grid(row=0, column=0, padx=0, pady=(10, 0),columnspan=2)
        ## '选择模型大小'标签
        self.lbl_model_size= ctk.CTkLabel(
            master=self.frm_advanced_options,
            text="模型大小",
            font=ctk.CTkFont(size=10, weight="bold"),
        )
        self.lbl_model_size.grid(row=1, column=0, columnspan=2, padx=5, pady=(10, 0), sticky="w")
        self.omn_model_size = ctk.CTkOptionMenu(
            master=self.frm_advanced_options,
            values=["large-v2", "large-v3"],
        )
        self.omn_model_size.grid(row=2, column=0, columnspan=2, padx=30, pady=(0, 10))

        ## '计算精度'标签
        self.lbl_compute_type = ctk.CTkLabel(
            master=self.frm_advanced_options,
            text="计算精度",
            font=ctk.CTkFont(size=10, weight="bold"),
        )
        self.lbl_compute_type.grid(row=3, column=0, columnspan=2, padx=5, pady=(10, 0), sticky="w")
        self.omn_compute_type = ctk.CTkOptionMenu(
            master=self.frm_advanced_options,
            values=["int8", "float16", "float32"],
        )
        self.omn_compute_type.set("float16")  # 设置默认值为float16
        self.omn_compute_type.grid(row=4, column=0, columnspan=2, padx=30, pady=(0, 20))

        ## '批处理大小'标签
        self.lab_batch_size = ctk.CTkLabel(
            master=self.frm_advanced_options,
            text="批处理大小",
            font=ctk.CTkFont(size=10, weight="bold"),
        )
        self.lab_batch_size.grid(row=5, column=0, padx=5, pady=(0, 20),sticky="w")
        self.entry_batch_size = ctk.CTkEntry(self.frm_advanced_options,width=70)
        self.entry_batch_size.grid(row=5, column=1, padx=30, pady=(0, 20), sticky="w")

        ## '外观模式'选项菜单
        self.lbl_appearance_mode = ctk.CTkLabel(
            master=self.control,
            text="外观模式",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.lbl_appearance_mode.grid(row=7, column=0, padx=0, pady=(10, 0))
        ## '选择外观模式'
        self.omn_appearance_mode = ctk.CTkOptionMenu(
            master=self.control,
            values=["System","Dark","Light"],
        )
        self.omn_appearance_mode.set("Dark")
        self.omn_appearance_mode.grid(row=8, column=0, padx=0, pady=(0, 20))

        # ====== 上方控制区域 ======
        # 创建上方控制区域框架
        top_control_frame = ctk.CTkFrame(self)
        top_control_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        top_control_frame.columnconfigure(0, weight=1)  # Input框可扩展
        top_control_frame.columnconfigure(1, weight=0)  # 按钮不扩展

        # 显示当前选择的音频文件路径输入框
        self.audio_entry = ctk.CTkEntry(top_control_frame, placeholder_text="请选择音频文件")
        self.audio_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        # ---- 选择音频按钮 ----
        # 创建选择音频文件按钮，绑定select_audio_file方法
        self.select_button = ctk.CTkButton(
            top_control_frame, text="选择音频文件",
            command=self.select_audio_file
        )
        self.select_button.grid(row=0, column=1)

        # ====== 日志输出区域 ======
        # 创建文本框用于显示操作日志
        self.log_box = ctk.CTkTextbox(self, font=("微软雅黑", 14))
        self.log_box.grid(row=1, column=1, sticky="nsew", padx=10, pady=(0, 10))

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
            self.audio_entry.delete(0, "end")
            self.audio_entry.insert(0, fp)
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
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    # 创建应用实例并启动主循环
    app = SubtitleApp()
    app.mainloop()