import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from utils import convert_to_wav
from summarize import transcribe_and_summarize
from pdf_generator import generate_pdf

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
application = ApplicationBuilder().token(TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь мне голосовое или аудиофайл, и я пришлю тебе PDF с кратким содержанием."
    )

# Обработчик голосовых и аудио
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("[INFO] Получен файл...")
        file = await update.message.audio.get_file() if update.message.audio else await update.message.voice.get_file()
        file_path = f"temp_{file.file_unique_id}.ogg"
        await file.download_to_drive(file_path)
        print(f"[INFO] Файл сохранён: {file_path}")

        wav_path = convert_to_wav(file_path)
        print(f"[INFO] Конвертирован в: {wav_path}")

        try:
            summary_text = transcribe_and_summarize(wav_path)
        except Exception as e:
            await update.message.reply_text("Ошибка при распознавании аудио: " + str(e))
            print(f"[ERROR] {e}")
            return

        pdf_path = generate_pdf(summary_text)
        await update.message.reply_document(open(pdf_path, "rb"), filename="summary.pdf")

        os.remove(file_path)
        os.remove(wav_path)
        os.remove(pdf_path)

    except Exception as e:
        await update.message.reply_text("Произошла ошибка при обработке. Попробуйте снова.")
        print(f"[ERROR] {e}")

# Регистрация хендлеров
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_audio))
