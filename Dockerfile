# Используем официальный образ Python 3.10
FROM python:3.10-slim

# Устанавливаем ffmpeg — он нужен для работы pydub
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и код
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Указываем порт (Render по умолчанию использует PORT из env)
ENV PORT=10000

# Запускаем FastAPI через uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
