from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, ApplicationBuilder
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = FastAPI()

application = ApplicationBuilder().token(BOT_TOKEN).build()

# 🔽 Тут будут хендлеры, например:
# application.add_handler(...)

# ✅ Добавляем запуск вебхука на старте
@app.on_event("startup")
async def on_startup():
    await application.bot.delete_webhook()
    await application.bot.set_webhook(url=WEBHOOK_URL)

# ✅ Приём обновлений от Telegram
@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"ok": True}
