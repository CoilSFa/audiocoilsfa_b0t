import os
import traceback
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
from dotenv import load_dotenv
from utils import convert_to_wav
from summarize import transcribe_and_summarize
from pdf_generator import generate_pdf
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Отправь голосовое сообщение, и я пришлю его расшифровку и краткое содержание.")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.info("📩 Получено сообщение от пользователя")

        file = await update.message.voice.get_file()
        ogg_path = f"temp_{file.file_unique_id}.ogg"
        await file.download_to_drive(ogg_path)
        logger.info(f"💾 Файл сохранён: {ogg_path}")

        wav_path = convert_to_wav(ogg_path)
        logger.info(f"🎵 Конвертирован в: {wav_path}")

        full_text, summary_text = transcribe_and_summarize(wav_path)

        logger.info(f"📄 Получен полный текст: {full_text}")
        logger.info(f"📝 Получен summary: {summary_text}")

        pdf_path = generate_pdf(full_text)

        await update.message.reply_text(
            f"📝 Краткое содержание:\n{summary_text}\n\n📄 PDF с полным текстом прилагается."
        )

        await update.message.reply_document(document=pdf_path)

    except Exception as e:
        logger.error(f"[ERROR] {e}")
        await update.message.reply_text("⚠️ Произошла ошибка при обработке. Попробуйте снова.")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_audio))
