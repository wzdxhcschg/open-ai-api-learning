"""
Chat Completions - 基础用法
涵盖: 单轮对话 / 多轮对话 / system prompt / temperature / max_tokens
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.client import client


def single_turn():
    print("=== 单轮对话 ===")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "用一句话解释什么是量子纠缠"}],
        max_tokens=100,
    )
    print(response.choices[0].message.content)


def multi_turn():
    print("\n=== 多轮对话 ===")
    messages = [
        {"role": "system", "content": "你是一位幽默的 Python 老师"},
        {"role": "user", "content": "什么是装饰器？"},
    ]
    r1 = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    assistant_msg = r1.choices[0].message.content
    print("Assistant:", assistant_msg)

    messages.append({"role": "assistant", "content": assistant_msg})
    messages.append({"role": "user", "content": "能给个例子吗？"})
    r2 = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    print("Assistant:", r2.choices[0].message.content)


def temperature_demo():
    print("\n=== Temperature 对比 ===")
    prompt = "给我一个创意公司名"
    for temp in [0.0, 1.0, 2.0]:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            max_tokens=20,
        )
        print(f"  temp={temp}: {r.choices[0].message.content.strip()}")


if __name__ == "__main__":
    single_turn()
    multi_turn()
    temperature_demo()
