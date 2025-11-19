#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件操作工具模块

提供常用的文件和目录操作功能，例如确保目录存在等。
"""

import os


def ensure_dir(path: str):
    """
    确保指定路径的目录存在，如果不存在则创建
    
    Args:
        path (str): 需要确保存在的目录路径
    """
    if not os.path.exists(path):
        os.makedirs(path)