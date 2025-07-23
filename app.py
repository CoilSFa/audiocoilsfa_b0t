from fastapi import FastAPI, Request
from bot import application
import logging

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Bot is running!"}

@app.post("/webhook")
async def webhook(request: Request):
    try:
        update_data = await request.json()
        await application.process_update(update_data)
    except Exception as e:
        logging.exception(f"Ошибка при обработке вебхука: {e}")
    return {"ok": True}
