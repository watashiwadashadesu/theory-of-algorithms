import pytest
import tempfile
import os
from pathlib import Path
from app.database_sql import BookClubManager
from app.models import Book


@pytest.fixture
def temp_db():
    """Создает временную базу данных для тестов."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name

    # Создаем менеджер с временной БД
    manager = BookClubManager(db_path)

    yield manager

    # Убираем за собой - удаляем временный файл БД
    os.unlink(db_path)


@pytest.fixture
def sample_book():
    """Возвращает образец книги для тестов."""
    return Book(
        title="Тестовая книга",
        author="Тестовый автор",
        year=2023,
        genre="Роман",
        status="В наличии",
        reader=None,
        rating=8.5
    )


@pytest.fixture
def sample_books():
    """Возвращает список образцов книг для тестов."""
    return [
        Book(title="Книга 1", author="Автор 1", year=2020, genre="Фэнтези", status="В наличии", rating=9.0),
        Book(title="Книга 2", author="Автор 2", year=2021, genre="Научная фантастика", status="Читается", rating=8.0),
        Book(title="Книга 3", author="Автор 3", year=2022, genre="Детектив", status="Прочитана", rating=7.5),
    ]