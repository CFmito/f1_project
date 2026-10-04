# Используем официальный образ Python
FROM python:3.11-slim

# Задаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код проекта в контейнер
COPY . .

# Открываем порт (например, 8000 для FastAPI/Uvicorn)
EXPOSE 8000

# Команда для запуска приложения (замените main:app на ваш файл и переменную)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]