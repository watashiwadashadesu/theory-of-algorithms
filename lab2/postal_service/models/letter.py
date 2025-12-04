from .base import PostalItem

class Letter(PostalItem):
    """Класс для представления Письма."""

    def __init__(self, distance_km, weight_kg, delivery_type="стандарт", is_registered=False):
        super().__init__("Письмо", distance_km, weight_kg, delivery_type)
        self._is_registered = is_registered

    # Managed property для is_registered
    @property
    def is_registered(self):
        """Является ли письмо заказным."""
        return self._is_registered

    @is_registered.setter
    def is_registered(self, value):
        """Устанавливает статус заказного письма."""
        if not isinstance(value, bool):
            raise ValueError("is_registered должен быть boolean.")
        self._is_registered = value

    def calculate_price(self, calculator):
        """Рассчитывает стоимость письма."""
        price = calculator.calculate_letter(self)
        self.price = price  # Используем property setter
        return price

    # Dunder методы
    def __str__(self):
        base_str = super().__str__()
        reg_status = "Заказное" if self._is_registered else "Обычное"
        return f"{base_str} | {reg_status} | Стоимость: {self.price} руб."

    def __repr__(self):
        base_repr = super().__repr__()
        return f"{base_repr}, registered={self._is_registered})"

    def __add__(self, other):
        """Объединение двух писем (возвращает список)."""
        if not isinstance(other, Letter):
            return NotImplemented
        return [self, other]

    def __len__(self):
        """'Длина' письма - условный показатель."""
        return int(self.weight_kg * 100)  # пример: 0.1кг -> 10

    def get_details(self):
        """Детальная информация о письме."""
        base_details = super().get_details()
        base_details.update({
            'registered': self._is_registered,
            'category': 'document'
        })
        return base_details