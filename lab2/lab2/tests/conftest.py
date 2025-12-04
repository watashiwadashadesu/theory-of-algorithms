import pytest
import sys
import os

# Добавляем корневую папку проекта в путь Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from postal_service.models import Letter, Parcel, Banderol
from postal_service.calculators import PriceCalculator

@pytest.fixture
def price_calculator():
    """Фикстура для калькулятора цен."""
    return PriceCalculator()

@pytest.fixture
def sample_letter():
    """Фикстура для тестового письма."""
    return Letter(distance_km=100, weight_kg=0.1, is_registered=True)

@pytest.fixture
def sample_parcel():
    """Фикстура для тестовой посылки."""
    return Parcel(distance_km=500, weight_kg=2, volume_cubic_cm=3000, is_fragile=True)

@pytest.fixture
def sample_banderol():
    """Фикстура для тестовой бандероли."""
    return Banderol(distance_km=200, weight_kg=0.5, volume_cubic_cm=1000)