class PriceCalculator:
    """Класс для расчета стоимости почтовых отправлений."""

    # Базовые тарифы (условные единицы)
    BASE_RATE_LETTER = 10
    BASE_RATE_BANDEROL = 20
    BASE_RATE_PARCEL = 50

    # Коэффициенты за расстояние
    DISTANCE_MULTIPLIER = 0.1  # За каждый км

    # Коэффициенты за вес
    WEIGHT_MULTIPLIER_LETTER = 2
    WEIGHT_MULTIPLIER_BANDEROL = 5
    WEIGHT_MULTIPLIER_PARCEL = 10

    # Коэффициенты за тип доставки
    DELIVERY_MULTIPLIERS = {
        "стандарт": 1.0,
        "ускоренная": 1.5,
        "экспресс": 2.0
    }

    # Доплаты
    REGISTERED_LETTER_FEE = 50  # Доплата за заказное письмо
    FRAGILE_PARCEL_FEE = 100    # Доплата за хрупкость
    VOLUME_SURCHARGE_THRESHOLD = 5000  # см³, порог объема
    VOLUME_SURCHARGE_RATE = 0.02       # Надбавка за объем

    def calculate_letter(self, letter):
        """Рассчитывает стоимость письма."""
        base_price = self.BASE_RATE_LETTER
        distance_cost = letter.distance_km * self.DISTANCE_MULTIPLIER
        weight_cost = letter.weight_kg * self.WEIGHT_MULTIPLIER_LETTER
        delivery_multiplier = self.DELIVERY_MULTIPLIERS.get(letter.delivery_type, 1.0)

        total = (base_price + distance_cost + weight_cost) * delivery_multiplier

        if letter.is_registered:
            total += self.REGISTERED_LETTER_FEE

        return round(total, 2)

    def calculate_banderol(self, banderol):
        """Рассчитывает стоимость бандероли."""
        base_price = self.BASE_RATE_BANDEROL
        distance_cost = banderol.distance_km * self.DISTANCE_MULTIPLIER
        weight_cost = banderol.weight_kg * self.WEIGHT_MULTIPLIER_BANDEROL
        delivery_multiplier = self.DELIVERY_MULTIPLIERS.get(banderol.delivery_type, 1.0)

        total = (base_price + distance_cost + weight_cost) * delivery_multiplier

        # Надбавка за большой объем
        if banderol.volume_cubic_cm > self.VOLUME_SURCHARGE_THRESHOLD:
            volume_surcharge = banderol.volume_cubic_cm * self.VOLUME_SURCHARGE_RATE
            total += volume_surcharge

        return round(total, 2)

    def calculate_parcel(self, parcel):
        """Рассчитывает стоимость посылки."""
        base_price = self.BASE_RATE_PARCEL
        distance_cost = parcel.distance_km * self.DISTANCE_MULTIPLIER
        weight_cost = parcel.weight_kg * self.WEIGHT_MULTIPLIER_PARCEL
        delivery_multiplier = self.DELIVERY_MULTIPLIERS.get(parcel.delivery_type, 1.0)

        total = (base_price + distance_cost + weight_cost) * delivery_multiplier

        # Надбавка за большой объем
        if parcel.volume_cubic_cm > self.VOLUME_SURCHARGE_THRESHOLD:
            volume_surcharge = parcel.volume_cubic_cm * self.VOLUME_SURCHARGE_RATE
            total += volume_surcharge

        # Доплата за хрупкость
        if parcel.is_fragile:
            total += self.FRAGILE_PARCEL_FEE

        return round(total, 2)