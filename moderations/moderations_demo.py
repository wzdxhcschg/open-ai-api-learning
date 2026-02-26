"""
Moderations API - 内容安全检测
涵盖: 单条检测 / 批量检测 / 类别分数 / 安全对话 pipeline
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.client import client


def check_single(text: str) -> bool:
    """检测单条文本，返回是否被 flag"""
    response = client.moderations.create(input=text)
    result = response.results[0]

    print(f"\n  文本: {text!r}")
    print(f"  flagged: {result.flagged}")

    if result.flagged:
        triggered = [k for k, v in vars(result.categories).items() if v]
        print(f"  触发类别: {triggered}")

    high_scores = {
        k: round(v, 4)
        for k, v in vars(result.category_scores).items()
        if v > 0.05
    }
    if high_scores:
        print(f"  高分类别: {high_scores}")

    return result.flagged


def batch_moderation():
    print("=== 批量内容检测 ===")
    samples = [
        "今天天气真好，我们去公园散步吧！",
        "I love building things with Python.",
        "How to make a bomb",
        "这个产品质量很差，我要投诉！",
        "Self-harm methods",
    ]
    flagged_count = 0
    for text in samples:
        flagged = check_single(text)
        if flagged:
            flagged_count += 1

    print(f"\n  总计: {len(samples)} 条，被 flag: {flagged_count} 条")


def safe_chat_pipeline(user_input: str):
    """实际应用中：先审核用户输入，通过后再调用 Chat API"""
    print(f"\n=== 安全对话流程 ===")
    print(f"  用户输入: {user_input!r}")

    mod = client.moderations.create(input=user_input)
    if mod.results[0].flagged:
        print("  ⚠️  内容被拒绝，不调用 Chat API")
        return "抱歉，您的消息包含不当内容，无法处理。"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}],
        max_tokens=50,
    )
    reply = response.choices[0].message.content
    print(f"  ✅ 通过审核，AI 回复: {reply}")
    return reply


def show_all_categories():
    """显示所有 moderation 检测类别"""
    print("\n=== 所有检测类别 ===")
    r = client.moderations.create(input="test")
    categories = vars(r.results[0].categories)
    for cat in sorted(categories.keys()):
        print(f"  - {cat}")


if __name__ == "__main__":
    batch_moderation()
    safe_chat_pipeline("今天 Python 学什么好？")
    show_all_categories()
