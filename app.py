from flask import Flask
import asyncio
from bot import main

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!", 200

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())  # запускаем бота как корутину
    app.run(host="0.0.0.0", port=10000)
