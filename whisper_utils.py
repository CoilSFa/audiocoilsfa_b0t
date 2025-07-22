import os
import tempfile
from telegram import Update
from telegram.ext import ContextTypes
import torch
import whisper

model = whisper.load_model("base")

async def transcribe_voice(update: Update, context: ContextTypes.DEFAULT_TYPE, is_voice=True):
    file = await (update.message.voice.get_file() if is_voice else update.message.audio.get_file())
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as f:
        await file.download_to_drive(custom_path=f.name)
        result = model.transcribe(f.name)
    return result["text"]