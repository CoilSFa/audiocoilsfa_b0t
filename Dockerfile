# Используем официальный образ Python 3.10
FROM python:3.10-slim

# Устанавливаем системные зависимости (включая unzip, ffmpeg и wget)
RUN apt-get update && \
    apt-get install -y ffmpeg curl tar && \
    apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app

# Скачиваем FreeSans.ttf и помещаем в рабочую директорию
RUN apt-get update && apt-get install -y unzip curl && \
    curl -L -o freefont.zip https://ftp.gnu.org/gnu/freefont/freefont-ttf-20120503.zip && \
    unzip freefont.zip && \
    cp freefont-20120503/FreeSans.ttf /app/FreeSans.ttf
    rm -rf freefont.zip freefont-ttf-20120503

# Копируем все файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pydub==0.24.1

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Команда запуска приложения
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
