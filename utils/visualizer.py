"""
Модуль для визуализации деревьев функций (опционально, с использованием Graphviz).
"""

from typing import Optional
from core.prf import PrimitiveFunction, Composition, PrimitiveRecursion


def visualize_function(function: PrimitiveFunction, output_path: Optional[str] = None) -> Optional[str]:
    """
    Визуализирует структуру функции в виде дерева.
    
    Args:
        function: Функция для визуализации
        output_path: Путь для сохранения изображения (опционально)
        
    Returns:
        Путь к созданному файлу или None
    """
    try:
        import graphviz
    except ImportError:
        print("Graphviz не установлен. Визуализация недоступна.")
        return None
    
    # Создаем граф
    dot = graphviz.Digraph(comment='PRF Function')
    dot.attr('node', shape='box', style='rounded')
    
    # Строим дерево
    _add_node_to_graph(dot, function, "root")
    
    # Рендерим
    if output_path:
        dot.render(output_path, format='png', cleanup=True)
        return output_path
    else:
        return dot.source


def _add_node_to_graph(dot, function: PrimitiveFunction, node_id: str, parent_id: Optional[str] = None) -> None:
    """Рекурсивно добавляет узлы в граф."""
    func_type = type(function).__name__
    label = f"{func_type}\\narity: {function.arity()}"
    
    dot.node(node_id, label)
    
    if parent_id:
        dot.edge(parent_id, node_id)
    
    # Добавляем дочерние узлы в зависимости от типа
    if isinstance(function, Composition):
        comp = function
        # Узел для f
        f_id = f"{node_id}_f"
        _add_node_to_graph(dot, comp.f, f_id, node_id)
        
        # Узлы для g_list
        for i, g in enumerate(comp.g_list):
            g_id = f"{node_id}_g{i}"
            _add_node_to_graph(dot, g, g_id, node_id)
    
    elif isinstance(function, PrimitiveRecursion):
        rec = function
        # Узел для g
        g_id = f"{node_id}_g"
        _add_node_to_graph(dot, rec.g, g_id, node_id)
        
        # Узел для h
        h_id = f"{node_id}_h"
        _add_node_to_graph(dot, rec.h, h_id, node_id)

