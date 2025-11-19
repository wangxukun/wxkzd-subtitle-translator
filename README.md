# wxkzd 字幕翻译工具

这是一个基于 WhisperX 和 vLLM 的字幕生成与翻译工具，可以自动将音频文件转换为文字并翻译成中文。

## 功能特点

- 使用 WhisperX 将音频文件转换为英文字幕
- 计划集成 vLLM + Qwen 模型进行中英翻译
- 图形用户界面，易于操作

## 技术架构

- **UI 层**: CustomTkinter (现代化的 Tkinter 封装)
- **音频转录**: WhisperX (基于 Whisper 的优化版本)
- **翻译引擎**: 计划集成 vLLM + Qwen 大语言模型
- **字幕处理**: pysrt 库

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行主程序:
   ```bash
   python main.py
   ```

2. 在图形界面中选择音频文件
3. 点击按钮生成英文字幕
4. （待完善）翻译为中文字幕

## 项目结构

```
wxkzd-subtitle-translator/
├── main.py                 # 程序入口
├── requirements.txt        # 依赖列表
├── ui/                     # 用户界面模块
│   └── main_window.py      # 主窗口实现
├── whisperx_module/        # 音频转录模块
│   └── whisperx_runner.py  # WhisperX 调用封装
├── translator_module/      # 翻译模块
│   └── vllm_translator.py  # vLLM 翻译封装
└── utils/                  # 工具函数
    ├── file_utils.py       # 文件操作工具
    └── subtitle_utils.py   # 字幕处理工具
```

## 开发计划

- [x] 基础UI界面
- [x] 音频转录功能（WhisperX）
- [ ] 字幕翻译功能（vLLM + Qwen）
- [ ] 完整的中英文对照字幕生成
- [ ] 更多音频格式支持