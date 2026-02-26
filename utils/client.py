"""统一的 OpenAI client 初始化，所有模块共用"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("请在 .env 文件中设置 OPENAI_API_KEY")
    return OpenAI(api_key=api_key)


client = get_client()
