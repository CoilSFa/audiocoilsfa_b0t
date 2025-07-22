from fastapi import FastAPI, Request
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import asyncio
import os
import uuid

from config import BOT_TOKEN, WEBHOOK_URL, AUDIO_DIR, TEXT_DIR
from transcribe import transcribe_audio
from summarize import summarize_text
from utils import convert_to_wav

app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()

@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.bot.delete_webhook()
    await application.bot.set_webhook(url=WEBHOOK_URL)
    print("✅ Webhook установлен!")

@app.post("/webhook")
async def webhook(request: Request):
    update = Update.de_json(await request.json(), application.bot)
    await application.process_update(update)
    return "OK"

# --- Handlers ---

async def start(update: Update, context):
    await update.message.reply_text("Привет! Пришли мне аудио или голосовое сообщение, и я расшифрую его.")

async def handle_audio(update: Update, context):
    audio_file = update.message.voice or update.message.audio or update.message.document
    if not audio_file:
        return await update.message.reply_text("Отправь голосовое или аудио файл.")

    file_id = audio_file.file_id
    file = await context.bot.get_file(file_id)

    file_name = f"{uuid.uuid4()}"
    original_path = f"{AUDIO_DIR}/{file_name}.oga"
    wav_path = f"{AUDIO_DIR}/{file_name}.wav"

    await file.download_to_drive(original_path)
    convert_to_wav(original_path, wav_path)

    # Распознавание
    try:
        transcription = transcribe_audio(wav_path)
    except Exception as e:
        return await update.message.reply_text(f"Ошибка при распознавании: {e}")

    # Сохранение текста
    with open(f"{TEXT_DIR}/{file_name}.txt", "w") as f:
        f.write(transcription)

    # Резюме
    try:
        summary = summarize_text(transcription)
    except Exception as e:
        summary = "Не удалось сделать выжимку."

    await update.message.reply_text(f"📝 Расшифровка:\n{transcription[:1000]}")
    await update.message.reply_text(f"📌 Выжимка:\n{summary[:1000]}")

# --- Router setup ---
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.Document.AUDIO, handle_audio))
