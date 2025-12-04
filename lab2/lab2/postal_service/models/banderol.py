from .base import PostalItem

class Banderol(PostalItem):
    """Класс для представления Бандероли."""

    def __init__(self, distance_km, weight_kg, volume_cubic_cm, delivery_type="стандарт"):
        super().__init__("Бандероль", distance_km, weight_kg, delivery_type)
        self._volume_cubic_cm = volume_cubic_cm

    # Managed property
    @property
    def volume_cubic_cm(self):
        """Объем бандероли в см³."""
        return self._volume_cubic_cm

    @volume_cubic_cm.setter
    def volume_cubic_cm(self, value):
        """Устанавливает объем с проверкой."""
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Объем должен быть положительным числом.")
        self._volume_cubic_cm = value

    def calculate_price(self, calculator):
        """Рассчитывает стоимость бандероли."""
        price = calculator.calculate_banderol(self)
        self.price = price
        return price

    # Dunder методы
    def __str__(self):
        base_str = super().__str__()
        return f"{base_str} | Объем: {self._volume_cubic_cm}см³ | Стоимость: {self.price} руб."

    def __repr__(self):
        base_repr = super().__repr__()
        return f"{base_repr}, volume={self._volume_cubic_cm})"

    def __contains__(self, item):
        """Проверка, содержится ли значение в свойствах бандероли."""
        return item in [self.name, self.delivery_type, str(self._volume_cubic_cm)]

    def __call__(self, new_volume=None):
        """Вызов объекта как функции для изменения объема."""
        if new_volume is not None:
            old_volume = self._volume_cubic_cm
            self.volume_cubic_cm = new_volume
            return f"Объем изменен с {old_volume}см³ на {new_volume}см³"
        return f"Бандероль: {self._volume_cubic_cm}см³"

    def get_details(self):
        """Детальная информация о бандероли."""
        base_details = super().get_details()
        base_details.update({
            'volume': self._volume_cubic_cm,
            'category': 'banderol'
        })
        return base_details