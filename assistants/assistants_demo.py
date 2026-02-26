"""
Assistants API v2
涵盖: 基础问答 / Code Interpreter / 多轮对话 / 管理 Assistants
"""
import time
import sys, os
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.client import client

OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


# ── 工具函数 ───────────────────────────────────────────────────────────────────

def wait_for_run(thread_id: str, run_id: str, timeout: int = 120):
    """轮询等待 run 完成"""
    start = time.time()
    while time.time() - start < timeout:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status in ("completed", "failed", "cancelled", "expired", "requires_action"):
            return run
        print(f"    [{run.status}] 等待中...")
        time.sleep(3)
    raise TimeoutError("Run 超时")


def get_last_message(thread_id: str) -> str:
    messages = client.beta.threads.messages.list(thread_id=thread_id, order="desc", limit=1)
    msg = messages.data[0]
    return "\n".join(block.text.value for block in msg.content if block.type == "text")


def print_all_messages(thread_id: str):
    messages = client.beta.threads.messages.list(thread_id=thread_id, order="asc")
    for msg in messages.data:
        role = "🧑 User" if msg.role == "user" else "🤖 Assistant"
        content = "\n".join(b.text.value for b in msg.content if b.type == "text")
        print(f"\n  {role}:\n    {content[:300]}")


# ── Demo 1: 基础问答 ──────────────────────────────────────────────────────────

def basic_assistant():
    print("=== Demo 1: 基础问答 Assistant ===")
    assistant = client.beta.assistants.create(
        name="Python Tutor",
        instructions="你是一个 Python 编程老师，用中文简洁地回答问题，多用代码示例",
        model="gpt-4o-mini",
    )
    thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="列表推导式和 map() 哪个更 Pythonic？",
    )
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
    run = wait_for_run(thread.id, run.id)

    print(f"  Status: {run.status}")
    print_all_messages(thread.id)

    client.beta.assistants.delete(assistant.id)
    print("\n  ✅ assistant 已删除")


# ── Demo 2: Code Interpreter ──────────────────────────────────────────────────

def code_interpreter_assistant():
    print("\n=== Demo 2: Code Interpreter ===")
    assistant = client.beta.assistants.create(
        name="Math Solver",
        instructions="你是一个数学助手，用代码解决问题，用中文解释结果",
        model="gpt-4o-mini",
        tools=[{"type": "code_interpreter"}],
    )
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="计算 1 到 100 之间所有质数的和，并列出这些质数",
    )
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
    run = wait_for_run(thread.id, run.id)

    messages = client.beta.threads.messages.list(thread_id=thread.id, order="asc")
    for msg in messages.data:
        if msg.role == "assistant":
            for block in msg.content:
                if block.type == "text":
                    print(f"\n  Assistant: {block.text.value[:400]}")

    client.beta.assistants.delete(assistant.id)


# ── Demo 3: 多轮对话 ───────────────────────────────────────────────────────────

def multi_turn_conversation():
    print("\n=== Demo 3: 多轮对话 ===")
    assistant = client.beta.assistants.create(
        name="Chat Assistant",
        instructions="你是一个友善的聊天助手，记住对话上下文",
        model="gpt-4o-mini",
    )
    thread = client.beta.threads.create()

    questions = [
        "我叫小明，我是一个 Python 初学者",
        "你还记得我叫什么名字吗？",
        "给我推荐一个适合初学者的 Python 项目",
    ]

    for q in questions:
        client.beta.threads.messages.create(thread_id=thread.id, role="user", content=q)
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
        wait_for_run(thread.id, run.id)
        reply = get_last_message(thread.id)
        print(f"\n  👤 {q}")
        print(f"  🤖 {reply[:200]}")

    client.beta.assistants.delete(assistant.id)


# ── Demo 4: 管理 Assistants ───────────────────────────────────────────────────

def manage_assistants():
    print("\n=== Demo 4: 管理 Assistants ===")
    assistants = client.beta.assistants.list(limit=5, order="desc")
    print(f"  当前 assistants 数量（最多显示5个）: {len(assistants.data)}")
    for a in assistants.data:
        print(f"    {a.id}  {a.name or '(unnamed)':20s}  model={a.model}")


if __name__ == "__main__":
    manage_assistants()
    basic_assistant()
    code_interpreter_assistant()
    multi_turn_conversation()
