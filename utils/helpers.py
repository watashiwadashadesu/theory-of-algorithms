"""
Вспомогательные функции для PRF Constructor.
"""

import json
from typing import Any, Dict, List


def format_function_name(function_type: str) -> str:
    """
    Форматирует имя функции для отображения.
    
    Args:
        function_type: Тип функции
        
    Returns:
        Отформатированное имя
    """
    names = {
        "zero": "Z(x)",
        "successor": "S(x)",
        "projection": "P",
        "composition": "Composition",
        "primitive_recursion": "Recursion"
    }
    return names.get(function_type, function_type)


def format_arguments(args: List[int]) -> str:
    """
    Форматирует список аргументов для отображения.
    
    Args:
        args: Список аргументов
        
    Returns:
        Отформатированная строка
    """
    return ", ".join(str(a) for a in args)


def safe_json_loads(data: str, default: Any = None) -> Any:
    """
    Безопасно загружает JSON.
    
    Args:
        data: JSON строка
        default: Значение по умолчанию при ошибке
        
    Returns:
        Распарсенный объект или default
    """
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default


def truncate_string(s: str, max_length: int = 50) -> str:
    """
    Обрезает строку до максимальной длины.
    
    Args:
        s: Строка
        max_length: Максимальная длина
        
    Returns:
        Обрезанная строка
    """
    if len(s) <= max_length:
        return s
    return s[:max_length - 3] + "..."


def get_function_color(function_type: str) -> str:
    """
    Возвращает цвет для типа функции.
    
    Args:
        function_type: Тип функции
        
    Returns:
        Цвет в формате hex
    """
    colors = {
        "zero": "#FF6B6B",  # Красный
        "successor": "#4ECDC4",  # Голубой
        "projection": "#95E1D3",  # Светло-голубой
        "composition": "#F38181",  # Розовый
        "primitive_recursion": "#AA96DA"  # Фиолетовый
    }
    return colors.get(function_type, "#CCCCCC")  # Серый по умолчанию

