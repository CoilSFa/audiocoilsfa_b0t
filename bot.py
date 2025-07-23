import traceback
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from dotenv import load_dotenv
import os
from utils import convert_to_wav
from summarize import transcribe_and_summarize
from pdf_generator import generate_pdf

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
application = ApplicationBuilder().token(TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне голосовое или аудиофайл, и я пришлю тебе PDF с кратким содержанием.")

# Обработчик аудио/голосовых сообщений
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message
        print("[INFO] Получен файл...")

        file = await (message.audio or message.voice).get_file()
        file_path = f"temp_{file.file_unique_id}.ogg"
        await file.download_to_drive(file_path)
        print(f"[INFO] Файл сохранён: {file_path}")

        wav_path = convert_to_wav(file_path)
        print(f"[INFO] Конвертирован в: {wav_path}")

        summary_text = transcribe_and_summarize(wav_path)
        pdf_path = generate_pdf(summary_text)

        await message.reply_document(document=open(pdf_path, "rb"), filename="summary.pdf")

        # Удаляем временные файлы
        os.remove(file_path)
        os.remove(wav_path)
        os.remove(pdf_path)

    except Exception as e:
        await update.message.reply_text("⚠️ Произошла ошибка при обработке. Попробуйте снова.")
        print("[ERROR]", e)
        traceback.print_exc()

# Регистрация обработчиков
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_audio))
