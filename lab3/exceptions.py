"""Общие исключения для приложения."""

class BookError(Exception):
    """Базовое исключение для ошибок, связанных с книгами."""
    pass

class BookValidationError(BookError):
    """Исключение при ошибке валидации данных книги."""
    pass

class BookNotFoundError(BookError):
    """Исключение, если книга не найдена."""
    pass