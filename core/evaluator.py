"""
Модуль для вычисления значений примитивно-рекурсивных функций.

Содержит класс для пошагового вычисления с отслеживанием промежуточных результатов.
"""

import sys
from typing import List, Dict, Any, Optional
from core.prf import PrimitiveFunction

# Увеличиваем лимит рекурсии Python для вычисления больших факториалов
# Это необходимо, так как примитивная рекурсия создает очень глубокую вложенность
# Для fact(9) нужно примерно 200000 уровней рекурсии из-за вложенности (факториал -> умножение -> сложение)
if sys.getrecursionlimit() < 300000:
    sys.setrecursionlimit(300000)


class EvaluationStep:
    """Представляет один шаг вычисления."""
    
    def __init__(self, function: PrimitiveFunction, args: List[int], result: int, 
                 depth: int = 0, step_num: int = 0):
        self.function = function
        self.args = args
        self.result = result
        self.depth = depth
        self.step_num = step_num
        self.substeps: List['EvaluationStep'] = []
    
    def __repr__(self) -> str:
        return f"Step {self.step_num}: {self.function}({self.args}) = {self.result}"


class Evaluator:
    """Вычислитель примитивно-рекурсивных функций с пошаговым отслеживанием."""
    
    def __init__(self, max_depth: int = 300000, max_steps: int = 100000000):
        """
        Args:
            max_depth: Максимальная глубина рекурсии
            max_steps: Максимальное количество шагов
        """
        self.max_depth = max_depth
        self.max_steps = max_steps
        self.step_counter = 0
        self.steps: List[EvaluationStep] = []
        self.warnings: List[str] = []
    
    def evaluate(self, function: PrimitiveFunction, args: List[int], 
                 track_steps: bool = False) -> int:
        """
        Вычисляет значение функции на заданных аргументах.
        
        Args:
            function: Функция для вычисления
            args: Аргументы функции
            track_steps: Если True, отслеживает шаги вычисления
            
        Returns:
            Результат вычисления
            
        Raises:
            ValueError: Если аргументы некорректны
            RecursionError: Если превышена максимальная глубина рекурсии
        """
        # Проверка арности
        if len(args) != function.arity():
            raise ValueError(
                f"Function arity mismatch: expected {function.arity()}, got {len(args)}"
            )
        
        # Проверка на большие числа
        if any(abs(a) > 10**6 for a in args):
            self.warnings.append("Large arguments detected, computation may be slow")
        
        self.step_counter = 0
        self.steps = []
        self.warnings = []
        
        if track_steps:
            result = self._evaluate_with_tracking(function, args, depth=0)
        else:
            result = self._evaluate_simple(function, args, depth=0)
        
        return result
    
    def _evaluate_simple(self, function: PrimitiveFunction, args: List[int], 
                        depth: int) -> int:
        """Простое вычисление без отслеживания шагов."""
        if depth > self.max_depth:
            raise RecursionError(f"Maximum recursion depth {self.max_depth} exceeded")
        
        if self.step_counter > self.max_steps:
            raise RecursionError(f"Maximum steps {self.max_steps} exceeded")
        
        self.step_counter += 1
        
        # Прямое вычисление в зависимости от типа функции
        from core.prf import Zero, Successor, Constant, Projection, Composition, PrimitiveRecursion
        
        if isinstance(function, (Zero, Successor, Constant, Projection)):
            # Базовые функции вычисляются напрямую
            return function.evaluate(args)
        
        elif isinstance(function, Composition):
            # Композиция
            comp = function
            g_results = []
            for g in comp.g_list:
                g_result = self._evaluate_simple(g, args, depth + 1)
                g_results.append(g_result)
            return self._evaluate_simple(comp.f, g_results, depth + 1)
        
        elif isinstance(function, PrimitiveRecursion):
            # Примитивная рекурсия
            rec = function
            x = args[0]
            y_args = args[1:]
            
            if x == 0:
                return self._evaluate_simple(rec.g, y_args, depth + 1)
            else:
                # Проверяем глубину перед рекурсивным вызовом
                if depth + 1 > self.max_depth:
                    raise RecursionError(f"Maximum recursion depth {self.max_depth} exceeded")
                prev_result = self._evaluate_simple(rec, [x - 1] + y_args, depth + 1)
                h_args = [x - 1, prev_result] + y_args
                return self._evaluate_simple(rec.h, h_args, depth + 1)
        
        else:
            # Общий случай
            return function.evaluate(args)
    
    def _evaluate_with_tracking(self, function: PrimitiveFunction, args: List[int], 
                                depth: int) -> int:
        """Вычисление с отслеживанием шагов."""
        if depth > self.max_depth:
            raise RecursionError(f"Maximum recursion depth {self.max_depth} exceeded")
        
        if self.step_counter > self.max_steps:
            raise RecursionError(f"Maximum steps {self.max_steps} exceeded")
        
        self.step_counter += 1
        step_num = self.step_counter
        
        # Вычисляем результат
        from core.prf import Zero, Successor, Constant, Projection, Composition, PrimitiveRecursion
        
        if isinstance(function, (Zero, Successor, Constant, Projection)):
            result = function.evaluate(args)
            step = EvaluationStep(function, args, result, depth, step_num)
            self.steps.append(step)
            return result
        
        elif isinstance(function, Composition):
            comp = function
            g_results = []
            substeps = []
            
            for g in comp.g_list:
                g_result = self._evaluate_with_tracking(g, args, depth + 1)
                g_results.append(g_result)
                substeps.append(self.steps[-1] if self.steps else None)
            
            f_result = self._evaluate_with_tracking(comp.f, g_results, depth + 1)
            step = EvaluationStep(function, args, f_result, depth, step_num)
            step.substeps = [s for s in substeps if s is not None]
            self.steps.append(step)
            return f_result
        
        elif isinstance(function, PrimitiveRecursion):
            rec = function
            x = args[0]
            y_args = args[1:]
            
            if x == 0:
                result = self._evaluate_with_tracking(rec.g, y_args, depth + 1)
            else:
                prev_result = self._evaluate_with_tracking(rec, [x - 1] + y_args, depth + 1)
                h_args = [x - 1, prev_result] + y_args
                result = self._evaluate_with_tracking(rec.h, h_args, depth + 1)
            
            step = EvaluationStep(function, args, result, depth, step_num)
            self.steps.append(step)
            return result
        
        else:
            result = function.evaluate(args)
            step = EvaluationStep(function, args, result, depth, step_num)
            self.steps.append(step)
            return result
    
    def get_steps(self) -> List[EvaluationStep]:
        """Возвращает список шагов вычисления."""
        return self.steps
    
    def get_warnings(self) -> List[str]:
        """Возвращает список предупреждений."""
        return self.warnings
    
    def get_statistics(self) -> Dict[str, Any]:
        """Возвращает статистику вычисления."""
        return {
            "total_steps": self.step_counter,
            "max_depth": max((s.depth for s in self.steps), default=0),
            "warnings": len(self.warnings)
        }

