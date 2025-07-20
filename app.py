from flask import Flask
import threading
import bot  # Импорт файла bot.py

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!", 200

# Запуск бота в отдельном потоке
threading.Thread(target=bot.main).start()
