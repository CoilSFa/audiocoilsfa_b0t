from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
from utils import convert_to_wav
from summarize import transcribe_and_summarize
from pdf_generator import generate_pdf

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
application = ApplicationBuilder().token(TOKEN).build()

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = await update.message.audio.get_file() if update.message.audio else await update.message.voice.get_file()
        file_path = f"temp_{file.file_unique_id}.ogg"
        await file.download_to_drive(file_path)

        wav_path = convert_to_wav(file_path)
        summary_text = transcribe_and_summarize(wav_path)

        pdf_path = generate_pdf(summary_text)
        await update.message.reply_document(document=open(pdf_path, "rb"), filename="summary.pdf")

        os.remove(file_path)
        os.remove(wav_path)
        os.remove(pdf_path)
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при обработке файла. Попробуй ещё раз.")
        print(f"[ERROR] {e}")

application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_audio))
