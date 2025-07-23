import logging
from fastapi import FastAPI, Request
from telegram import Update
from bot import application  # Объект telegram.Application

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI()

# ✅ Инициализация Telegram Application при запуске сервера
@app.on_event("startup")
async def startup_event():
    await application.initialize()
    logger.info("✅ Telegram Application инициализировано")

# 🌐 Простой healthcheck
@app.get("/")
async def root():
    return {"status": "ok"}

# 📬 Webhook для Telegram
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        logger.exception(f"❌ Ошибка при обработке вебхука: {e}")
        return {"status": "error", "detail": str(e)}
