FROM python:3.10-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y fonts-dejavu-core

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Рабочая директория
WORKDIR /app

# Копируем всё, включая шрифт
COPY . .

# Убедись, что FreeSans.ttf лежит в корне проекта
# или путь укажи соответствующий в pdf_generator.py
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
