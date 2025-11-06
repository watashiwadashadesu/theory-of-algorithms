#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Список с именами и ростом членов семьи (в см)
my_family_height = [
    ['Отец', 180],
    ['Мать', 165],
    ['Брат', 185],
]


def get_height():
    """Получение информации о росте семьи"""
    # Рост отца
    father_height = my_family_height[0][1]

    # Общий рост семьи
    total_height = sum(person[1] for person in my_family_height)

    return (f"Рост отца - {father_height} см\nОбщий рост моей семьи - "
            f"{total_height} см")

