"""
Chat Completions - Structured Output
涵盖: JSON mode / JSON Schema 精确控制输出结构
"""
import json
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.client import client


def json_mode():
    print("=== JSON Mode ===")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你只能输出合法的 JSON，不要输出其他任何内容"},
            {"role": "user", "content": "给我3个热门编程语言，每个包含 name、year_created、use_case 字段"},
        ],
        response_format={"type": "json_object"},
    )
    data = json.loads(response.choices[0].message.content)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def json_schema_mode():
    """使用 json_schema response_format 精确控制输出结构（gpt-4o 及以上支持）"""
    print("\n=== JSON Schema Mode ===")
    schema = {
        "type": "object",
        "properties": {
            "languages": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "year": {"type": "integer"},
                        "paradigm": {"type": "string"},
                    },
                    "required": ["name", "year", "paradigm"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["languages"],
        "additionalProperties": False,
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "列出5种编程语言"}],
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "languages_response", "strict": True, "schema": schema},
        },
    )
    data = json.loads(response.choices[0].message.content)
    for lang in data["languages"]:
        print(f"  {lang['name']} ({lang['year']}) - {lang['paradigm']}")


if __name__ == "__main__":
    json_mode()
    json_schema_mode()
