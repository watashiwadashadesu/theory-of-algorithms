#!/usr/bin/env python3
# -*- coding: utf-8 -*-
sweets = {
    'печенье': [
        {'shop': 'пятерочка', 'price': 9.99},
        {'shop': 'ашан', 'price': 10.99}
    ],
    'конфеты': [
        {'shop': 'магнит', 'price': 30.99},
        {'shop': 'пятерочка', 'price': 32.99}
    ],
    'карамель': [
        {'shop': 'магнит', 'price': 41.99},
        {'shop': 'ашан', 'price': 45.99}
    ],
    'пирожное': [
        {'shop': 'пятерочка', 'price': 59.99},
        {'shop': 'магнит', 'price': 62.99}
    ]
}

def get_sweets():
    """Получение информации о сладостях и ценах"""
    result = ""
    for sweet, prices in sweets.items():
        result += f"{sweet}:\n"
        for offer in prices:
            result += f"  {offer['shop']}: {offer['price']} руб\n"
    return result

