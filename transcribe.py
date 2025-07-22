import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def transcribe_audio(file_path: str) -> str:
    with open(file_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
    return transcript["text"]
