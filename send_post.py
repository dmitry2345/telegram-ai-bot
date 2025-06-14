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

# Стоп-слова (можно дополнять)
BANNED_KEYWORDS = [
    "Украина", "Путин", "мобилизация", "взрыв", "теракт", "боевые действия",
    "ЛГБТ", "смерть", "убийство", "насилие", "протест", "политика", "санкции",
    "Навальный", "СВО", "спецоперация", "экстремизм", "МИД", "Минобороны"
]

def is_safe(title):
    """Проверяет, не содержит ли заголовок запрещённых слов."""
    lower_title = title.lower()
    for word in BANNED_KEYWORDS:
        if word.lower() in lower_title:
            return False
    return True

def get_safe_news():
    today = datetime.date.today().strftime("%d.%m.%Y")
    message = f"<b>Технологические новости на {today}:</b>\n\n"

    entries = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        entries.extend(feed.entries)

    unique_titles = set()
    filtered_news = []

    for entry in entries:
        title = entry.title.strip()
        link = entry.link
        if title not in unique_titles and is_safe(title):
            unique_titles.add(title)
            filtered_news.append(f"🔹 <a href='{link}'>{title}</a>")

    if not filtered_news:
        return f"<b>Нет подходящих новостей на {today}</b>\nВсе материалы отфильтрованы по безопасности."

    random.shuffle(filtered_news)
    message += "\n".join(filtered_news[:5])
    message += "\n\n<i>Источник: Хабр, VC.ru, РБК</i>"
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
    news = get_safe_news()
    send_to_telegram(news)

if __name__ == "__main__":
    main()
