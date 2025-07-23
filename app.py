from fastapi import FastAPI, Request
from telegram import Update
from bot import application  # твой telegram.Application
import logging

logger = logging.getLogger(__name__)
app = FastAPI()

# --- Выполняем инициализацию Telegram приложения при запуске ---
@app.on_event("startup")
async def startup_event():
    await application.initialize()
    logger.info("✅ Telegram Application инициализировано")

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/webhook")
async def webhook(request: Request):
    try:
        update_data = Update.de_json(await request.json(), application.bot)
        await application.process_update(update_data)
        return {"status": "processed"}
    except Exception as e:
        logger.exception(f"Ошибка при обработке вебхука: {e}")
        return {"status": "error", "detail": str(e)}
