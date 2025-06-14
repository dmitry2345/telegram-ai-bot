import os
import datetime
import requests

# Переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = "EleutherAI/gpt-j-6B"
HF_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def generate_text_for_today() -> str:
    today = datetime.date.today().strftime("%d.%m.%Y")
    prompt = f"Технологические новости за {today}:"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200}}
    response = requests.post(HF_URL, headers=HEADERS, json=payload, timeout=60)
    if response.status_code != 200:
        raise Exception(f"HF API status {response.status_code}: {response.text}")
    data = response.json()
    if isinstance(data, dict) and data.get("error"):
        raise Exception(f"HF API error: {data['error']}")
    if not isinstance(data, list) or not data:
        raise Exception(f"Неправильный формат ответа HF: {data}")
    body = data[0].get("generated_text", "").strip()
    if not body:
        raise Exception("HF вернул пустой текст")
    affiliate = "https://www.amazon.com/dp/B00EXAMPLE/?tag=yourID-20"
    return (
        f"<b>Новости {today}</b>\n\n"
        f"{body}\n\n"
        f"<a href=\"{affiliate}\">Рекомендуемый товар</a>"
    )

def main():
    text = generate_text_for_today()
    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    r = requests.post(send_url, data=payload, timeout=30)
    if not r.ok:
        raise Exception(f"Telegram API error {r.status_code}: {r.text}")

if __name__ == "__main__":
    main()
