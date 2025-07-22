from fastapi import FastAPI, Request
from bot import application
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "bot is running"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    # 👇 Инициализируем, если еще не было
    if not application._initialized:
        await application.initialize()

    await application.process_update(data)
    return {"ok": True}
