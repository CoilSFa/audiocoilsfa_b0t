import os
import openai
from pydub import AudioSegment

openai.api_key = os.getenv("OPENAI_API_KEY")

def split_audio(path, chunk_length_ms=30000):
    audio = AudioSegment.from_wav(path)
    chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    chunk_paths = []
    for i, chunk in enumerate(chunks):
        chunk_path = f"{path}_chunk{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)
    return chunk_paths

def transcribe_and_summarize(path: str) -> tuple[str, str]:
    chunk_paths = split_audio(path)
    print(f"[INFO] Аудио разделено на {len(chunk_paths)} фрагментов")

    full_text = ""
    for chunk_path in chunk_paths:
        with open(chunk_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            full_text += transcript.text + "\n"
        os.remove(chunk_path)

    summary = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Сделай краткое содержание следующего текста:\n\n{full_text}"}],
        max_tokens=800
    )
    return summary.choices[0].message.content.strip(), full_text
