import os
import datetime
import requests
import feedparser

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Можно заменить на другой RSS-источник
RSS_URL = "https://www.theverge.com/rss/index.xml"

def get_rss_news():
    feed = feedparser.parse(RSS_URL)
    today = datetime.date.today().strftime("%d.%m.%Y")
    message = f"<b>Техно-новости на {today}:</b>\n\n"
    
    for entry in feed.entries[:5]:  # Берем только 5 свежих
        title = entry.title
        link = entry.link
        message += f"🔹 <a href='{link}'>{title}</a>\n"

    message += "\n<i>Источник: The Verge</i>"
    return message

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    response = requests.post(url, data=payload)
    if not response.ok:
        raise Exception(f"Ошибка Telegram API: {response.text}")

def main():
    news = get_rss_news()
    send_to_telegram(news)

if __name__ == "__main__":
    main()
