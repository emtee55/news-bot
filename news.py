import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
print("KEY:", api_key)

if not api_key:
    raise ValueError("APIキーが読み込めてない")

client = OpenAI(api_key=api_key)

print("START")

# テスト用
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "テスト"}]
)

print(response.choices[0].message.content)
