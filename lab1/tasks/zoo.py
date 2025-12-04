#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def shake_zoo():
    """Операции с зоопарком"""
    # Исходный список животных в зоопарке
    zoo = ['lion', 'kangaroo', 'elephant', 'monkey']

    result = ""

    # 1. Посадить медведя между львом и кенгуру
    zoo.insert(1, 'bear')
    result += f"1. После добавления медведя: {zoo}\n"

    # 2. Добавить птиц в конец зоопарка
    birds = ['rooster', 'ostrich', 'lark']
    zoo.extend(birds)
    result += f"2. После добавления птиц: {zoo}\n"

    # 3. Убрать слона
    zoo.remove('elephant')
    result += f"3. После удаления слона: {zoo}\n"

    # 4. Найти клетки льва и жаворонка (нумерация с 1 для человека)
    lion_cage = zoo.index('lion') + 1
    lark_cage = zoo.index('lark') + 1
    result += (f"4. Лев сидит в клетке №{lion_cage}, "
               f"жаворонок в клетке №{lark_cage}\n")

    return result
