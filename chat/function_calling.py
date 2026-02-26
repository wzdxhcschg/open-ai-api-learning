"""
Chat Completions - Function Calling / Tool Use
涵盖: 单工具 / 多工具并行 / tool_choice 控制
"""
import json
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.client import client


# ── 模拟工具函数 ───────────────────────────────────────────────────────────────

def get_weather(city: str) -> dict:
    mock = {"Beijing": "晴天 22°C", "Shanghai": "多云 18°C", "Guangzhou": "雷阵雨 30°C"}
    return {"city": city, "weather": mock.get(city, "暂无数据")}


def calculator(expression: str) -> dict:
    try:
        result = eval(expression, {"__builtins__": {}})  # 生产环境请用安全解析器
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}


# ── Tool 定义 ──────────────────────────────────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称（英文），如 Beijing"}
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "合法的数学表达式，如 '2 ** 10'"}
                },
                "required": ["expression"],
            },
        },
    },
]

TOOL_MAP = {"get_weather": get_weather, "calculator": calculator}


def run_tool_calls(tool_calls):
    """执行所有工具调用，返回 tool result messages"""
    results = []
    for tc in tool_calls:
        args = json.loads(tc.function.arguments)
        result = TOOL_MAP[tc.function.name](**args)
        results.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "content": json.dumps(result, ensure_ascii=False),
        })
    return results


def single_tool_demo():
    print("=== 单工具调用 ===")
    messages = [{"role": "user", "content": "北京今天天气怎么样？"}]
    r = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=TOOLS, tool_choice="auto")
    msg = r.choices[0].message
    print("  工具调用:", [(tc.function.name, tc.function.arguments) for tc in msg.tool_calls])

    messages += [msg, *run_tool_calls(msg.tool_calls)]
    final = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=TOOLS)
    print("  最终回答:", final.choices[0].message.content)


def parallel_tool_demo():
    print("\n=== 并行工具调用 ===")
    messages = [{"role": "user", "content": "上海和广州天气怎样？顺便帮我算 2 的 16 次方"}]
    r = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=TOOLS)
    msg = r.choices[0].message
    print(f"  触发了 {len(msg.tool_calls)} 个工具调用")

    messages += [msg, *run_tool_calls(msg.tool_calls)]
    final = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=TOOLS)
    print("  最终回答:", final.choices[0].message.content)


def force_tool_demo():
    print("\n=== 强制指定工具 (tool_choice) ===")
    messages = [{"role": "user", "content": "你好"}]
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOLS,
        tool_choice={"type": "function", "function": {"name": "get_weather"}},
    )
    msg = r.choices[0].message
    print("  强制调用:", msg.tool_calls[0].function.name, msg.tool_calls[0].function.arguments)


if __name__ == "__main__":
    single_tool_demo()
    parallel_tool_demo()
    force_tool_demo()
