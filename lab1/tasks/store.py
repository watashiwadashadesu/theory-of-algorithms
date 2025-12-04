#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть словарь кодов товаров
goods = {
    'Лампа': '12345',
    'Стол': '23456',
    'Диван': '34567',
    'Стул': '45678',
}

# Есть словарь списков количества товаров на складе
store = {
    '12345': [
        {'quantity': 27, 'price': 42},
    ],
    '23456': [
        {'quantity': 22, 'price': 510},
        {'quantity': 32, 'price': 520},
    ],
    '34567': [
        {'quantity': 2, 'price': 1200},
        {'quantity': 1, 'price': 1150},
    ],
    '45678': [
        {'quantity': 50, 'price': 100},
        {'quantity': 12, 'price': 95},
        {'quantity': 43, 'price': 97},
    ],
}


def view_store():
    """Расчет стоимости товаров на складе"""
    result = ""

    # Для каждого товара рассчитываем общее количество и стоимость
    for product_name, product_code in goods.items():
        product_items = store[product_code]

        # Суммируем количество и стоимость по всем партиям товара
        total_quantity = 0
        total_cost = 0

        for item in product_items:
            total_quantity += item['quantity']
            total_cost += item['quantity'] * item['price']

        result += (f"{product_name} - {total_quantity} шт, "
                   f"стоимость {total_cost} руб\n")

    return result
