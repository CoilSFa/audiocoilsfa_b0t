FROM python:3.10-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копируем исходники
COPY . /app

# Скачиваем FreeSans.ttf (с поддержкой Unicode)
RUN curl -L -o /app/freefont.zip https://ftp.gnu.org/gnu/freefont/freefont-ttf-20120503.zip && \
    unzip /app/freefont.zip -d /app/fonts && \
    cp /app/fonts/freefont-20120503/FreeSans.ttf /app/FreeSans.ttf && \
    rm -rf /app/freefont.zip /app/fonts

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем приложение
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
