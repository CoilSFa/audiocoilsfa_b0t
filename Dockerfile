FROM python:3.10-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    unzip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создание рабочей директории
WORKDIR /app
COPY . .

# ⬇️ Загрузка FreeSans.ttf во время сборки
RUN curl -L -o freefont.zip https://ftp.gnu.org/gnu/freefont/freefont-20120503.zip && \
    unzip freefont.zip -d fonts && \
    cp fonts/freefont-20120503/FreeSans.ttf /app/FreeSans.ttf && \
    rm -rf freefont.zip fonts

# Запуск приложения
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
