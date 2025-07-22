import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters
)

from utils import convert_to_wav
from summarize import transcribe_and_summarize
from pdf_generator import generate_pdf

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

application = ApplicationBuilder().token(TOKEN).build()

# 🔹 Обработка /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь мне голосовое или аудиофайл, и я пришлю тебе PDF с кратким содержанием."
    )

# 🔹 Обработка аудио и голосовых
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("[INFO] Получен файл...")

        message = update.message
        file = None

        if message.voice:
            file = await message.voice.get_file()
        elif message.audio:
            file = await message.audio.get_file()
        else:
            await message.reply_text("Пожалуйста, отправь голосовое сообщение или аудиофайл.")
            return

        file_path = f"temp_{file.file_unique_id}.ogg"
        await file.download_to_drive(file_path)
        print(f"[INFO] Файл сохранён: {file_path}")

        # Конвертация и расшифровка
        wav_path = convert_to_wav(file_path)
        print(f"[INFO] Конвертирован в: {wav_path}")

        summary_text = transcribe_and_summarize(wav_path)
        print("[INFO] Расшифровка и выжимка завершены")

        pdf_path = generate_pdf(summary_text)
        await message.reply_document(document=open(pdf_path, "rb"), filename="summary.pdf")
        print("[INFO] PDF отправлен")

        # Очистка
        for f in [file_path, wav_path, pdf_path]:
            if os.path.exists(f):
                os.remove(f)

    except Exception as e:
        print(f"[ERROR] {e}")
        await update.message.reply_text("⚠️ Произошла ошибка при обработке. Попробуйте снова.")

# Добавляем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_audio))
