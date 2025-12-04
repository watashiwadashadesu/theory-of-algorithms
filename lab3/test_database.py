import pytest
import tempfile
import os
from pathlib import Path
from shared.database import BookClubManager, Book
from shared.exceptions import BookNotFoundError, BookValidationError


class TestBookClubManager:
    """Тесты для менеджера книжного клуба с SQLite."""

    def test_add_and_get_book(self, temp_db: BookClubManager, sample_book):
        """Тест добавления и получения книги."""
        # Добавляем книгу
        added_book = temp_db.add_book(sample_book)

        # Проверяем, что присвоился ID
        assert added_book.id is not None
        assert added_book.id > 0

        # Получаем книгу по ID
        retrieved_book = temp_db.get_book_by_id(added_book.id)

        # Проверяем, что данные совпадают
        assert retrieved_book is not None
        assert retrieved_book.title == sample_book.title
        assert retrieved_book.author == sample_book.author
        assert retrieved_book.year == sample_book.year

    def test_get_all_books(self, temp_db: BookClubManager, sample_books):
        """Тест получения всех книг."""
        # Добавляем несколько книг
        for book in sample_books:
            temp_db.add_book(book)

        # Получаем все книги
        all_books = temp_db.get_all_books()

        # Проверяем количество
        assert len(all_books) == len(sample_books)

        # Проверяем, что названия совпадают
        titles = [book.title for book in all_books]
        expected_titles = [book.title for book in sample_books]
        assert set(titles) == set(expected_titles)

    def test_update_book(self, temp_db: BookClubManager, sample_book):
        """Тест обновления книги."""
        # Добавляем книгу
        added_book = temp_db.add_book(sample_book)
        book_id = added_book.id

        # Обновляем данные
        updates = {
            "title": "Обновленное название",
            "rating": 9.8,
            "status": "Прочитана"
        }

        updated_book = temp_db.update_book(book_id, updates)

        # Проверяем обновления
        assert updated_book is not None
        assert updated_book.title == updates["title"]
        assert updated_book.rating == updates["rating"]
        assert updated_book.status == updates["status"]

        # Старые данные должны сохраниться
        assert updated_book.author == sample_book.author
        assert updated_book.year == sample_book.year

    def test_update_nonexistent_book(self, temp_db: BookClubManager):
        """Тест обновления несуществующей книги."""
        with pytest.raises(BookNotFoundError) as exc_info:
            temp_db.update_book(999, {"title": "Новое название"})

        assert "не найдена" in str(exc_info.value)

    def test_delete_book(self, temp_db: BookClubManager, sample_book):
        """Тест удаления книги."""
        # Добавляем книгу
        added_book = temp_db.add_book(sample_book)
        book_id = added_book.id

        # Проверяем, что книга есть
        assert temp_db.get_book_by_id(book_id) is not None

        # Удаляем книгу
        result = temp_db.delete_book(book_id)

        # Проверяем результат удаления
        assert result is True

        # Проверяем, что книга удалена
        assert temp_db.get_book_by_id(book_id) is None

    def test_delete_nonexistent_book(self, temp_db: BookClubManager):
        """Тест удаления несуществующей книги."""
        with pytest.raises(BookNotFoundError) as exc_info:
            temp_db.delete_book(999)

        assert "не найдена" in str(exc_info.value)

    def test_search_books(self, temp_db: BookClubManager):
        """Тест поиска книг."""
        from datetime import date

        current_year = date.today().year

        # Используем латиницу для надежного тестирования
        books = [
            Book(title="Test Book One", author="Author One",
                 year=current_year - 10, genre="Novel"),
            Book(title="Test Book Two", author="Author Two",
                 year=current_year - 5, genre="Fantasy"),
            Book(title="Another Book", author="Author One",
                 year=current_year - 8, genre="Novel"),
        ]

        for book in books:
            temp_db.add_book(book)

        # Тест 1: Поиск по автору (регистронезависимый)
        author_one_books = temp_db.search_books(author="author one")  # строчными
        assert len(author_one_books) == 2

        # Тест 2: Поиск по части названия (регистронезависимый)
        test_books = temp_db.search_books(title="test")
        assert len(test_books) == 2

        # Тест 3: Поиск по другой части названия
        book_books = temp_db.search_books(title="book")
        assert len(book_books) == 3  # все три книги содержат "book"

        # Тест 4: Поиск по заглавной букве
        test_books_upper = temp_db.search_books(title="Test")  # с заглавной
        assert len(test_books_upper) == 2

        # Тест 5: Поиск по жанру
        novel_books = temp_db.search_books(genre="Novel")
        assert len(novel_books) == 2

        # Тест 6: Комбинированный поиск
        combined_search = temp_db.search_books(author="Author One", genre="Novel")
        assert len(combined_search) == 2

    def test_statistics(self, temp_db: BookClubManager, sample_books):
        """Тест сбора статистики."""
        # Добавляем книги
        for book in sample_books:
            temp_db.add_book(book)

        # Получаем статистику
        stats = temp_db.get_statistics()

        # Отладочный вывод
        print(f"\n📊 Статистика: {stats}")
        print(f"📚 Всего книг: {stats['total_books']}")
        print(f"📈 Статусы: {stats['status_counts']}")

        # Проверяем статистику
        assert stats["total_books"] == len(sample_books)

        # Проверяем подсчет по статусам
        status_counts = stats["status_counts"]

        # Проверяем, что все статусы из sample_books учтены
        expected_statuses = set(book.status for book in sample_books)
        actual_statuses = set(status_counts.keys())

        print(f"✅ Ожидаемые статусы: {expected_statuses}")
        print(f"✅ Фактические статусы: {actual_statuses}")

        # Проверяем, что все статусы присутствуют
        assert expected_statuses == actual_statuses

        # Проверяем подсчет для каждого статуса
        for status in expected_statuses:
            expected_count = sum(1 for book in sample_books if book.status == status)
            actual_count = status_counts.get(status, 0)
            print(f"📊 Статус '{status}': ожидалось {expected_count}, получено {actual_count}")
            assert actual_count == expected_count

        # Дополнительные проверки статистики
        assert "average_rating" in stats
        assert "genre_counts" in stats

        # Проверяем подсчет по жанрам
        genre_counts = stats["genre_counts"]
        expected_genres = set(book.genre for book in sample_books)
        actual_genres = set(genre_counts.keys())

        print(f"📚 Ожидаемые жанры: {expected_genres}")
        print(f"📚 Фактические жанры: {actual_genres}")

        assert expected_genres == actual_genres

    def test_count_books(self, temp_db: BookClubManager, sample_books):
        """Тест подсчета книг."""
        # Изначально 0 книг
        assert temp_db.count_books() == 0

        # Добавляем книги
        for book in sample_books:
            temp_db.add_book(book)

        # Проверяем подсчет (ИСПРАВЛЕНО: вызываем метод который только что добавили)
        assert temp_db.count_books() == len(sample_books)

    def test_add_invalid_book(self, temp_db: BookClubManager):
        """Тест добавления некорректной книги."""
        invalid_book = Book(title="", author="Автор", year=2000)

        with pytest.raises(BookValidationError):
            temp_db.add_book(invalid_book)