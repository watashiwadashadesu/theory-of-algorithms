from abc import ABC, abstractmethod


class PostalItem(ABC):
    """Абстрактный базовый класс для всех почтовых отправлений."""

    # Managed-атрибут: счетчик созданных объектов
    _instances_count = 0

    def __init__(self, name, distance_km, weight_kg, delivery_type="стандарт"):
        self.name = name
        self.distance_km = distance_km
        self.weight_kg = weight_kg
        self.delivery_type = delivery_type
        self._calculated_price = None

        # Увеличиваем счетчик при создании каждого объекта
        PostalItem._instances_count += 1
        self._id = PostalItem._instances_count  # Уникальный ID для каждого объекта

    # Managed property (геттер) для ID
    @property
    def id(self):
        """Уникальный идентификатор отправления (только для чтения)."""
        return self._id

    # Managed property для цены с валидацией
    @property
    def price(self):
        """Стоимость отправления (руб)."""
        if self._calculated_price is None:
            raise ValueError("Цена еще не была рассчитана. Сначала вызовите calculate_price.")
        return self._calculated_price

    @price.setter
    def price(self, value):
        """Устанавливает стоимость с проверкой."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Стоимость должна быть положительным числом.")
        self._calculated_price = round(value, 2)

    # Dunder методы
    def __str__(self):
        """Строковое представление для пользователя."""
        return f"{self.name} №{self._id} | {self.distance_km}км | {self.weight_kg}кг | {self.delivery_type}"

    def __repr__(self):
        """Строковое представление для разработчика."""
        return f"{self.__class__.__name__}(id={self._id}, name='{self.name}', distance={self.distance_km}, weight={self.weight_kg})"

    def __eq__(self, other):
        """Проверка на равенство по ID."""
        if not isinstance(other, PostalItem):
            return False
        return self._id == other._id

    def __lt__(self, other):
        """Сравнение по стоимости (для сортировки)."""
        if not isinstance(other, PostalItem):
            return NotImplemented
        return self.price < other.price

    # Class method для работы с managed-атрибутом класса
    @classmethod
    def get_instances_count(cls):
        """Возвращает количество созданных отправлений."""
        return cls._instances_count

    @abstractmethod
    def calculate_price(self, calculator):
        """Абстрактный метод для расчета цены."""
        pass

    def get_details(self):
        """Возвращает детальную информацию об отправлении."""
        return {
            'id': self._id,
            'type': self.name,
            'distance': self.distance_km,
            'weight': self.weight_kg,
            'delivery_type': self.delivery_type,
            'price': self._calculated_price
        }