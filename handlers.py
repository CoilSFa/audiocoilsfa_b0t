from telegram import Update
from telegram.ext import ContextTypes
from whisper_utils import transcribe_voice

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь голосовое или аудиофайл — я расшифрую его.")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Обрабатываю голосовое сообщение...")
    transcript = await transcribe_voice(update, context, is_voice=True)
    await update.message.reply_text(f"Расшифровка: {transcript}")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Обрабатываю аудиофайл...")
    transcript = await transcribe_voice(update, context, is_voice=False)
    await update.message.reply_text(f"Расшифровка: {transcript}")