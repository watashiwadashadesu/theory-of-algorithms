# Лабораторная работа №1
Введение в язык программирования python

## Описание

Репозиторий содержит решения 11 заданий по курсу "Теория алгоритмов".  
Каждое задание оформлено как отдельный модуль в папке `lab1/tasks/`.  
Верхнеуровневый модуль `main.py` позволяет запускать задачи централизованно.

## Установка и запуск

1. **Клонируйте репозиторий:**  
   ```bash
   git clone https://github.com/watashiwadashadesu/theory-of-algorithms.git
   cd theory-of-algorithms
   
2. **Создайте виртуальное окружение и установите зависимости:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    # или .venv\Scripts\activate  # Windows
    pip install -r requirements.txt

3. **Запуск всех заданий:**
    ```bash
    python main.py
   
4. **Запуск отдельных заданий:**
    ```bash
    python tasks/circle.py
    python tasks/distance.py
    # и т.д.

5. **Запуск всех тестов:**
    ```bash
    python -m pytest lab1/tests/tests.py -v