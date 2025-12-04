#!/usr/bin/env python3
"""
Скрипт для запуска десктопного приложения книжного клуба.
"""
import sys
import argparse
from PySide6.QtWidgets import QApplication
from app.views.main_window import MainWindow
from shared.database import BookClubManager


def parse_args():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description="Десктопное приложение книжного клуба")
    parser.add_argument(
        "--db",
        default="book_club.db",
        help="Путь к файлу базы данных SQLite (по умолчанию: book_club.db)"
    )
    return parser.parse_args()


def main():
    """Основная функция запуска десктопного приложения."""
    args = parse_args()

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Создаем менеджер БД
    manager = BookClubManager(args.db)
    print(f"Используется база данных: {args.db}")

    # Передаем менеджер в главное окно
    # Нужно обновить MainWindow чтобы он принимал manager
    window = MainWindow(manager)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()