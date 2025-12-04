import pytest
from postal_service.models import Letter, Parcel, Banderol, PostalItem


class TestPostalItem:
    """Тесты для базового класса PostalItem."""

    def test_abstract_class_cannot_be_instantiated(self):
        """Абстрактный класс нельзя инстанциировать."""
        with pytest.raises(TypeError):
            item = PostalItem("Test", 100, 1)

    def test_instances_counter(self, sample_letter, sample_parcel):
        """Тест счетчика созданных объектов."""
        # Счетчик увеличивается при создании каждого объекта
        initial_count = PostalItem.get_instances_count()

        new_letter = Letter(50, 0.2)
        new_parcel = Parcel(100, 1, 2000)

        assert PostalItem.get_instances_count() == initial_count + 2

    def test_managed_properties(self, sample_letter):
        """Тест managed properties."""
        # Property price до расчета
        with pytest.raises(ValueError, match="Цена еще не была рассчитана"):
            _ = sample_letter.price

        # Property id (read-only)
        assert hasattr(sample_letter, 'id')
        with pytest.raises(AttributeError):
            sample_letter.id = 999  # Нельзя изменить


class TestLetter:
    """Тесты для класса Letter."""

    def test_letter_creation(self, sample_letter):
        """Тест создания письма."""
        assert sample_letter.name == "Письмо"
        assert sample_letter.distance_km == 100
        assert sample_letter.weight_kg == 0.1
        assert sample_letter.is_registered == True

    def test_letter_managed_properties(self):
        """Тест managed properties письма."""
        letter = Letter(50, 0.2)

        # is_registered property
        assert letter.is_registered == False  # по умолчанию

        letter.is_registered = True
        assert letter.is_registered == True

        with pytest.raises(ValueError):
            letter.is_registered = "not_a_boolean"

    def test_letter_dunder_methods(self, sample_letter, price_calculator):
        """Тест dunder методов письма."""
        sample_letter.calculate_price(price_calculator)

        # __str__
        assert "Письмо" in str(sample_letter)
        assert "Заказное" in str(sample_letter)

        # __repr__
        assert "Letter" in repr(sample_letter)
        assert "id=" in repr(sample_letter)

        # __eq__
        same_letter = Letter(100, 0.1, is_registered=True)
        different_letter = Letter(50, 0.2)
        assert sample_letter != same_letter  # разные ID
        assert sample_letter != different_letter

        # __add__
        letter2 = Letter(50, 0.2)
        combined = sample_letter + letter2
        assert isinstance(combined, list)
        assert len(combined) == 2

        # __len__
        assert len(sample_letter) == 10  # 0.1кг * 100

    def test_letter_price_calculation(self, sample_letter, price_calculator):
        """Тест расчета цены письма."""
        price = sample_letter.calculate_price(price_calculator)

        assert isinstance(price, float)
        assert price > 0
        assert sample_letter.price == price  # Проверка property


class TestParcel:
    """Тесты для класса Parcel."""

    def test_parcel_creation(self, sample_parcel):
        """Тест создания посылки."""
        assert sample_parcel.name == "Посылка"
        assert sample_parcel.volume_cubic_cm == 3000
        assert sample_parcel.is_fragile == True

    def test_parcel_managed_properties(self):
        """Тест managed properties посылки."""
        parcel = Parcel(100, 1, 2000)

        # volume property
        parcel.volume_cubic_cm = 2500
        assert parcel.volume_cubic_cm == 2500

        with pytest.raises(ValueError):
            parcel.volume_cubic_cm = -100

        # is_fragile property
        parcel.is_fragile = False
        assert parcel.is_fragile == False

    def test_parcel_dunder_methods(self, sample_parcel, price_calculator):
        """Тест dunder методов посылки."""
        sample_parcel.calculate_price(price_calculator)

        # __str__
        assert "Посылка" in str(sample_parcel)
        assert "Хрупкая" in str(sample_parcel)

        # __mul__
        multiple_parcels = sample_parcel * 3
        assert isinstance(multiple_parcels, list)
        assert len(multiple_parcels) == 3

        # __getitem__
        assert sample_parcel['distance'] == 500
        assert sample_parcel['weight'] == 2
        assert sample_parcel['fragile'] == True
        assert sample_parcel['nonexistent'] is None

    def test_parcel_comparison(self, sample_parcel, price_calculator):
        """Тест сравнения посылок."""
        cheap_parcel = Parcel(50, 0.5, 1000, is_fragile=False)

        sample_parcel.calculate_price(price_calculator)
        cheap_parcel.calculate_price(price_calculator)

        # __lt__
        assert cheap_parcel < sample_parcel


class TestBanderol:
    """Тесты для класса Banderol."""

    def test_banderol_creation(self, sample_banderol):
        """Тест создания бандероли."""
        assert sample_banderol.name == "Бандероль"
        assert sample_banderol.volume_cubic_cm == 1000

    def test_banderol_dunder_methods(self, sample_banderol):
        """Тест dunder методов бандероли."""
        # __contains__
        assert "Бандероль" in sample_banderol
        assert "стандарт" in sample_banderol
        assert "1000" in sample_banderol
        assert "несуществующее" not in sample_banderol

        # __call__
        result = sample_banderol()
        assert "Бандероль" in result

        result = sample_banderol(1500)
        assert "изменен" in result
        assert sample_banderol.volume_cubic_cm == 1500

    def test_banderol_price_calculation(self, sample_banderol, price_calculator):
        """Тест расчета цены бандероли."""
        price = sample_banderol.calculate_price(price_calculator)

        assert isinstance(price, float)
        assert price > 0
        # Проверяем, что цена сохранилась в property
        assert hasattr(sample_banderol, '_calculated_price')
        assert sample_banderol.price == price