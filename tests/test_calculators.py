import pytest
from postal_service.calculators import PriceCalculator
from postal_service.models import Letter, Parcel, Banderol


class TestPriceCalculator:
    """Тесты для класса PriceCalculator."""

    def test_calculator_initialization(self):
        """Тест инициализации калькулятора."""
        calculator = PriceCalculator()
        assert hasattr(calculator, 'BASE_RATE_LETTER')
        assert hasattr(calculator, 'BASE_RATE_PARCEL')
        assert hasattr(calculator, 'BASE_RATE_BANDEROL')

    def test_letter_calculation(self):
        """Тест расчета стоимости письма."""
        calculator = PriceCalculator()
        letter = Letter(distance_km=100, weight_kg=0.1, is_registered=True)

        price = calculator.calculate_letter(letter)

        assert isinstance(price, float)
        assert price > 0
        # Заказное письмо должно стоить дороже обычного
        regular_letter = Letter(100, 0.1, is_registered=False)
        regular_price = calculator.calculate_letter(regular_letter)
        assert price > regular_price

    def test_parcel_calculation(self):
        """Тест расчета стоимости посылки."""
        calculator = PriceCalculator()
        fragile_parcel = Parcel(distance_km=500, weight_kg=2,
                                volume_cubic_cm=3000, is_fragile=True)
        regular_parcel = Parcel(distance_km=500, weight_kg=2,
                                volume_cubic_cm=3000, is_fragile=False)

        fragile_price = calculator.calculate_parcel(fragile_parcel)
        regular_price = calculator.calculate_parcel(regular_parcel)

        assert fragile_price > regular_price  # Хрупкая дороже
        assert fragile_price > 0
        assert regular_price > 0

    def test_banderol_calculation(self):
        """Тест расчета стоимости бандероли."""
        calculator = PriceCalculator()
        small_banderol = Banderol(distance_km=200, weight_kg=0.5, volume_cubic_cm=1000)
        large_banderol = Banderol(distance_km=200, weight_kg=0.5, volume_cubic_cm=6000)

        small_price = calculator.calculate_banderol(small_banderol)
        large_price = calculator.calculate_banderol(large_banderol)

        # Большая бандероль должна стоить дороже (надбавка за объем)
        assert large_price > small_price
        assert small_price > 0
        assert large_price > 0

    def test_delivery_type_impact(self):
        """Тест влияния типа доставки на стоимость."""
        calculator = PriceCalculator()
        standard_letter = Letter(100, 0.1, delivery_type="стандарт")
        express_letter = Letter(100, 0.1, delivery_type="экспресс")

        standard_price = calculator.calculate_letter(standard_letter)
        express_price = calculator.calculate_letter(express_letter)

        assert express_price > standard_price  # Экспресс дороже

    @pytest.mark.parametrize("distance,weight,expected_min", [
        (0, 0.1, 10),  # Минимальная базовая стоимость
        (100, 0.1, 20),  # С учетом расстояния
        (100, 0.5, 21),  # С учетом веса
    ])
    def test_letter_price_ranges(self, distance, weight, expected_min):
        """Параметризованный тест диапазонов цен для писем."""
        calculator = PriceCalculator()
        letter = Letter(distance, weight)
        price = calculator.calculate_letter(letter)
        assert price >= expected_min