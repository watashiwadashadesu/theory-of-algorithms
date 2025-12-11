"""
Модуль для валидации примитивно-рекурсивных функций.

Проверяет корректность построения функций и их арность.
"""

from typing import List, Optional
from core.prf import PrimitiveFunction, Composition, PrimitiveRecursion


class ValidationError(Exception):
    """Исключение для ошибок валидации."""
    pass


class Validator:
    """Валидатор примитивно-рекурсивных функций."""
    
    @staticmethod
    def validate(function: PrimitiveFunction) -> List[str]:
        """
        Валидирует функцию и возвращает список ошибок.
        
        Args:
            function: Функция для валидации
            
        Returns:
            Список ошибок (пустой, если функция корректна)
        """
        errors = []
        
        try:
            Validator._validate_recursive(function, errors, set())
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
        
        return errors
    
    @staticmethod
    def _validate_recursive(function: PrimitiveFunction, errors: List[str], 
                           visited: set) -> None:
        """Рекурсивная валидация функции."""
        # Проверка на циклические зависимости
        func_id = id(function)
        if func_id in visited:
            errors.append("Circular dependency detected")
            return
        
        visited.add(func_id)
        
        try:
            # Проверка арности
            arity = function.arity()
            if arity < 0:
                errors.append(f"Invalid arity: {arity}")
            
            # Валидация в зависимости от типа
            if isinstance(function, Composition):
                comp = function
                # Проверка количества функций в композиции
                if len(comp.g_list) != comp.f.arity():
                    errors.append(
                        f"Composition arity mismatch: f requires {comp.f.arity()} "
                        f"functions, got {len(comp.g_list)}"
                    )
                
                # Проверка арности функций в списке
                if comp.g_list:
                    first_arity = comp.g_list[0].arity()
                    for i, g in enumerate(comp.g_list):
                        if g.arity() != first_arity:
                            errors.append(
                                f"Composition: all g functions must have same arity, "
                                f"g[{i}] has arity {g.arity()}, expected {first_arity}"
                            )
                
                # Рекурсивная валидация
                Validator._validate_recursive(comp.f, errors, visited)
                for g in comp.g_list:
                    Validator._validate_recursive(g, errors, visited)
            
            elif isinstance(function, PrimitiveRecursion):
                rec = function
                g_arity = rec.g.arity()
                h_arity = rec.h.arity()
                
                # Проверка соотношения арностей
                if h_arity != g_arity + 2:
                    errors.append(
                        f"PrimitiveRecursion: h must have arity {g_arity + 2}, "
                        f"got {h_arity}"
                    )
                
                # Рекурсивная валидация
                Validator._validate_recursive(rec.g, errors, visited)
                Validator._validate_recursive(rec.h, errors, visited)
        
        finally:
            visited.remove(func_id)
    
    @staticmethod
    def validate_arguments(function: PrimitiveFunction, args: List[int]) -> Optional[str]:
        """
        Проверяет корректность аргументов для функции.
        
        Args:
            function: Функция
            args: Аргументы
            
        Returns:
            Сообщение об ошибке или None, если все корректно
        """
        if len(args) != function.arity():
            return (
                f"Argument count mismatch: function requires {function.arity()} "
                f"arguments, got {len(args)}"
            )
        
        # Проверка на отрицательные аргументы (для некоторых функций)
        if any(a < 0 for a in args):
            return "Negative arguments are not supported for primitive recursive functions"
        
        return None
    
    @staticmethod
    def is_valid(function: PrimitiveFunction) -> bool:
        """
        Проверяет, является ли функция валидной.
        
        Args:
            function: Функция для проверки
            
        Returns:
            True, если функция валидна
        """
        errors = Validator.validate(function)
        return len(errors) == 0

