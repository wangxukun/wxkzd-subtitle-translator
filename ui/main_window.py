import customtkinter as ctk

def start_app():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("远路字幕翻译工具 - wxkzd subtitle translator")
    app.geometry("900x600")

    title = ctk.CTkLabel(app, text="字幕生成与翻译工具", font=("微软雅黑", 28))
    title.pack(pady=20)

    # TODO: 后面会加按钮：选择音频、生成英文字幕、翻译字幕
    placeholder = ctk.CTkLabel(app, text="UI 初始化成功！（等待添加功能）")
    placeholder.pack(pady=20)

    app.mainloop()
