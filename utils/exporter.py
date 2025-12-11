"""
Модуль для экспорта функций в различные форматы.
"""

from typing import Optional
from core.prf import PrimitiveFunction, Zero, Successor, Constant, Projection, Composition, PrimitiveRecursion


def export_to_latex(function: PrimitiveFunction, name: Optional[str] = None) -> str:
    """
    Экспортирует функцию в LaTeX формат.
    
    Args:
        function: Функция для экспорта
        name: Имя функции
        
    Returns:
        LaTeX код
    """
    lines = []
    lines.append("\\documentclass{article}")
    lines.append("\\usepackage{amsmath}")
    lines.append("\\usepackage{amssymb}")
    lines.append("\\begin{document}")
    lines.append("")
    
    if name:
        lines.append(f"\\section*{{{name}}}")
        lines.append("")
    
    lines.append("\\begin{align*}")
    latex_expr = _function_to_latex(function)
    lines.append(f"  {latex_expr}")
    lines.append("\\end{align*}")
    lines.append("")
    lines.append("\\end{document}")
    
    return "\n".join(lines)


def _function_to_latex(function: PrimitiveFunction) -> str:
    """Преобразует функцию в LaTeX выражение."""
    if isinstance(function, Zero):
        return "Z(x) = 0"
    
    elif isinstance(function, Successor):
        return "S(x) = x + 1"
    
    elif isinstance(function, Constant):
        if function.arity() == 0:
            return f"C_{{{function.value}}}() = {function.value}"
        else:
            return f"C_{{{function.value}}}(x_1, \\ldots, x_{{{function.arity()}}}) = {function.value}"
    
    elif isinstance(function, Projection):
        return f"P_{{{function.i}}}^{{{function.n}}}(x_1, \\ldots, x_{{{function.n}}}) = x_{{{function.i}}}"
    
    elif isinstance(function, Composition):
        f_latex = _function_to_latex(function.f)
        g_latex_list = [_function_to_latex(g) for g in function.g_list]
        return f"\\text{{Composition}}({f_latex}, [{', '.join(g_latex_list)}])"
    
    elif isinstance(function, PrimitiveRecursion):
        g_latex = _function_to_latex(function.g)
        h_latex = _function_to_latex(function.h)
        return f"\\text{{Recursion}}({g_latex}, {h_latex})"
    
    else:
        return str(function)


def export_to_json(function: PrimitiveFunction, name: Optional[str] = None) -> dict:
    """
    Экспортирует функцию в JSON формат.
    
    Args:
        function: Функция для экспорта
        name: Имя функции
        
    Returns:
        Словарь с данными функции
    """
    return {
        "name": name or "function",
        "definition": function.to_dict(),
        "arity": function.arity()
    }

