from telegram import Update, Audio, Voice
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне аудиофайл или голосовое сообщение, и я его расшифрую 🧠")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я получил твоё голосовое сообщение! 🎤 (Пока я не обрабатываю его, но скоро буду!)")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Аудиофайл получен! 🔊 (В следующей версии я начну его обрабатывать)")

def main():
    import os
    token = os.getenv("BOT_TOKEN")
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    application.run_polling()

if __name__ == "__main__":
    main()
