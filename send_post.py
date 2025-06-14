import os
import datetime
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def generate_news():
    prompt = (
        "Сгенерируй 3 короткие технологические новости на русском языке, "
        "каждая не длиннее 2 предложений. Стиль — как у РБК, без политики, без шуток, "
        "без неподтверждённой информации. Строго по делу."
    )

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Ты — журналист-технолог."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"DeepSeek error: {response.status_code} - {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"].strip()

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"<b>AI‑новости на {datetime.date.today().strftime('%d.%m.%Y')}:</b>\n\n{text}",
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    if not response.ok:
        raise Exception(f"Telegram error: {response.text}")

def main():
    news = generate_news()
    send_to_telegram(news)

if __name__ == "__main__":
    main()
