# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем системные зависимости для Tkinter и Graphviz
RUN apt-get update && apt-get install -y \
    python3-tk \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем точку монтирования для базы данных
VOLUME /app/data

# Запускаем приложение
CMD ["python", "main.py"]