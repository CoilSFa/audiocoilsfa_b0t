import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = FastAPI()
application: Application = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text("Привет! Бот работает через вебхук ✅")

application.add_handler(CommandHandler("start", start))


@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.bot.delete_webhook()
    await application.bot.set_webhook(url=WEBHOOK_URL)
    print("✅ Webhook установлен!")


@app.on_event("shutdown")
async def on_shutdown():
    await application.shutdown()


@app.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)  # ✅ Критическая строка
    return {"ok": True}
