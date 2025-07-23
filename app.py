from flask import Flask
import threading
import bot

app = Flask(__name__)

threading.Thread(target=bot.main).start()

@app.route("/")
def home():
    return "Bot is running!", 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
