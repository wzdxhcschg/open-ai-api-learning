"""
Files API
涵盖: 上传 / 列举 / 获取信息 / 下载内容 / 删除
主要用于: Fine-tuning 数据集 / Assistants 知识库
"""
import json
import sys, os
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.client import client

OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def create_finetune_jsonl(path: Path, n: int = 5):
    """生成符合 OpenAI fine-tuning 格式的 JSONL 数据集"""
    qa_pairs = [
        ("1加1等于几？", "2"),
        ("Python 的创始人是谁？", "Guido van Rossum"),
        ("地球绕太阳转一圈需要多久？", "约365.25天"),
        ("HTTP 的全称是什么？", "HyperText Transfer Protocol"),
        ("DNA 的双螺旋结构由谁发现？", "Watson 和 Crick（1953年）"),
    ]
    with open(path, "w", encoding="utf-8") as f:
        for q, a in qa_pairs[:n]:
            record = {"messages": [
                {"role": "system", "content": "你是一个简洁准确的知识助手"},
                {"role": "user", "content": q},
                {"role": "assistant", "content": a},
            ]}
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"  已生成 {n} 条训练数据: {path.name}")
    return path


def upload_file(file_path: Path, purpose: str = "fine-tune"):
    print(f"\n=== 上传文件 (purpose={purpose}) ===")
    with open(file_path, "rb") as f:
        uploaded = client.files.upload(file=(file_path.name, f, "application/json"))
    print(f"  file_id: {uploaded.id}")
    print(f"  filename: {uploaded.filename}")
    print(f"  size: {uploaded.bytes} bytes")
    print(f"  status: {uploaded.status}")
    return uploaded.id


def list_files(purpose: str | None = None):
    print("\n=== 列举文件 ===")
    kwargs = {}
    if purpose:
        kwargs["purpose"] = purpose
    files = client.files.list(**kwargs)
    if not files.data:
        print("  暂无文件")
        return
    for f in files.data[:10]:
        print(f"  {f.id}  {f.filename:30s}  {f.bytes:>8} bytes  {f.purpose}")


def get_file_info(file_id: str):
    print(f"\n=== 获取文件信息: {file_id} ===")
    info = client.files.retrieve(file_id)
    print(f"  id: {info.id}")
    print(f"  filename: {info.filename}")
    print(f"  status: {info.status}")
    print(f"  created_at: {info.created_at}")


def download_file_content(file_id: str):
    print(f"\n=== 下载文件内容: {file_id} ===")
    content = client.files.content(file_id)
    text = content.read().decode("utf-8")
    for i, line in enumerate(text.strip().split("\n")[:3], 1):
        print(f"  Line {i}: {line[:80]}")


def delete_file(file_id: str):
    print(f"\n=== 删除文件: {file_id} ===")
    result = client.files.delete(file_id)
    print(f"  deleted: {result.deleted}  id: {result.id}")


def full_lifecycle():
    # 1. 创建示例数据
    sample_path = OUTPUT_DIR / "sample_finetune.jsonl"
    create_finetune_jsonl(sample_path)

    # 2. 上传
    file_id = upload_file(sample_path)

    # 3. 列举
    list_files()

    # 4. 查询
    get_file_info(file_id)

    # 5. 删除
    delete_file(file_id)

    print("\n✅ Files API 完整生命周期测试完成")


if __name__ == "__main__":
    full_lifecycle()
