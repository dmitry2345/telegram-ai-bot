import os
import datetime
import requests
import feedparser
import random

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RSS_FEEDS = [
    "https://habr.com/ru/rss/",
    "https://vc.ru/rss/all",
    "https://rssexport.rbc.ru/rbcnews/news/30/full.rss"
]

BANNED_KEYWORDS = [
    "Украина", "Путин", "мобилизация", "взрыв", "теракт", "насилие",
    "спецоперация", "Навальный", "санкции", "экстремизм", "МИД"
]

INTRO_LINES = [
    "🔥 Самое интересное из мира технологий:",
    "💡 Сегодня в новостях:",
    "🚀 Вот что обсуждают прямо сейчас:",
    "📱 Не пропустите важное:",
    "🧠 Свежие идеи и тренды:"
]

EMOJI_LIST = ["💻", "📊", "📡", "📱", "🚀", "🧠", "🔍"]

def is_safe(title):
    lower = title.lower()
    return not any(bad.lower() in lower for bad in BANNED_KEYWORDS)

def get_catchy_news():
    today = datetime.date.today().strftime("%d.%m.%Y")
    intro = random.choice(INTRO_LINES)
    message = f"<b>{intro}</b>\n\n"

    entries = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        entries.extend(feed.entries)

    random.shuffle(entries)
    seen = set()
    count = 0

    for entry in entries:
        title = entry.title.strip()
        link = entry.link
        if title not in seen and is_safe(title):
            seen.add(title)
            emoji = random.choice(EMOJI_LIST)
            message += f"{emoji} <b>{title}</b>\n<a href='{link}'>Читать →</a>\n\n"
            count += 1
        if count == 5:
            break

    if count == 0:
        return "⚠️ Сегодня нет безопасных новостей для публикации."

    message += "<i>Источник: Хабр, VC.ru, РБК</i>"
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
    news = get_catchy_news()
    send_to_telegram(news)

if __name__ == "__main__":
    main()
