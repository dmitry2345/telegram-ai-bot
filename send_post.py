import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HF_TOKEN = os.getenv("HF_TOKEN")

def generate_post():
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

    prompt = (
        "Напиши короткую, позитивную, интересную новость из России в стиле Telegram-поста. "
        "Тема должна быть безопасной, без политики, с эмодзи и лёгким юмором. Пример:\n\n"
        "🚀 В Казани школьники собрали собственную ракету на уроке труда. Уже планируют запуск!"
    )

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": f"[INST] {prompt} [/INST]",
        "options": {
            "wait_for_model": True
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Ошибка HuggingFace API: {response.status_code} - {response.text}")

    data = response.json()
    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"].strip()
    else:
        raise Exception("Неверный ответ HuggingFace API")

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
