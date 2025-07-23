import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from dotenv import load_dotenv
from utils import convert_to_wav
from summarize import transcribe_and_summarize
from pdf_generator import generate_pdf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
application = ApplicationBuilder().token(TOKEN).build()
MAX_TG_MESSAGE_LENGTH = 4096

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Отправь мне аудиофайл или голосовое сообщение, и я пришлю тебе краткое содержание + PDF.")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🟢 handle_audio STARTED")
    try:
        logger.info("📩 Получено сообщение от пользователя")

        message = update.message
        file = None
        if message.voice:
            file = await message.voice.get_file()
        elif message.audio:
            file = await message.audio.get_file()
        elif message.document and message.document.mime_type.startswith("audio/"):
            file = await message.document.get_file()
        else:
            await message.reply_text("⚠️ Пожалуйста, отправьте аудиофайл или голосовое сообщение.")
            return

        ogg_path = f"temp_{file.file_unique_id}"
        extension = os.path.splitext(file.file_path)[1] or ".ogg"
        ogg_path += extension
        await file.download_to_drive(ogg_path)
        logger.info(f"💾 Файл сохранён: {ogg_path}")

        wav_path = convert_to_wav(ogg_path)
        logger.info(f"🎵 Конвертирован в: {wav_path}")

        full_text, summary_text = transcribe_and_summarize(wav_path)
        logger.info(f"📄 Получен полный текст ({len(full_text)} символов)")
        logger.info(f"📝 Получено summary ({len(summary_text)} символов)")

        pdf_path = generate_pdf(full_text)

        for i in range(0, len(summary_text), MAX_TG_MESSAGE_LENGTH):
            chunk = summary_text[i:i+MAX_TG_MESSAGE_LENGTH]
            await message.reply_text(f"📝 Краткое содержание:{chunk}")

        await message.reply_document(document=pdf_path)

        os.remove(ogg_path)
        os.remove(wav_path)
        os.remove(pdf_path)

    except Exception as e:
        logger.exception("❌ Ошибка при обработке аудио:")
        await update.message.reply_text("⚠️ Произошла ошибка при обработке. Попробуйте снова.")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO | filters.Document.AUDIO, handle_audio))
