"""
Общий модуль для работы с базой данных.
Используется и в десктопном, и в веб-приложении.
"""
import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import contextmanager
from dataclasses import dataclass

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Book:
    """Класс, представляющий книгу в клубе."""
    id: Optional[int] = None
    title: str = ""
    author: str = ""
    year: int = 1900
    genre: str = "Роман"
    status: str = "В наличии"
    reader: Optional[str] = None
    rating: Optional[float] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def validate(self):
        """Проверяет корректность данных книги."""
        from datetime import date
        from .exceptions import BookValidationError

        if not self.title.strip():
            raise BookValidationError("Название книги не может быть пустым.")
        if not self.author.strip():
            raise BookValidationError("Автор не может быть пустым.")
        if not (1900 <= self.year <= date.today().year + 2):
            raise BookValidationError(f"Год издания должен быть между 1900 и {date.today().year + 2}.")
        if self.rating is not None and not (0 <= self.rating <= 10):
            raise BookValidationError("Рейтинг должен быть от 0 до 10.")

    def to_dict(self):
        """Преобразует книгу в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre,
            "status": self.status,
            "reader": self.reader,
            "rating": self.rating,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __str__(self):
        return f"{self.title} ({self.author}, {self.year})"


class DatabaseConnection:
    """Менеджер подключения к базе данных SQLite."""

    def __init__(self, db_path: str = "book_club.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self):
        """Инициализирует базу данных и создает таблицы, если их нет."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    genre TEXT DEFAULT 'Роман',
                    status TEXT DEFAULT 'В наличии',
                    reader TEXT,
                    rating REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS update_books_timestamp 
                AFTER UPDATE ON books
                BEGIN
                    UPDATE books 
                    SET updated_at = CURRENT_TIMESTAMP 
                    WHERE id = NEW.id;
                END;
            """)

            conn.commit()
            logger.info(f"База данных инициализирована: {self.db_path}")

    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для получения соединения с БД."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()


class BookClubManager:
    """Класс для управления данными книжного клуба."""

    def __init__(self, db_path: str = "book_club.db"):
        self.db = DatabaseConnection(db_path)
        logger.info(f"Менеджер книжного клуба инициализирован с БД: {db_path}")

    def count_books(self) -> int:
        """Возвращает общее количество книг."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM books")
            result = cursor.fetchone()
            return result['count'] if result else 0

    def _row_to_book(self, row: sqlite3.Row) -> Book:
        """Преобразует строку БД в объект Book."""
        return Book(
            id=row['id'],
            title=row['title'],
            author=row['author'],
            year=row['year'],
            genre=row['genre'],
            status=row['status'],
            reader=row['reader'],
            rating=row['rating'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )

    def get_all_books(self) -> List[Book]:
        """Возвращает список всех книг."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books ORDER BY title")
            rows = cursor.fetchall()
            return [self._row_to_book(row) for row in rows]

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Возвращает книгу по ID."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
            row = cursor.fetchone()
            return self._row_to_book(row) if row else None

    def add_book(self, book: Book) -> Book:
        """Добавляет новую книгу в клуб."""
        book.validate()

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO books (title, author, year, genre, status, reader, rating)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (book.title, book.author, book.year, book.genre,
                  book.status, book.reader, book.rating))

            book.id = cursor.lastrowid

            # Получаем полную запись с timestamp
            cursor.execute("SELECT * FROM books WHERE id = ?", (book.id,))
            row = cursor.fetchone()

            logger.info(f"Добавлена книга: {book.title}")
            return self._row_to_book(row)

    def update_book(self, book_id: int, updated_data: dict) -> Book:
        """Обновляет данные книги по ID."""
        from .exceptions import BookNotFoundError

        existing_book = self.get_book_by_id(book_id)
        if not existing_book:
            raise BookNotFoundError(f"Книга с ID {book_id} не найдена.")

        # Создаем временный объект для валидации
        temp_book = Book(**{**existing_book.__dict__, **updated_data})
        temp_book.validate()

        # Формируем SQL запрос
        set_clause = ", ".join([f"{key} = ?" for key in updated_data.keys()])
        values = list(updated_data.values())
        values.append(book_id)

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE books 
                SET {set_clause}
                WHERE id = ?
            """, values)

            if cursor.rowcount == 0:
                raise BookNotFoundError(f"Книга с ID {book_id} не найдена.")

            logger.info(f"Обновлена книга ID {book_id}")

            # ОБЯЗАТЕЛЬНО: получаем обновленную книгу
            cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_book(row)
            else:
                raise BookNotFoundError(f"Книга с ID {book_id} не найдена после обновления.")

    def delete_book(self, book_id: int) -> bool:
        """Удаляет книгу по ID."""
        from .exceptions import BookNotFoundError

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM books WHERE id = ?", (book_id,))
            row = cursor.fetchone()

            if not row:
                raise BookNotFoundError(f"Книга с ID {book_id} не найдена.")

            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))

            if cursor.rowcount > 0:
                logger.info(f"Удалена книга: {row['title']}")
                return True

            return False

    def search_books(self, **filters) -> List[Book]:
        """Ищет книги по заданным критериям."""
        if not filters:
            return self.get_all_books()

        query = "SELECT * FROM books WHERE "
        conditions = []
        values = []

        for key, value in filters.items():
            if value is not None:
                if key == 'title' or key == 'author':
                    conditions.append(f"{key} LIKE ?")
                    values.append(f"%{value}%")
                else:
                    conditions.append(f"{key} = ?")
                    values.append(value)

        if not conditions:
            return self.get_all_books()

        query += " AND ".join(conditions) + " ORDER BY title"

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            rows = cursor.fetchall()

            # Фильтруем результаты для регистронезависимого поиска
            filtered_rows = []
            for row in rows:
                match = True
                for key, value in filters.items():
                    if value and key in ['title', 'author']:
                        row_value = row[key] if row[key] else ""
                        if value.lower() not in row_value.lower():
                            match = False
                            break
                if match:
                    filtered_rows.append(row)

            return [self._row_to_book(row) for row in filtered_rows]

    def get_statistics(self) -> dict:
        """Собирает статистику по книгам."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            # Статистика по статусам
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM books 
                GROUP BY status
            """)
            status_rows = cursor.fetchall()
            status_counts = {row['status']: row['count'] for row in status_rows}

            # Статистика по жанрам
            cursor.execute("""
                SELECT genre, COUNT(*) as count 
                FROM books 
                GROUP BY genre
            """)
            genre_rows = cursor.fetchall()
            genre_counts = {row['genre']: row['count'] for row in genre_rows}

            # Общая статистика
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_books,
                    AVG(rating) as avg_rating,
                    MIN(year) as oldest_year,
                    MAX(year) as newest_year
                FROM books
            """)
            stats = cursor.fetchone()

            return {
                "status_counts": status_counts,
                "genre_counts": genre_counts,
                "total_books": stats['total_books'] or 0,
                "average_rating": round(stats['avg_rating'] or 0, 2),
                "oldest_year": stats['oldest_year'],
                "newest_year": stats['newest_year']
            }