import os
import datetime
import logging
import requests
from telegram import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue

# 1) Логирование
logging.basicConfig(
    format='%(asctime)s — %(levelname)s — %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2) Переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = "EleutherAI/gpt-j-6B"
HF_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# 3) Команда /start
async def start_command(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я публикую новости в канал по расписанию.\n"
        "Команды:\n"
        "/start — это сообщение\n"
        "/now — немедленно запостить свежие новости"
    )

# 4) Команда /now
async def now_command(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = generate_text_for_today()
        await context.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False
        )
        await update.message.reply_text("✅ Опубликовал в канал.")
    except Exception as e:
        logger.error(f"Ошибка в /now: {e}")
        await update.message.reply_text(f"❌ Не удалось опубликовать: {e}")

# 5) Функция по расписанию
async def scheduled_post(context: ContextTypes.DEFAULT_TYPE):
    try:
        text = generate_text_for_today()
        await context.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False
        )
    except Exception as e:
        logger.error(f"Ошибка в scheduled_post: {e}")

# 6) Генерация текста с проверками
def generate_text_for_today() -> str:
    today = datetime.date.today().strftime("%d.%m.%Y")
    prompt = f"Технологические новости за {today}:"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200}}
    response = requests.post(HF_URL, headers=HEADERS, json=payload, timeout=60)
    # Проверяем код ответа
    if response.status_code != 200:
        raise Exception(f"HF API status {response.status_code}: {response.text}")
    data = response.json()
    # Проверяем наличие ошибок в ответе
    if isinstance(data, dict) and data.get("error"):
        raise Exception(f"HF API error: {data['error']}")
    if not isinstance(data, list) or not data:
        raise Exception(f"Неправильный формат ответа HF: {data}")
    body = data[0].get("generated_text", "").strip()
    if not body:
        raise Exception("HF вернул пустой текст")
    # Вставляем affiliate‑ссылку
    affiliate = "https://www.amazon.com/dp/B00EXAMPLE/?tag=yourID-20"
    return (
        f"<b>Новости {today}</b>\n\n"
        f"{body}\n\n"
        f"<a href=\"{affiliate}\">Рекомендуемый товар</a>"
    )

# 7) Точка входа бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("now", now_command))
    # Расписание: каждые 3600 с (1 час)
    app.job_queue.run_repeating(scheduled_post, interval=3600, first=10)
    logger.info("Бот запущен и слушает обновления...")
    app.run_polling()

if __name__ == "__main__":
    main()
