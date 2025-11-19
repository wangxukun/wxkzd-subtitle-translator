#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
字幕翻译工具主入口文件

这个文件是整个应用程序的入口点，负责初始化并启动图形用户界面。
"""

# 导入UI模块中的启动函数
from ui.main_window import start_app

if __name__ == "__main__":
    # 当脚本直接运行时（而非作为模块导入时），启动应用程序
    start_app()