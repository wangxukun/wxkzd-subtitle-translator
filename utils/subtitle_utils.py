#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
字幕处理工具模块

提供加载和保存SRT字幕文件的功能。
"""


def load_srt(path):
    """
    从指定路径加载SRT字幕文件内容
    
    Args:
        path (str): SRT字幕文件的路径
        
    Returns:
        str: 字幕文件的内容
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_srt(path, content):
    """
    将字幕内容保存到指定路径的SRT文件中
    
    Args:
        path (str): 要保存的SRT文件路径
        content (str): 要保存的字幕内容
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)