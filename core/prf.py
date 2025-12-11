"""
Модуль для реализации примитивно-рекурсивных функций (ПРФ).

Содержит базовые классы для базовых функций и операторов.
"""

import json
from typing import List, Any, Optional, Dict


class PrimitiveFunction:
    """Базовый класс для примитивных функций."""
    
    def evaluate(self, args: List[int]) -> int:
        """
        Вычисляет значение функции на заданных аргументах.
        
        Args:
            args: Список аргументов функции
            
        Returns:
            Результат вычисления
        """
        raise NotImplementedError
    
    def arity(self) -> int:
        """
        Возвращает арность функции (количество аргументов).
        
        Returns:
            Арность функции
        """
        raise NotImplementedError
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует функцию в словарь для сериализации.
        
        Returns:
            Словарь с описанием функции
        """
        raise NotImplementedError
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PrimitiveFunction':
        """
        Создает функцию из словаря.
        
        Args:
            data: Словарь с описанием функции
            
        Returns:
            Экземпляр функции
        """
        raise NotImplementedError


class Zero(PrimitiveFunction):
    """Функция нуля Z(x) = 0."""
    
    def __init__(self):
        pass
    
    def evaluate(self, args: List[int]) -> int:
        """Z(x) = 0 для любого x."""
        return 0
    
    def arity(self) -> int:
        return 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": "zero"}
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Zero':
        return Zero()
    
    def __repr__(self) -> str:
        return "Z(x)"


class Successor(PrimitiveFunction):
    """Функция следования S(x) = x + 1."""
    
    def __init__(self):
        pass
    
    def evaluate(self, args: List[int]) -> int:
        """S(x) = x + 1."""
        if len(args) < 1:
            raise ValueError("Successor requires at least 1 argument")
        return args[0] + 1
    
    def arity(self) -> int:
        return 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": "successor"}
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Successor':
        return Successor()
    
    def __repr__(self) -> str:
        return "S(x)"


class Constant(PrimitiveFunction):
    """Константная функция C_n(x₁,...,xₙ) = n."""
    
    def __init__(self, value: int, arity: int = 0):
        """
        Args:
            value: Значение константы
            arity: Арность функции (0 для константы без аргументов)
        """
        self.value = value
        self.arity_value = arity
    
    def evaluate(self, args: List[int]) -> int:
        """C_n(...) = n (игнорирует аргументы)."""
        if len(args) != self.arity_value:
            raise ValueError(f"Constant requires {self.arity_value} arguments, got {len(args)}")
        return self.value
    
    def arity(self) -> int:
        return self.arity_value
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": "constant", "value": self.value, "arity": self.arity_value}
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Constant':
        return Constant(data["value"], data.get("arity", 0))
    
    def __repr__(self) -> str:
        return f"C_{self.value}()" if self.arity_value == 0 else f"C_{self.value}(x₁,...,xₙ)"


class Projection(PrimitiveFunction):
    """Функция проекции P_i^n(x₁,...,xₙ) = xᵢ."""
    
    def __init__(self, n: int, i: int):
        """
        Args:
            n: Арность функции (количество аргументов)
            i: Индекс проекции (от 1 до n)
        """
        if i < 1 or i > n:
            raise ValueError(f"Projection index must be between 1 and {n}")
        self.n = n
        self.i = i
    
    def evaluate(self, args: List[int]) -> int:
        """P_i^n(x₁,...,xₙ) = xᵢ."""
        if len(args) < self.n:
            raise ValueError(f"Projection requires {self.n} arguments, got {len(args)}")
        return args[self.i - 1]  # Индекс с 1, поэтому вычитаем 1
    
    def arity(self) -> int:
        return self.n
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": "projection", "n": self.n, "i": self.i}
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Projection':
        return Projection(data["n"], data["i"])
    
    def __repr__(self) -> str:
        return f"P_{self.i}^{self.n}(x₁,...,xₙ)"


class Composition(PrimitiveFunction):
    """Оператор суперпозиции (композиции)."""
    
    def __init__(self, f: PrimitiveFunction, g_list: List[PrimitiveFunction]):
        """
        Args:
            f: Внешняя функция
            g_list: Список функций для подстановки
        """
        if len(g_list) != f.arity():
            raise ValueError(f"Composition requires {f.arity()} functions, got {len(g_list)}")
        self.f = f
        self.g_list = g_list
    
    def evaluate(self, args: List[int]) -> int:
        """Вычисляет f(g₁(args), ..., gₙ(args))."""
        # Вычисляем все g_i(args)
        g_results = [g.evaluate(args) for g in self.g_list]
        # Применяем f к результатам
        return self.f.evaluate(g_results)
    
    def arity(self) -> int:
        if not self.g_list:
            return 0
        return self.g_list[0].arity()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "composition",
            "f": self.f.to_dict(),
            "g_list": [g.to_dict() for g in self.g_list]
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Composition':
        f = function_from_dict(data["f"])
        g_list = [function_from_dict(g) for g in data["g_list"]]
        return Composition(f, g_list)
    
    def __repr__(self) -> str:
        return f"Composition({self.f}, [{', '.join(str(g) for g in self.g_list)}])"


class PrimitiveRecursion(PrimitiveFunction):
    """Оператор примитивной рекурсии."""
    
    def __init__(self, g: PrimitiveFunction, h: PrimitiveFunction):
        """
        Args:
            g: Базовая функция (для случая x=0)
            h: Рекурсивная функция (для случая x>0)
        """
        # g должна иметь арность на 1 меньше, чем h
        # h должна иметь арность на 2 больше, чем g
        if h.arity() != g.arity() + 2:
            raise ValueError(
                f"PrimitiveRecursion: h must have arity {g.arity() + 2}, got {h.arity()}"
            )
        self.g = g
        self.h = h
    
    def evaluate(self, args: List[int]) -> int:
        """
        Вычисляет примитивную рекурсию:
        f(0, y₁, ..., yₙ) = g(y₁, ..., yₙ)
        f(x+1, y₁, ..., yₙ) = h(x, f(x, y₁, ..., yₙ), y₁, ..., yₙ)
        """
        if len(args) < 1:
            raise ValueError("PrimitiveRecursion requires at least 1 argument")
        
        x = args[0]
        y_args = args[1:]
        
        # Базовый случай: x = 0
        if x == 0:
            return self.g.evaluate(y_args)
        
        # Рекурсивный случай: x > 0
        # Вычисляем f(x-1, y₁, ..., yₙ)
        prev_result = self.evaluate([x - 1] + y_args)
        
        # Вычисляем h(x-1, f(x-1, ...), y₁, ..., yₙ)
        h_args = [x - 1, prev_result] + y_args
        return self.h.evaluate(h_args)
    
    def arity(self) -> int:
        return self.g.arity() + 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "primitive_recursion",
            "g": self.g.to_dict(),
            "h": self.h.to_dict()
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PrimitiveRecursion':
        g = function_from_dict(data["g"])
        h = function_from_dict(data["h"])
        return PrimitiveRecursion(g, h)
    
    def __repr__(self) -> str:
        return f"PrimitiveRecursion({self.g}, {self.h})"


# Фабрика для создания функций из словаря
def function_from_dict(data: Dict[str, Any]) -> PrimitiveFunction:
    """Создает функцию из словаря."""
    func_type = data.get("type")
    
    if func_type == "zero":
        return Zero.from_dict(data)
    elif func_type == "successor":
        return Successor.from_dict(data)
    elif func_type == "constant":
        return Constant.from_dict(data)
    elif func_type == "projection":
        return Projection.from_dict(data)
    elif func_type == "composition":
        return Composition.from_dict(data)
    elif func_type == "primitive_recursion":
        return PrimitiveRecursion.from_dict(data)
    else:
        raise ValueError(f"Unknown function type: {func_type}")


# Предопределенные функции
def create_addition() -> PrimitiveFunction:
    """Создает функцию сложения add(x, y) через примитивную рекурсию."""
    # add(0, y) = P₁¹(y) = y
    # add(x+1, y) = S(P₂³(x, add(x, y), y)) = add(x, y) + 1
    g = Projection(1, 1)  # P₁¹
    h = Composition(
        Successor(),
        [Projection(3, 2)]  # P₂³ - берет второй аргумент (add(x, y))
    )
    return PrimitiveRecursion(g, h)


def create_multiplication() -> PrimitiveFunction:
    """Создает функцию умножения mult(x, y) через примитивную рекурсию."""
    # mult(0, y) = Z(y) = 0
    # mult(x+1, y) = add(mult(x, y), y) = add(P₂³(x, mult(x, y), y), P₃³(x, mult(x, y), y))
    add = create_addition()
    # g должна иметь арность 1 (для y)
    g = Zero()  # Z(y) = 0
    # h должна иметь арность 3: h(x, mult(x,y), y) = add(mult(x,y), y)
    h = Composition(
        add,
        [Projection(3, 2), Projection(3, 3)]  # add(P₂³, P₃³) = add(mult(x,y), y)
    )
    return PrimitiveRecursion(g, h)


def create_factorial() -> PrimitiveFunction:
    """Создает функцию факториала fact(x) через примитивную рекурсию."""
    # fact(0) = 1
    # fact(x+1) = mult(x+1, fact(x)) = mult(S(x), fact(x))
    mult = create_multiplication()
    # g должна иметь арность 0 (константа 1)
    g = Constant(1, arity=0)  # Константа 1 с арностью 0
    # h должна иметь арность 2: h(x, fact(x)) = mult(x+1, fact(x))
    # h вычисляет mult(x+1, fact(x)) = mult(S(P₁²), P₂²)
    h = Composition(
        mult,
        [
            Composition(Successor(), [Projection(2, 1)]),  # S(P₁²) = x+1
            Projection(2, 2)  # P₂² = fact(x)
        ]
    )
    return PrimitiveRecursion(g, h)

