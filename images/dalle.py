"""
Images - DALL·E 3 / DALL·E 2
涵盖: 生成 / 不同尺寸 / 多张 / Base64 返回 / 图片变体 / 图片编辑
"""
import base64
import sys, os
import urllib.request
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.client import client

OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def download_image(url: str, path: Path):
    urllib.request.urlretrieve(url, path)
    print(f"    已下载: {path.name}")


def generate_dalle3():
    print("=== DALL·E 3 生成 ===")
    response = client.images.generate(
        model="dall-e-3",
        prompt="A futuristic city skyline at sunset with flying cars, cyberpunk style, ultra-detailed, 4K",
        size="1024x1024",
        quality="standard",   # standard | hd (hd 更贵但质量更高)
        style="vivid",        # vivid | natural
        n=1,
    )
    img = response.data[0]
    download_image(img.url, OUTPUT_DIR / "dalle3_1024.png")
    print(f"  修改后的 prompt: {img.revised_prompt[:80]}...")


def generate_dalle3_sizes():
    print("\n=== DALL·E 3 不同尺寸 ===")
    sizes = ["1024x1024", "1792x1024", "1024x1792"]
    for size in sizes:
        r = client.images.generate(
            model="dall-e-3",
            prompt="A serene mountain lake at dawn",
            size=size,
        )
        w, h = size.split("x")
        download_image(r.data[0].url, OUTPUT_DIR / f"dalle3_{w}x{h}.png")


def generate_dalle2_multiple():
    print("\n=== DALL·E 2 生成多张 ===")
    response = client.images.generate(
        model="dall-e-2",
        prompt="A cute robot drinking coffee in a cozy cafe",
        size="512x512",
        n=3,
    )
    for i, img in enumerate(response.data):
        download_image(img.url, OUTPUT_DIR / f"dalle2_multi_{i}.png")


def generate_b64():
    print("\n=== 返回 Base64 格式 ===")
    response = client.images.generate(
        model="dall-e-2",
        prompt="A simple geometric abstract pattern with primary colors",
        size="256x256",
        response_format="b64_json",
    )
    data = base64.b64decode(response.data[0].b64_json)
    out = OUTPUT_DIR / "dalle2_b64.png"
    out.write_bytes(data)
    print(f"  已保存: {out.name} ({len(data):,} bytes)")


def create_variation(image_path: str):
    """创建图片变体（仅 DALL·E 2 支持，图片需为正方形 PNG，≤4MB）"""
    print("\n=== DALL·E 2 图片变体 ===")
    with open(image_path, "rb") as f:
        response = client.images.create_variation(model="dall-e-2", image=f, n=2, size="512x512")
    for i, img in enumerate(response.data):
        download_image(img.url, OUTPUT_DIR / f"dalle2_variation_{i}.png")


def edit_image(image_path: str, mask_path: str):
    """
    编辑图片（inpainting）
    image_path: 原始 PNG (带 alpha 通道)
    mask_path:  遮罩 PNG (透明区域 = 待填充区域)
    """
    print("\n=== DALL·E 2 图片编辑 (Inpainting) ===")
    with open(image_path, "rb") as img, open(mask_path, "rb") as mask:
        response = client.images.edit(
            model="dall-e-2",
            image=img,
            mask=mask,
            prompt="A beautiful flower arrangement",
            size="512x512",
        )
    download_image(response.data[0].url, OUTPUT_DIR / "dalle2_edited.png")


if __name__ == "__main__":
    generate_dalle3()
    generate_dalle3_sizes()
    generate_dalle2_multiple()
    generate_b64()
    # 以下需要提供本地图片（取消注释）:
    # create_variation("your_image.png")
    # edit_image("your_image.png", "your_mask.png")
