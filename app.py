from fastapi import FastAPI, Request
from telegram import Update
from bot import application
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

app = FastAPI()

# Гарантируем однократную инициализацию
is_initialized = False

@app.post("/webhook")
async def webhook(request: Request):
    global is_initialized
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)

        if not is_initialized:
            logger.info("🔧 Initializing Telegram application...")
            await application.initialize()
            is_initialized = True

        logger.info("📩 Processing update...")
        await application.process_update(update)

        return {"ok": True}
    except Exception as e:
        logger.exception("❌ Ошибка при обработке вебхука:")
        return {"ok": False, "error": str(e)}

@app.get("/")
async def root():
    return {"status": "Webhook is running"}
