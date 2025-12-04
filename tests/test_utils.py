import pytest
import os
import tempfile
from postal_service.models import Letter, Parcel, Banderol
from postal_service.calculators import PriceCalculator
from postal_service.utils import save_to_excel


class TestReporter:
    """Тесты для утилит отчетов."""

    def test_excel_creation(self, sample_letter, sample_parcel, sample_banderol, price_calculator):
        """Тест создания Excel отчета."""
        # Рассчитываем цены
        sample_letter.calculate_price(price_calculator)
        sample_parcel.calculate_price(price_calculator)
        sample_banderol.calculate_price(price_calculator)

        items = [sample_letter, sample_parcel, sample_banderol]

        # Создаем временный файл
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
            filename = tmp_file.name

        try:
            # Сохраняем отчет
            save_to_excel(items, filename)

            # Проверяем, что файл создан
            assert os.path.exists(filename)
            assert os.path.getsize(filename) > 0

        finally:
            # Удаляем временный файл
            if os.path.exists(filename):
                os.unlink(filename)

    def test_empty_list_handling(self):
        """Тест обработки пустого списка отправлений."""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
            filename = tmp_file.name

        try:
            save_to_excel([], filename)
            assert os.path.exists(filename)
        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    def test_invalid_filename(self, sample_letter, price_calculator):
        """Тест обработки невалидного имени файла."""
        sample_letter.calculate_price(price_calculator)

        with pytest.raises(Exception):  # Может быть разное исключение
            save_to_excel([sample_letter], "/invalid/path/report.xlsx")