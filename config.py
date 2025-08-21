import os

# Токен бота (лучше хранить как переменную окружения)
BOT_TOKEN = os.getenv("BOT_TOKEN", "ВАШ_ТОКЕН_БОТА")

# URL для вебхука
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://audiocoilsfa-b0t.onrender.com/webhook")

# Папки для хранения
AUDIO_DIR = "audio"
TEXT_DIR = "texts"

# Создание папок при запуске
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)
