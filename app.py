from flask import Flask
import asyncio
import threading
from bot import main as telegram_main

app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Бот работает!"

def run_bot():
    asyncio.run(telegram_main())

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
