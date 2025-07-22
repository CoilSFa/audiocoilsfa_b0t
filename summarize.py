import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def summarize_text(text: str) -> str:
    prompt = (
        "Выдели ключевые темы и кратко поясни их для следующего текста:\n\n"
        f"{text}\n\nОтвет:"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message["content"]
