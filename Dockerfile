# Используем официальный Python образ
FROM python:3.12-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Создаем пользователя для безопасности
RUN groupadd --gid 1000 django && \
    useradd --uid 1000 --gid django --shell /bin/bash --create-home django

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем код проекта
COPY . .

# Создаем директории для статических файлов
RUN mkdir -p /app/staticfiles /app/media

# Устанавливаем права доступа
RUN chown -R django:django /app

# Переключаемся на пользователя django
USER django

# Открываем порт
EXPOSE 8000

# Команда по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]