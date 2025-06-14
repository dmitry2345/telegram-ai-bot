import os
import datetime
import requests
from openai import OpenAI

# Получаем переменные из окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Инициализируем OpenAI SDK
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_news():
    today = datetime.date.today().strftime("%d.%m.%Y")
    prompt = (
        f"Сгенерируй короткие технологические новости на сегодня ({today}) "
        "в стиле новостной сводки. Сделай их интересными, актуальными и информативными."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты технологический журналист."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.7
    )

    text = response.choices[0].message.content.strip()
    affiliate = "https://www.amazon.com/dp/B00EXAMPLE/?tag=yourID-20"
    return (
        f"<b>Новости {today}</b>\n\n"
        f"{text}\n\n"
        f"<a href=\"{affiliate}\">Рекомендуемый гаджет</a>"
    )

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    r = requests.post(url, data=payload)
    if not r.ok:
        raise Exception(f"Telegram error: {r.text}")

def main():
    news = generate_news()
    send_to_telegram(news)

if __name__ == "__main__":
    main()
