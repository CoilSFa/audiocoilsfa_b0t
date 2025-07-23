# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем зависимости: ffmpeg, curl, unzip
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Скачиваем DejaVuSans.ttf и кладём его в /app
RUN curl -L -o dejavu.zip https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip && \
    unzip dejavu.zip && \
    cp dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf /app/DejaVuSans.ttf && \
    rm -rf dejavu.zip dejavu-fonts-ttf-2.37

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запуск приложения (проверь, если запускается через uvicorn или python)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
