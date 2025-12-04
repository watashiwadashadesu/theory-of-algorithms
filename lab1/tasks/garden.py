#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# в саду сорвали цветы
garden = ('ромашка', 'роза', 'одуванчик', 'ромашка', 'гладиолус', 'подсолнух', 'роза',)

# на лугу сорвали цветы
meadow = ('клевер', 'одуванчик', 'ромашка', 'клевер', 'мак', 'одуванчик', 'ромашка',)


def flowers(garden_plants, meadow_plants):
    """Анализ цветов в саду и на лугу"""
    garden_set = set(garden_plants)
    meadow_set = set(meadow_plants)

    # 1. Все виды цветов
    all_flowers = garden_set.union(meadow_set)

    # 2. Цветы, которые растут и там и там
    common_flowers = garden_set.intersection(meadow_set)

    # 3. Цветы, которые растут только в саду
    only_garden = garden_set.difference(meadow_set)

    # 4. Цветы, которые растут только на лугу
    only_meadow = meadow_set.difference(garden_set)

    result = f"""Все виды цветов: {sorted(all_flowers)}
Цветы, растущие и в саду и на лугу: {sorted(common_flowers)}
Цветы, растущие только в саду: {sorted(only_garden)}
Цветы, растущие только на лугу: {sorted(only_meadow)}"""

    return result
