from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
import os
import sys

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    print("[系统] 找不到 OPENROUTER_API_KEY。请先在 .env 文件里写入密钥。")
    sys.exit(1)

# 读取通用提示词和领域技能，拼接成系统提示词
SCRIPT_DIR = os.path.dirname(__file__)
try:
    agent_prompt = open(os.path.join(SCRIPT_DIR, "agent.md"), "r", encoding="utf-8").read()
    skill_prompt = open(os.path.join(SCRIPT_DIR, "skill.md"), "r", encoding="utf-8").read()
except FileNotFoundError as e:
    print(f"[系统] 找不到提示词文件：{e}")
    sys.exit(1)

system_prompt = agent_prompt + "\n\n" + skill_prompt
messages = [{"role": "system", "content": system_prompt}]

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    timeout=120,
)

while True:
    try:
        user_input = input("\n你：")
    except EOFError:
        break
    except KeyboardInterrupt:
        print("\n[系统] 已退出。")
        break

    messages.append({"role": "user", "content": user_input})

    while True:
        try:
            response = client.chat.completions.create(
                model="anthropic/claude-opus-4",
                messages=messages,
            )
        except Exception as e:
            print(f"[系统] API 调用失败：{e}")
            break

        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        print(f"[AI] {reply}")

        if reply.strip().startswith("完成:"):
            break

        if "命令:" not in reply:
            print("[系统] AI 没有给出可执行命令，请重新描述任务。")
            break

        command = reply.strip().split("命令:")[1].strip()
        print(f"[系统] 正在执行: {command}")
        result = os.popen(command).read()
        print(f"[系统] {result}")
        messages.append({"role": "user", "content": f"执行完毕:{result}"})
