from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
import os
import sys

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    print("[系统] 找不到 OPENROUTER_API_KEY。请先在 .env 文件里写入密钥。")
    sys.exit(1)

# 获取用户输入：优先使用命令行参数，否则读取一行输入
try:
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = input("你：")
except (EOFError, KeyboardInterrupt):
    print("\n[系统] 已取消输入。")
    sys.exit(0)

if not prompt.strip():
    print("[系统] 输入为空，请输入内容后再运行。")
    sys.exit(0)

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    timeout=120,
)

try:
    response = client.chat.completions.create(
        model="anthropic/claude-opus-4",
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.choices[0].message.content
    if content:
        print(content)
    else:
        print("[系统] API 返回为空。")
except Exception as e:
    print(f"[系统] 调用失败：{e}")
# MIT License | 郑先隽，北师大心理学部教授，人本AI设计与创新
