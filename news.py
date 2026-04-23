with open("C:\\Users\\gonbe\\Desktop\\log.txt", "a", encoding="utf-8") as f:
    f.write("実行された\n")

import requests
from openai import OpenAI

import os
from openai import OpenAI

import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
print("KEY:", api_key)

client = OpenAI(api_key=api_key)

url = "https://newsapi.org/v2/everything?q=Japan&apiKey=3c1265346560455dab50e1b3185182c0"

res = requests.get(url)
data = res.json()

articles = data.get("articles", [])

for article in articles[:3]:
    text = article.get("title") + " " + str(article.get("description"))

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "ニュースを日本語で一文で要約してください"},
            {"role": "user", "content": text}
        ]
    )

    print("元タイトル:", article.get("title"))
    print("要約:", response.choices[0].message.content)
    print("------")

with open("C:\\Users\\gonbe\\Desktop\\news.txt", "w", encoding="utf-8") as f:
    for article in data["articles"][:5]:
        title = article["title"]
        desc = article.get("description", "")

        prompt = f"{title}\n{desc}\n要約して"

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        summary = response.choices[0].message.content

        f.write(f"元タイトル: {title}\n")
        f.write(f"要約: {summary}\n")
        f.write("------\n")

webhook_url = "https://discord.com/api/webhooks/1496901091458154496/5RXCIo267gaPaGyScCEDsqA2S6xf4-jCtQgDbm-w82uiyRAYx3hiRitblqftCyei0WSo"
message = "【今日のニュース】\n\n"

for article in articles[:3]:
    title = article["title"]
    desc = article.get("description", "")

    prompt = f"{title}\n{desc}\n要約して"

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    summary = response.choices[0].message.content

    message += f"・{summary}\n"

requests.post(webhook_url, json={"content": message})

