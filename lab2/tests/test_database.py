import pytest
import os
import tempfile
import sys

# Добавляем путь к проекту
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from postal_service.database import DatabaseManager
from postal_service.models import Letter, Parcel, Banderol
from postal_service.calculators import PriceCalculator


class TestDatabase:
    """Тесты для работы с базой данных."""

    @pytest.fixture
    def temp_db(self):
        """Создает временную базу данных для тестов."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            db_path = tmp_file.name

        db = DatabaseManager(db_path)
        yield db

        # Очистка после тестов
        if os.path.exists(db_path):
            os.unlink(db_path)

    @pytest.fixture
    def sample_items(self, price_calculator):
        """Создает тестовые объекты."""
        letter = Letter(100, 0.1, is_registered=True)
        parcel = Parcel(500, 2, 3000, is_fragile=True)
        banderol = Banderol(200, 0.5, 1000)

        # Рассчитываем цены
        letter.calculate_price(price_calculator)
        parcel.calculate_price(price_calculator)
        banderol.calculate_price(price_calculator)

        return [letter, parcel, banderol]

    def test_database_initialization(self, temp_db):
        """Тест инициализации базы данных."""
        # Проверяем, что база создана и таблицы существуют
        assert os.path.exists(temp_db.db_path)

    def test_save_postal_item(self, temp_db, sample_items):
        """Тест сохранения отправления в базу данных."""
        for item in sample_items:
            item_id = temp_db.save_postal_item(item)
            assert item_id is not None
            assert item_id > 0

    def test_get_all_items(self, temp_db, sample_items):
        """Тест получения всех отправлений."""
        # Сохраняем тестовые данные
        for item in sample_items:
            temp_db.save_postal_item(item)

        # Получаем все записи
        items = temp_db.get_all_items()

        assert len(items) == len(sample_items)
        assert all(isinstance(item, dict) for item in items)

    def test_get_items_by_type(self, temp_db, sample_items):
        """Тест получения отправлений по типу."""
        # Сохраняем тестовые данные
        for item in sample_items:
            temp_db.save_postal_item(item)

        # Получаем только письма
        letters = temp_db.get_items_by_type("Письмо")

        assert len(letters) == 1
        assert letters[0]['item_type'] == "Письмо"

    def test_get_total_statistics(self, temp_db, sample_items):
        """Тест получения статистики."""
        # Сохраняем тестовые данные
        for item in sample_items:
            temp_db.save_postal_item(item)

        stats = temp_db.get_total_statistics()

        assert stats['total_count'] == len(sample_items)
        assert stats['total_cost'] > 0
        assert 'Письмо' in stats['type_counts']
        assert 'Посылка' in stats['type_counts']
        assert 'Бандероль' in stats['type_counts']

    def test_clear_database(self, temp_db, sample_items):
        """Тест очистки базы данных."""
        # Сохраняем тестовые данные
        for item in sample_items:
            temp_db.save_postal_item(item)

        # Проверяем, что данные есть
        assert len(temp_db.get_all_items()) == len(sample_items)

        # Очищаем базу
        temp_db.clear_database()

        # Проверяем, что данные удалены
        assert len(temp_db.get_all_items()) == 0