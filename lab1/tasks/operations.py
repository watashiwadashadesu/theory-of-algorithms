#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import product


def find_combinations(target=25):
    numbers = [1, 2, 3, 4, 5]
    ops = ['+', '-', '*']
    brackets = [True, False]  # использовать скобки или нет

    solutions = set()  # для хранения уникальных решений

    # Генерируем все возможные комбинации операторов
    for op_comb in product(ops, repeat=len(numbers) - 1):
        # Генерируем все возможные расстановки скобок (упрощенно)
        for use_brackets in brackets:
            if use_brackets:
                # Вариант 1: (a op b) op c op d op e
                expr1 = (f"({numbers[0]}{op_comb[0]}{numbers[1]})"
                         f"{op_comb[1]}{numbers[2]}{op_comb[2]}"
                         f"{numbers[3]}{op_comb[3]}{numbers[4]}")
                # Вариант 2: a op (b op c) op d op e
                expr2 = (f"{numbers[0]}{op_comb[0]}({numbers[1]}"
                         f"{op_comb[1]}{numbers[2]}){op_comb[2]}"
                         f"{numbers[3]}{op_comb[3]}{numbers[4]}")
                # Вариант 3: a op b op (c op d) op e
                expr3 = (f"{numbers[0]}{op_comb[0]}{numbers[1]}"
                         f"{op_comb[1]}({numbers[2]}{op_comb[2]}"
                         f"{numbers[3]}){op_comb[3]}{numbers[4]}")
                # Вариант 4: (a op b op c) op d op e
                expr4 = (f"({numbers[0]}{op_comb[0]}{numbers[1]}"
                         f"{op_comb[1]}{numbers[2]}){op_comb[2]}"
                         f"{numbers[3]}{op_comb[3]}{numbers[4]}")

                for expr in [expr1, expr2, expr3, expr4]:
                    try:
                        if eval(expr) == target:
                            solutions.add(expr)
                    except:
                        pass
            else:
                # Без скобок
                expr = (f"{numbers[0]}{op_comb[0]}{numbers[1]}"
                        f"{op_comb[1]}{numbers[2]}{op_comb[2]}"
                        f"{numbers[3]}{op_comb[3]}{numbers[4]}")
                try:
                    if eval(expr) == target:
                        solutions.add(expr)
                except:
                    pass

    return solutions


def res():
    """Поиск способов получить 25 из чисел 1,2,3,4,5"""
    solutions = find_combinations(25)

    if not solutions:
        return "Не найдено способов получить 25"

    result = f"Найдено {len(solutions)} способов получить 25:\n"
    for i, solution in enumerate(solutions, 1):
        result += f"{i}. {solution} = 25\n"

    return result
