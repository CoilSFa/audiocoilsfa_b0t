from fastapi import FastAPI, Request
from telegram import Update
from bot import application
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("[INFO] Initializing Telegram bot")
    await application.initialize()  # 💡 Это важно для Webhook
    await application.start()
    print("[INFO] Bot started")

@app.on_event("shutdown")
async def shutdown_event():
    await application.stop()
    await application.shutdown()

@app.get("/")
async def root():
    return {"status": "bot is running"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)  # 💡 Преобразуем словарь в Update
    await application.process_update(update)
    return {"ok": True}
