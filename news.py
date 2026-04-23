import os
import requests
from openai import OpenAI

# APIキー取得
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("APIキーが読み込めていません")

client = OpenAI(api_key=api_key)

# ニュース取得（例：NewsAPI）
NEWS_API_KEY = "3c1265346560455dab50e1b3185182c0"

url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
response = requests.get(url)
data = response.json()

articles = data["articles"][:3]

results = []

for article in articles:
    title = article["title"]

    # 要約（精度高め）
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "あなたは優秀なニュース編集者です。重要なポイントを日本語で簡潔に要約してください。"
            },
            {
                "role": "user",
                "content": title
            }
        ]
    )

    summary = res.choices[0].message.content

    results.append(f"元タイトル: {title}\n要約: {summary}\n------")

# テキストにまとめる
output = "\n".join(results)

# ファイル保存
with open("news.txt", "w", encoding="utf-8") as f:
    f.write(output)

print(output)

WEBHOOK_URL = "https://discord.com/api/webhooks/1496901091458154496/5RXCIo267gaPaGyScCEDsqA2S6xf4-jCtQgDbm-w82uiyRAYx3hiRitblqftCyei0WSo"

requests.post(WEBHOOK_URL, json={"content": output})
