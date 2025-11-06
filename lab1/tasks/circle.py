#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Заданное значение радиуса круга
radius = 42
pi = 3.1415926

def calc_area():
    """Вычисление площади круга с точностью до 4-х знаков после запятой"""
    area = pi * radius ** 2
    return round(area, 4)

def is_in(point):
    """Проверка точки внутри круга"""
    distance = (point[0]**2 + point[1]**2)**0.5
    return distance <= radius

def is_out(point):
    """Проверка точки вне круга"""
    distance = (point[0]**2 + point[1]**2)**0.5
    return distance > radius

# Точки для проверки
point_1 = (23, 34)
point_2 = (30, 30)
