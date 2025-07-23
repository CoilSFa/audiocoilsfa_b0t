FROM python:3.10-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    tar \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создание рабочей директории
WORKDIR /app
COPY . .

# ⬇️ Загрузка FreeSans.ttf из tar.gz (рабочий источник)
RUN curl -L -o freefont.tar.gz https://ftp.gnu.org/gnu/freefont/freefont-ttf-20120503.tar.gz && \
    tar -xzf freefont.tar.gz && \
    cp freefont-ttf-20120503/FreeSans.ttf /app/FreeSans.ttf && \
    rm -rf freefont.tar.gz freefont-ttf-20120503

# Запуск
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
