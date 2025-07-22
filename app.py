import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, ApplicationBuilder

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Пример: https://audiocoilsfa-b0t.onrender.com/webhook

app = FastAPI()

application: Application = ApplicationBuilder().token(BOT_TOKEN).build()

@app.on_event("startup")
async def startup():
    await application.initialize()  # 🔥 Обязательно!
    await application.bot.delete_webhook()
    await application.bot.set_webhook(url=WEBHOOK_URL)
    print("✅ Webhook установлен!")

@app.on_event("shutdown")
async def shutdown():
    await application.shutdown()

@app.post("/webhook")
async def process_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"ok": True}

