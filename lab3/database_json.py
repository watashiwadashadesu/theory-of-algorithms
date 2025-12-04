import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from .models import Book
from .exceptions import BookNotFoundError

# Настройка логирования активности
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
log_file = LOG_DIR / f"book_club_{datetime.now().strftime('%Y%m')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()  # Также выводим в консоль
    ]
)
logger = logging.getLogger(__name__)


class BookClubManager:
    """Класс для управления данными книжного клуба."""

    def __init__(self, data_file: str = "books_data.json"):
        self._books: List[Book] = []
        self._next_id = 1
        self.data_file = Path(data_file)
        self._load_from_file()

    def _load_from_file(self):
        """Загружает книги из JSON-файла, если он существует."""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        book = Book(**item)
                        self._books.append(book)
                        if book.id and book.id >= self._next_id:
                            self._next_id = book.id + 1
                logger.info(f"Загружено {len(self._books)} книг из файла.")
            except Exception as e:
                logger.error(f"Ошибка загрузки данных: {e}")
                self._books = []

    def _save_to_file(self):
        """Сохраняет книги в JSON-файл."""
        try:
            data = [book.__dict__ for book in self._books]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info("Данные книг сохранены в файл.")
        except Exception as e:
            logger.error(f"Ошибка сохранения данных: {e}")

    def get_all_books(self) -> List[Book]:
        """Возвращает список всех книг."""
        return self._books.copy()

    def add_book(self, book: Book) -> Book:
        """Добавляет новую книгу в клуб."""
        book.validate()
        book.id = self._next_id
        self._next_id += 1
        self._books.append(book)
        self._save_to_file()
        logger.info(f"Добавлена книга: {book}")
        return book

    def update_book(self, book_id: int, updated_data: dict) -> Optional[Book]:
        """Обновляет данные книги по ID."""
        for i, book in enumerate(self._books):
            if book.id == book_id:
                # Обновляем только переданные поля
                for key, value in updated_data.items():
                    if hasattr(book, key):
                        setattr(book, key, value)
                book.validate()
                self._books[i] = book
                self._save_to_file()
                logger.info(f"Обновлена книга ID {book_id}: {book}")
                return book
        logger.warning(f"Не найдена книга для обновления с ID {book_id}")
        raise BookNotFoundError(f"Книга с ID {book_id} не найдена.")

    def delete_book(self, book_id: int) -> bool:
        """Удаляет книгу по ID."""
        for i, book in enumerate(self._books):
            if book.id == book_id:
                deleted_book = self._books.pop(i)
                self._save_to_file()
                logger.info(f"Удалена книга: {deleted_book}")
                return True
        logger.warning(f"Попытка удалить несуществующую книгу с ID {book_id}")
        raise BookNotFoundError(f"Книга с ID {book_id} не найдена.")

    def get_books_statistics(self) -> dict:
        """Собирает статистику по книгам для графика."""
        if not self._books:
            return {}

        status_counts = {}
        genre_counts = {}
        ratings = []

        for book in self._books:
            # Статистика по статусам
            status_counts[book.status] = status_counts.get(book.status, 0) + 1
            # Статистика по жанрам
            genre_counts[book.genre] = genre_counts.get(book.genre, 0) + 1
            # Сбор рейтингов для среднего
            if book.rating is not None:
                ratings.append(book.rating)

        avg_rating = sum(ratings) / len(ratings) if ratings else 0

        return {
            "status_counts": status_counts,
            "genre_counts": genre_counts,
            "total_books": len(self._books),
            "average_rating": round(avg_rating, 2)
        }