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
    print("🟢 handle_audio STARTED")
    try:
        logger.info("📩 Получено сообщение от пользователя")

        # Определяем, какой тип аудио был прислан
        if update.message.voice:
            file = await update.message.voice.get_file()
            file_id = update.message.voice.file_unique_id
            extension = "ogg"

        elif update.message.audio:
            file = await update.message.audio.get_file()
            file_id = update.message.audio.file_unique_id
            extension = "mp3"

        elif update.message.document and update.message.document.mime_type.startswith("audio/"):
            file = await update.message.document.get_file()
            file_id = update.message.document.file_unique_id
            extension = update.message.document.file_name.split(".")[-1]  # .mp3, .m4a и т.д.

        else:
            logger.warning("⚠️ Сообщение не содержит поддерживаемого аудиофайла.")
            await update.message.reply_text("⚠️ Пожалуйста, отправьте аудиофайл (голосовое, .mp3, .m4a, .ogg).")
            return

        # Сохраняем файл
        input_path = f"temp_{file_id}.{extension}"
        await file.download_to_drive(input_path)
        logger.info(f"💾 Файл сохранён: {input_path}")

        # Конвертация в WAV
        wav_path = convert_to_wav(input_path)
        logger.info(f"🎵 Конвертирован в: {wav_path}")

        # Расшифровка и суммаризация
        full_text, summary_text = transcribe_and_summarize(wav_path)

        logger.info(f"📄 Получен полный текст: {full_text}")
        logger.info(f"📝 Получен summary: {summary_text}")

        # PDF генерация
        pdf_path = generate_pdf(full_text)

        # Ответ пользователю
        await update.message.reply_text(
            f"📝 Краткое содержание:\n{summary_text}\n\n📄 PDF с полным текстом прилагается."
        )
        await update.message.reply_document(document=pdf_path)

    except Exception as e:
        logger.exception("❌ Ошибка при обработке аудио:")
        await update.message.reply_text("⚠️ Произошла ошибка при обработке. Попробуйте снова.")



application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_audio))
