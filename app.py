from fastapi import FastAPI, Request
from telegram import Update
from bot import application
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bot is running"}

@app.post("/webhook")
async def webhook(request: Request):
    try:
        update_data = await request.json()
        update = Update.de_json(update_data, application.bot)
        await application.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        logger.exception("Ошибка при обработке вебхука:")
        return {"status": "error", "message": str(e)}
