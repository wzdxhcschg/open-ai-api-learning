"""
Audio - Text-to-Speech (TTS)
涵盖: 基础生成 / 对比声音 / HD vs 标准 / 格式控制 / 语速
模型: tts-1 (速度快) / tts-1-hd (质量更高)
声音: alloy echo fable onyx nova shimmer
"""
import sys, os
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.client import client

OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def basic_tts():
    print("=== TTS 基础 ===")
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input="Hello! 这是一段由 OpenAI TTS 生成的语音示例。",
    )
    out = OUTPUT_DIR / "tts_basic.mp3"
    response.stream_to_file(out)
    print(f"  已保存: {out}")


def compare_voices():
    print("\n=== 对比不同声音 ===")
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    text = "The quick brown fox jumps over the lazy dog."
    for voice in voices:
        r = client.audio.speech.create(model="tts-1", voice=voice, input=text)
        out = OUTPUT_DIR / f"tts_voice_{voice}.mp3"
        r.stream_to_file(out)
        print(f"  {voice} -> {out.name}")


def hd_vs_standard():
    print("\n=== tts-1 vs tts-1-hd 质量对比 ===")
    text = "Artificial intelligence is transforming every industry."
    for model in ["tts-1", "tts-1-hd"]:
        r = client.audio.speech.create(model=model, voice="nova", input=text)
        out = OUTPUT_DIR / f"tts_{model.replace('-', '_')}.mp3"
        r.stream_to_file(out)
        print(f"  {model} -> {out.name}")


def different_formats():
    print("\n=== 不同音频格式 ===")
    formats = ["mp3", "opus", "aac", "flac"]
    for fmt in formats:
        r = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input="Testing audio formats.",
            response_format=fmt,
        )
        out = OUTPUT_DIR / f"tts_format.{fmt}"
        r.stream_to_file(out)
        size = out.stat().st_size
        print(f"  {fmt}: {size:,} bytes -> {out.name}")


def speed_control():
    print("\n=== 语速控制 (speed 参数) ===")
    text = "This is a test of speech speed control."
    for speed in [0.75, 1.0, 1.25]:
        r = client.audio.speech.create(model="tts-1", voice="nova", input=text, speed=speed)
        out = OUTPUT_DIR / f"tts_speed_{str(speed).replace('.', '_')}.mp3"
        r.stream_to_file(out)
        print(f"  speed={speed} -> {out.name}")


if __name__ == "__main__":
    basic_tts()
    compare_voices()
    hd_vs_standard()
    different_formats()
    speed_control()
