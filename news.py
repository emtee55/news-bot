import os
import requests
from openai import OpenAI

# =========================
# 設定
# =========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = "ここにニュースAPIキー"
DISCORD_WEBHOOK_URL = "ここにWebhook（任意）"

if not OPENAI_API_KEY:
    raise ValueError("OpenAI APIキーが設定されていません")

client = OpenAI(api_key=OPENAI_API_KEY)

# =========================
# ニュース取得
# =========================
url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
data = requests.get(url).json()

# =========================
# フィルター＆重複除去
# =========================
KEYWORDS = ["AI", "Tech", "Business", "Economy", "Startup"]

seen = set()
filtered = []

for a in data["articles"]:
    title = a.get("title")
    if not title:
        continue

    # 重複排除
    if title in seen:
        continue
    seen.add(title)

    # 重要度フィルター
    if any(k.lower() in title.lower() for k in KEYWORDS):
        filtered.append(a)

articles = filtered[:10]

# =========================
# AI処理関数
# =========================
def rewrite_title(title):
    try:
        res = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "ニュースの見出しを日本語で分かりやすく魅力的に書き換えてください"},
                {"role": "user", "content": title}
            ]
        )
        return res.choices[0].message.content.strip()
    except:
        return title


def summarize(text):
    try:
        res = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "重要ポイントを日本語で簡潔に要約してください"},
                {"role": "user", "content": text}
            ]
        )
        return res.choices[0].message.content.strip()
    except:
        return "要約失敗"


def short_summary(text):
    try:
        res = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "内容を一文で超簡潔にまとめてください"},
                {"role": "user", "content": text}
            ]
        )
        return res.choices[0].message.content.strip()
    except:
        return ""


def categorize(title):
    t = title.lower()
    if "ai" in t:
        return "AI"
    elif "stock" in t or "economy" in t:
        return "経済"
    elif "tech" in t:
        return "テック"
    else:
        return "その他"

# =========================
# メイン処理
# =========================
results = []

for article in articles:
    title = article["title"]

    jp_title = rewrite_title(title)
    summary = summarize(title)
    short = short_summary(title)
    category = categorize(title)

    results.append(
        f"【{category}】\n"
        f"📰 {jp_title}\n"
        f"💡 {short}\n"
        f"📝 {summary}\n"
        "------"
    )

output = "\n".join(results)

# =========================
# ファイル保存
# =========================
with open("news.txt", "w", encoding="utf-8") as f:
    f.write(output)

print(output)

# =========================
# Discord通知（任意）
# =========================
if DISCORD_WEBHOOK_URL:
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": output})
    except:
        print("Discord送信失敗")
