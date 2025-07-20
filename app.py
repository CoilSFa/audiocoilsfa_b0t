from flask import Flask
import threading
import bot  # Импортирует твой файл bot.py

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!", 200

# Запускает бота в фоне
threading.Thread(target=bot.main).start()
