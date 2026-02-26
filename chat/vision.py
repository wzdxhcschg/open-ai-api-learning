"""
Chat Completions - Vision (图片理解)
涵盖: URL 图片 / Base64 本地图片 / detail 参数对比
"""
import base64
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.client import client

SAMPLE_IMAGE_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/"
    "PNG_transparency_demonstration_1.png/280px-PNG_transparency_demonstration_1.png"
)


def vision_url():
    print("=== Vision (URL) ===")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "这张图里有什么？请详细描述"},
                {"type": "image_url", "image_url": {"url": SAMPLE_IMAGE_URL, "detail": "auto"}},
            ],
        }],
    )
    print(response.choices[0].message.content)


def vision_base64(image_path: str):
    print("\n=== Vision (Base64 本地图片) ===")
    ext = os.path.splitext(image_path)[-1].lstrip(".").lower()
    media_type = {
        "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "png": "image/png", "gif": "image/gif", "webp": "image/webp"
    }.get(ext, "image/png")
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "描述这张图片的内容"},
                {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{b64}"}},
            ],
        }],
    )
    print(response.choices[0].message.content)


def vision_detail_comparison():
    """high detail 消耗更多 token 但识别更准确"""
    print("\n=== Detail 参数对比 ===")
    for detail in ["low", "high"]:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "图中有几个形状？只回答数字"},
                    {"type": "image_url", "image_url": {"url": SAMPLE_IMAGE_URL, "detail": detail}},
                ],
            }],
        )
        usage = r.usage
        print(f"  detail={detail}: {r.choices[0].message.content.strip()}  (tokens: {usage.prompt_tokens})")


if __name__ == "__main__":
    vision_url()
    vision_detail_comparison()
    # 本地图片示例（取消注释）:
    # vision_base64("your_image.png")
