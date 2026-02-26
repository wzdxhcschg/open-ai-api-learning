"""
Embeddings API
涵盖: 单文本/批量嵌入 / 余弦相似度 / 语义搜索 / 降维 / token 用量
"""
import math
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.client import client

MODEL = "text-embedding-3-small"   # 也可用 text-embedding-3-large / text-embedding-ada-002


# ── 核心工具函数 ───────────────────────────────────────────────────────────────

def embed(texts: list[str], dimensions: int | None = None) -> list[list[float]]:
    kwargs = {"model": MODEL, "input": texts}
    if dimensions:
        kwargs["dimensions"] = dimensions
    response = client.embeddings.create(**kwargs)
    return [d.embedding for d in sorted(response.data, key=lambda x: x.index)]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x ** 2 for x in a))
    norm_b = math.sqrt(sum(x ** 2 for x in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


# ── Demo 函数 ──────────────────────────────────────────────────────────────────

def single_embed():
    print("=== 单文本嵌入 ===")
    vecs = embed(["Hello, world!"])
    print(f"  维度: {len(vecs[0])}")
    print(f"  前5个值: {vecs[0][:5]}")


def batch_embed():
    print("\n=== 批量嵌入 ===")
    texts = ["Python", "JavaScript", "机器学习", "猫咪", "量子力学"]
    vecs = embed(texts)
    print(f"  嵌入了 {len(vecs)} 个文本，每个维度: {len(vecs[0])}")


def similarity_demo():
    print("\n=== 语义相似度计算 ===")
    pairs = [
        ("我喜欢吃苹果", "苹果是我最爱的水果"),
        ("我喜欢吃苹果", "今天天气真好"),
        ("深度学习", "神经网络"),
        ("深度学习", "烹饪食谱"),
    ]
    all_texts = [t for pair in pairs for t in pair]
    vecs = embed(all_texts)
    for i, (a, b) in enumerate(pairs):
        va, vb = vecs[i * 2], vecs[i * 2 + 1]
        sim = cosine_similarity(va, vb)
        print(f"  {sim:.4f}  |  '{a}' vs '{b}'")


def semantic_search():
    print("\n=== 语义搜索 ===")
    corpus = [
        "Python 是一种高级编程语言，以简洁著称",
        "猫咪喜欢在温暖的地方打盹",
        "机器学习需要大量高质量数据",
        "法国的首都是巴黎",
        "深度学习是机器学习的一个重要分支",
        "JavaScript 是 Web 前端开发的核心语言",
        "太阳是太阳系的中心恒星",
    ]
    query = "AI 模型训练需要什么？"
    all_vecs = embed(corpus + [query])
    corpus_vecs, query_vec = all_vecs[:-1], all_vecs[-1]

    results = sorted(
        [(cosine_similarity(query_vec, cv), text) for cv, text in zip(corpus_vecs, corpus)],
        reverse=True,
    )
    print(f"  Query: {query!r}")
    print("  Top 3 结果:")
    for rank, (score, text) in enumerate(results[:3], 1):
        print(f"    {rank}. [{score:.4f}] {text}")


def dimension_reduction():
    print("\n=== 降维（指定 dimensions 参数）===")
    text = ["OpenAI embeddings support dimension reduction"]
    for dim in [256, 512, 1536]:
        vecs = embed(text, dimensions=dim)
        print(f"  dimensions={dim}: 实际向量维度 = {len(vecs[0])}")


def token_usage():
    print("\n=== Token 用量统计 ===")
    texts = ["Hello world", "这是第二段文本", "Third document here"]
    response = client.embeddings.create(model=MODEL, input=texts)
    print(f"  prompt_tokens: {response.usage.prompt_tokens}")
    print(f"  total_tokens: {response.usage.total_tokens}")


if __name__ == "__main__":
    single_embed()
    batch_embed()
    similarity_demo()
    semantic_search()
    dimension_reduction()
    token_usage()
