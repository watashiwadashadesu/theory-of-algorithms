import pytest
from datetime import date
from app.models import Book
from app.exceptions import BookValidationError


class TestBookModel:
    """Тесты для модели Book."""

    def test_book_creation(self):
        """Тест создания объекта Book."""
        book = Book(
            title="1984",
            author="Джордж Оруэлл",
            year=1949,
            genre="Антиутопия",
            status="Прочитана",
            rating=9.5
        )

        assert book.title == "1984"
        assert book.author == "Джордж Оруэлл"
        assert book.year == 1949
        assert book.genre == "Антиутопия"
        assert book.rating == 9.5

    def test_book_validation_success(self):
        """Тест успешной валидации книги."""
        book = Book(
            title="Властелин колец",
            author="Дж. Р. Р. Толкин",
            year=1954,
            rating=10.0
        )

        # Не должно вызывать исключений
        book.validate()

    def test_book_validation_empty_title(self):
        """Тест валидации с пустым названием."""
        book = Book(title="", author="Автор", year=2000)

        with pytest.raises(BookValidationError) as exc_info:
            book.validate()

        assert "Название книги не может быть пустым" in str(exc_info.value)

    def test_book_validation_empty_author(self):
        """Тест валидации с пустым автором."""
        book = Book(title="Книга", author="", year=2000)

        with pytest.raises(BookValidationError) as exc_info:
            book.validate()

        assert "Автор не может быть пустым" in str(exc_info.value)

    def test_book_validation_invalid_year(self):
        """Тест валидации с некорректным годом."""
        # Год в прошлом
        book = Book(title="Книга", author="Автор", year=1899)

        with pytest.raises(BookValidationError) as exc_info:
            book.validate()

        assert "Год издания должен быть между" in str(exc_info.value)

        # Год в будущем (более чем на 2 года вперед)
        future_year = date.today().year + 3
        book = Book(title="Книга", author="Автор", year=future_year)

        with pytest.raises(BookValidationError) as exc_info:
            book.validate()

    def test_book_validation_invalid_rating(self):
        """Тест валидации с некорректным рейтингом."""
        book = Book(title="Книга", author="Автор", year=2000, rating=11.0)

        with pytest.raises(BookValidationError) as exc_info:
            book.validate()

        assert "Рейтинг должен быть от 0 до 10" in str(exc_info.value)

        # Отрицательный рейтинг
        book.rating = -1.0
        with pytest.raises(BookValidationError):
            book.validate()

    def test_book_str_representation(self):
        """Тест строкового представления книги."""
        book = Book(title="Гарри Поттер", author="Дж. К. Роулинг", year=1997)

        expected = "Гарри Поттер (Дж. К. Роулинг, 1997)"
        assert str(book) == expected