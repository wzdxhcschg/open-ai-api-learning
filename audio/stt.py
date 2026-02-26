"""
Audio - Speech-to-Text (Whisper)
涵盖: 基础转录 / 指定语言 / 时间戳 / prompt 提示词 / 翻译成英文
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.client import client

# 测试时请提供音频文件路径
AUDIO_FILE = "your_audio.mp3"


def transcribe_basic(audio_path: str):
    print("=== 基础转录 ===")
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="text",
        )
    print("转录结果:", result)


def transcribe_with_language(audio_path: str, language: str = "zh"):
    print(f"\n=== 指定语言转录 (language={language}) ===")
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language=language,
            response_format="text",
        )
    print("转录结果:", result)


def transcribe_with_timestamps(audio_path: str):
    print("\n=== 带时间戳的转录 ===")
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            timestamp_granularities=["segment", "word"],
        )
    print(f"  语言: {result.language}  时长: {result.duration:.1f}s")
    print("  Segments:")
    for seg in result.segments[:5]:
        print(f"    [{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}")


def transcribe_with_prompt(audio_path: str):
    """prompt 可以提示专有名词拼写，提升准确率"""
    print("\n=== 带 prompt 的转录 ===")
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            prompt="这段录音讨论 OpenAI、GPT-4、ChatGPT 等 AI 技术",
            response_format="text",
        )
    print("转录结果:", result)


def translate_to_english(audio_path: str):
    """将任意语言音频翻译成英文"""
    print("\n=== 翻译成英文 ===")
    with open(audio_path, "rb") as f:
        result = client.audio.translations.create(
            model="whisper-1",
            file=f,
        )
    print("翻译结果:", result.text)


if __name__ == "__main__":
    if not os.path.exists(AUDIO_FILE):
        print(f"请提供音频文件，修改 AUDIO_FILE 变量（当前: {AUDIO_FILE!r}）")
        print("支持格式: mp3, mp4, mpeg, mpga, m4a, wav, webm")
    else:
        transcribe_basic(AUDIO_FILE)
        transcribe_with_language(AUDIO_FILE, "zh")
        transcribe_with_timestamps(AUDIO_FILE)
        translate_to_english(AUDIO_FILE)
