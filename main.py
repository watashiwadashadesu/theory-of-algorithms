"""
Точка входа в приложение PRF Constructor.

Запускает главное окно приложения.
"""

import sys
import os

# Увеличиваем лимит рекурсии Python для вычисления больших факториалов
sys.setrecursionlimit(50000)

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow


def main():
    """Главная функция приложения."""
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

