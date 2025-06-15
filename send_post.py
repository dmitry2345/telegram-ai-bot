import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def generate_post():
    url = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

    prompt = (
        "Составь короткий новостной пост для Telegram-канала на русском языке. "
        "Тема — актуальные, безопасные новости из России. Пиши кратко, интересно, не упоминай политику и конфликты. "
        "Формат — Telegram-пост с эмодзи. Пример:\n"
        "📰 В Сочи открылся новый арт-фестиваль. Ждут более 10 тысяч гостей!"
    )

    headers = {"Content-Type": "application/json"}
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Ошибка HuggingFace API: {response.status_code} - {response.text}")

    result = response.json()
    if isinstance(result, list) and len(result) > 0:
        return result[0]["generated_text"].strip()
    else:
        raise Exception("Ответ HuggingFace пуст или некорректен")

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    if not response.ok:
        raise Exception(f"Ошибка Telegram API: {response.text}")

def main():
    post = generate_post()
    send_to_telegram(post)

if __name__ == "__main__":
    main()
