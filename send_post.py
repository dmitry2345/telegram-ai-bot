import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def generate_post():
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

    prompt = (
        "Составь короткий новостной пост для Telegram-канала на русском языке. "
        "Тема — актуальные новости России. Пиши кратко, интересно и безопасно, избегай острых тем. "
        "Пример: 📰 В Москве запустили новый маршрут электробусов. Подробнее в источниках."
    )

    headers = {"Content-Type": "application/json"}
    payload = {
        "inputs": f"[INST] {prompt} [/INST]",
        "options": {
            "wait_for_model": True
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Ошибка HuggingFace API: {response.status_code} - {response.text}")

    result = response.json()
    if isinstance(result, list) and len(result) > 0:
        return result[0]["generated_text"].strip()
    else:
        raise Exception("Ответ HuggingFace некорректен")

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
