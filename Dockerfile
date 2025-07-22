# Используем официальный образ Python 3.10
FROM python:3.10-slim

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы проекта
COPY . .

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir pydub==0.24.1

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Указываем команду запуска
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
