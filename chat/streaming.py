"""
Chat Completions - Streaming 流式输出
涵盖: 基础流式 / 流式 + token 用量统计
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.client import client


def stream_chat():
    print("=== Streaming ===")
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "写一首关于 Python 的五行短诗"}],
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
    print()


def stream_with_usage():
    """stream=True 时同时获取 token 用量（需传 stream_options）"""
    print("\n=== Streaming + Usage ===")
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello!"}],
        stream=True,
        stream_options={"include_usage": True},
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
        if chunk.usage:
            print(f"\n  tokens: prompt={chunk.usage.prompt_tokens} completion={chunk.usage.completion_tokens}")
    print()


if __name__ == "__main__":
    stream_chat()
    stream_with_usage()
