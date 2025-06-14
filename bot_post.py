import os
import datetime
import requests
from transformers import AutoTokenizer, AutoModelForCausalLM

# 1) Чтение переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HF_API_KEY = os.getenv("HF_API_KEY")

# 2) Инициализация модели через HuggingFace Inference API
API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def generate_text(prompt: str) -> str:
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200}}
    response = requests.post(API_URL, headers=headers, json=payload)
    data = response.json()
    return data[0]["generated_text"].strip()

# 3) Формирование контента
today = datetime.date.today().strftime("%d.%m.%Y")
prompt = f"Технологические новости за {today}:"
text = generate_text(prompt)

# 4) Прикрепление affiliate‑ссылки (можете использовать любую, например, Amazon)
affiliate_link = f"https://www.amazon.com/dp/B00EXAMPLE/?tag=yourID-20"
message = f"<b>Новости {today}</b>\n\n{text}\n\n<a href=\"{affiliate_link}\">Рекомендуемый товар</a>"

# 5) Отправка в Telegram
send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
payload = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": message,
    "parse_mode": "HTML",
    "disable_web_page_preview": False
}
requests.post(send_url, data=payload)
