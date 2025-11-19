#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WhisperX 运行器模块

该模块提供了对 WhisperX 工具的封装，用于将音频文件转换为文字并生成字幕文件。
WhisperX 是对 OpenAI Whisper 的改进版本，具有更快的速度和更好的准确性。
"""

import os
import subprocess
import uuid


class WhisperXRunner:
    """
    WhisperX 运行器类
    
    负责调用外部的 whisperx 命令行工具来处理音频文件并生成字幕。
    """

    def __init__(self):
        """
        初始化 WhisperX 运行器
        """
        pass

    def generate_subtitles(self, audio_path: str, output_dir: str):
        """
        调用 whisperx 生成英文字幕
        
        Args:
            audio_path (str): 输入音频文件的路径
            output_dir (str): 输出字幕文件的目录
            
        Returns:
            str: 生成的字幕文件路径
            
        Raises:
            RuntimeError: 当 whisperx 执行失败时抛出异常
        """
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        # 根据音频文件名构建输出字幕文件名
        base = os.path.splitext(os.path.basename(audio_path))[0]
        out_srt = os.path.join(output_dir, f"{base}.en.srt")

        print(f"[WhisperX] 开始生成字幕: {audio_path}")

        """
        whisperx 最基本命令：
        whisperx input.mp3 --model large-v3 --output_dir output --align_model WAV2VEC2_ASR_LARGE_960H
        """

        # 构建 whisperx 命令行参数
        cmd = [
            "whisperx",
            audio_path,
            "--model", "large-v3",
            "--output_dir", output_dir,
            "--output_format", "srt"
        ]

        # 执行命令并捕获输出
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )

        # 检查执行结果
        if result.returncode != 0:
            print("[WhisperX 错误]\n", result.stderr)
            raise RuntimeError("WhisperX 执行失败！")

        print("[WhisperX] 字幕生成完成")
        return out_srt