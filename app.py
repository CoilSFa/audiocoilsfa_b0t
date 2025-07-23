from fastapi import FastAPI, Request
from telegram import Update
from bot import application
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        
        # 🔧 Обязательная инициализация
        if not application.ready:
            await application.initialize()

        await application.process_update(update)
        return {"ok": True}
    except Exception as e:
        logger.exception("Ошибка при обработке вебхука:")
        return {"ok": False, "error": str(e)}

@app.get("/")
async def root():
    return {"status": "ok"}
