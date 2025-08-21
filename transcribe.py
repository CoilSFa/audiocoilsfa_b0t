import os
import tempfile
import subprocess

from config import AUDIO_DIR, TEXT_DIR

# Функция для транскрибации аудио через Whisper (локально или openai-whisper)
def transcribe_audio(file_path: str) -> str:
    """
    Принимает путь до аудиофайла и возвращает текст.
    Если Whisper не установлен, функция просто возвращает тестовый текст.
    """
    try:
        import whisper
        model = whisper.load_model("base")  # можно "small" или "medium"
        result = model.transcribe(file_path, language="ru")
        text = result["text"]
    except Exception as e:
        text = f"[Ошибка транскрибации: {e}]"

    # Сохраним результат в файл
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    text_file = os.path.join(TEXT_DIR, f"{base_name}.txt")

    with open(text_file, "w", encoding="utf-8") as f:
        f.write(text)

    return text
