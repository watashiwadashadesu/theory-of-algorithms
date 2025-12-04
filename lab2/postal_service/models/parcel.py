from .base import PostalItem

class Parcel(PostalItem):
    """Класс для представления Посылки."""

    def __init__(self, distance_km, weight_kg, volume_cubic_cm, delivery_type="стандарт", is_fragile=False):
        super().__init__("Посылка", distance_km, weight_kg, delivery_type)
        self._volume_cubic_cm = volume_cubic_cm
        self._is_fragile = is_fragile

    # Managed properties
    @property
    def volume_cubic_cm(self):
        """Объем посылки в см³."""
        return self._volume_cubic_cm

    @volume_cubic_cm.setter
    def volume_cubic_cm(self, value):
        """Устанавливает объем с проверкой."""
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Объем должен быть положительным числом.")
        self._volume_cubic_cm = value

    @property
    def is_fragile(self):
        """Является ли посылка хрупкой."""
        return self._is_fragile

    @is_fragile.setter
    def is_fragile(self, value):
        """Устанавливает статус хрупкости."""
        if not isinstance(value, bool):
            raise ValueError("is_fragile должен быть boolean.")
        self._is_fragile = value

    def calculate_price(self, calculator):
        """Рассчитывает стоимость посылки."""
        price = calculator.calculate_parcel(self)
        self.price = price
        return price

    # Dunder методы
    def __str__(self):
        base_str = super().__str__()
        fragile_status = "Хрупкая" if self._is_fragile else "Обычная"
        return f"{base_str} | Объем: {self._volume_cubic_cm}см³ | {fragile_status} | Стоимость: {self.price} руб."

    def __repr__(self):
        base_repr = super().__repr__()
        return f"{base_repr}, volume={self._volume_cubic_cm}, fragile={self._is_fragile})"

    def __mul__(self, quantity):
        """Создание нескольких одинаковых посылок."""
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Количество должно быть положительным целым числом.")
        return [Parcel(self.distance_km, self.weight_kg, self._volume_cubic_cm,
                      self.delivery_type, self._is_fragile) for _ in range(quantity)]

    def __getitem__(self, key):
        """Доступ к свойствам как к элементам словаря."""
        properties = {
            'distance': self.distance_km,
            'weight': self.weight_kg,
            'volume': self._volume_cubic_cm,
            'fragile': self._is_fragile
        }
        return properties.get(key, None)

    def get_details(self):
        """Детальная информация о посылке."""
        base_details = super().get_details()
        base_details.update({
            'volume': self._volume_cubic_cm,
            'fragile': self._is_fragile,
            'category': 'package'
        })
        return base_details
