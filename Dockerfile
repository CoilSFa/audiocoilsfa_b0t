# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Скачиваем Unicode-совместимый шрифт
RUN curl -L -o /app/FreeSans.ttf https://github.com/alerque/libertinus/releases/download/v7.040/LibertinusSans-Regular.otf

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт (если нужно для Render)
EXPOSE 10000

# Стартовая команда
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
