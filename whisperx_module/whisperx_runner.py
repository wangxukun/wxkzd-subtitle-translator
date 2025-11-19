import os
import subprocess
import uuid

class WhisperXRunner:
    def __init__(self):
        pass

    def generate_subtitles(self, audio_path: str, output_dir: str):
        """
        调用 whisperx 生成英文字幕
        """
        os.makedirs(output_dir, exist_ok=True)

        # 输出文件名
        base = os.path.splitext(os.path.basename(audio_path))[0]
        out_srt = os.path.join(output_dir, f"{base}.en.srt")

        print(f"[WhisperX] 开始生成字幕: {audio_path}")

        """
        whisperx 最基本命令：
        whisperx input.mp3 --model large-v3 --output_dir output --align_model WAV2VEC2_ASR_LARGE_960H
        """

        cmd = [
            "whisperx",
            audio_path,
            "--model", "large-v3",
            "--output_dir", output_dir,
            "--output_format", "srt"
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )

        if result.returncode != 0:
            print("[WhisperX 错误]\n", result.stderr)
            raise RuntimeError("WhisperX 执行失败！")

        print("[WhisperX] 字幕生成完成")
        return out_srt
