import os
import datetime
import requests
import feedparser
import random

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Список русскоязычных RSS-лент
RSS_FEEDS = [
    "https://habr.com/ru/rss/",
    "https://vc.ru/rss/all",
    "https://rssexport.rbc.ru/rbcnews/news/30/full.rss"
]

def get_russian_news():
    today = datetime.date.today().strftime("%d.%m.%Y")
    message = f"<b>Свежие новости на {today}:</b>\n\n"
    
    entries = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        entries.extend(feed.entries)

    # Убираем дубли по названию
    unique_titles = set()
    news = []
    for entry in entries:
        title = entry.title.strip()
        if title not in unique_titles:
            unique_titles.add(title)
            link = entry.link
            news.append(f"🔹 <a href='{link}'>{title}</a>")

    random.shuffle(news)
    message += "\n".join(news[:5])  # Только 5 случайных

    message += "\n\n<i>Источник: Хабр, VC, РБК</i>"
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
    news = get_russian_news()
    send_to_telegram(news)

if __name__ == "__main__":
    main()
