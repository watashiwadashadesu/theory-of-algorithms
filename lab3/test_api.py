"""
Тесты для API веб-приложения книжного клуба.
"""
import pytest
from fastapi.testclient import TestClient
import tempfile
import os

# Импортируем из shared
from shared.database import BookClubManager

# Импортируем приложение
from web_app.main import app

@pytest.fixture
def client():
    """Создает тестового клиента FastAPI."""
    return TestClient(app)


@pytest.fixture
def temp_db():
    """Создает временную базу данных для тестов."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name

    # Временно изменяем путь к БД в приложении
    original_manager = None

    # Создаем менеджер с временной БД
    manager = BookClubManager(db_path)

    yield manager

    # Убираем за собой
    os.unlink(db_path)


def test_read_root(client):
    """Тест главной страницы."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Книжный клуб" in response.text


def test_add_book_page(client):
    """Тест страницы добавления книги."""
    response = client.get("/books/add")
    assert response.status_code == 200
    assert "Добавить новую книгу" in response.text


def test_get_books_api(client):
    """Тест API для получения книг."""
    response = client.get("/api/books")
    assert response.status_code == 200
    assert "books" in response.json()


def test_create_book_api(client):
    """Тест API для создания книги."""
    response = client.post(
        "/api/books",
        data={
            "title": "Тестовая книга",
            "author": "Тестовый автор",
            "year": "2023",
            "genre": "Роман",
            "status": "В наличии"
        }
    )
    # Должен перенаправить на главную страницу
    assert response.status_code == 303


def test_create_book_api_invalid(client):
    """Тест API для создания книги с невалидными данными."""
    response = client.post(
        "/api/books",
        data={
            "title": "",  # Пустое название - должно вызвать ошибку
            "author": "Автор",
            "year": "2023"
        }
    )
    # Должен вернуть 400 Bad Request
    assert response.status_code == 400


def test_get_stats_api(client):
    """Тест API для получения статистики."""
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "statistics" in data
    assert "total_books" in data["statistics"]