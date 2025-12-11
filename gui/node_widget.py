"""
Виджеты узлов для визуализации функций на холсте.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Dict, Any
from utils.helpers import format_function_name, get_function_color


class NodeWidget:
    """Виджет узла функции на холсте."""
    
    def __init__(self, canvas: tk.Canvas, x: int, y: int, 
                 function_type: str, node_id: Optional[str] = None,
                 on_select: Optional[Callable] = None,
                 on_drag: Optional[Callable] = None):
        """
        Args:
            canvas: Холст Tkinter
            x, y: Координаты узла
            function_type: Тип функции
            node_id: Уникальный ID узла
            on_select: Callback при выборе узла
            on_drag: Callback при перетаскивании
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.function_type = function_type
        self.node_id = node_id or f"node_{id(self)}"
        self.on_select = on_select
        self.on_drag = on_drag
        
        self.width = 100
        self.height = 60
        self.selected = False
        
        self._create_widgets()
        self._bind_events()
    
    def _create_widgets(self) -> None:
        """Создает графические элементы узла."""
        color = get_function_color(self.function_type)
        name = format_function_name(self.function_type)
        
        # Прямоугольник узла
        self.rect_id = self.canvas.create_rectangle(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.x + self.width // 2,
            self.y + self.height // 2,
            fill=color,
            outline="black",
            width=2,
            tags=(self.node_id, "node")
        )
        
        # Текст с именем функции
        self.text_id = self.canvas.create_text(
            self.x,
            self.y,
            text=name,
            fill="black",
            font=("Arial", 10, "bold"),
            tags=(self.node_id, "node")
        )
    
    def _bind_events(self) -> None:
        """Привязывает события к узлу."""
        # Выбор узла
        self.canvas.tag_bind(self.node_id, "<Button-1>", self._on_click)
        # Перетаскивание
        self.canvas.tag_bind(self.node_id, "<B1-Motion>", self._on_drag)
    
    def _on_click(self, event: tk.Event) -> None:
        """Обработчик клика по узлу."""
        self.select()
        if self.on_select:
            self.on_select(self)
    
    def _on_drag(self, event: tk.Event) -> None:
        """Обработчик перетаскивания узла."""
        dx = event.x - self.x
        dy = event.y - self.y
        
        self.move(dx, dy)
        
        if self.on_drag:
            self.on_drag(self, dx, dy)
    
    def move(self, dx: int, dy: int) -> None:
        """Перемещает узел на заданное смещение."""
        self.x += dx
        self.y += dy
        
        self.canvas.move(self.node_id, dx, dy)
    
    def set_position(self, x: int, y: int) -> None:
        """Устанавливает позицию узла."""
        dx = x - self.x
        dy = y - self.y
        self.move(dx, dy)
    
    def select(self) -> None:
        """Выбирает узел."""
        if not self.selected:
            self.selected = True
            self.canvas.itemconfig(self.rect_id, outline="blue", width=3)
    
    def deselect(self) -> None:
        """Снимает выбор с узла."""
        if self.selected:
            self.selected = False
            self.canvas.itemconfig(self.rect_id, outline="black", width=2)
    
    def delete(self) -> None:
        """Удаляет узел с холста."""
        self.canvas.delete(self.node_id)
    
    def get_position(self) -> tuple:
        """Возвращает позицию узла."""
        return (self.x, self.y)
    
    def get_bounds(self) -> tuple:
        """Возвращает границы узла (x1, y1, x2, y2)."""
        return (
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.x + self.width // 2,
            self.y + self.height // 2
        )
    
    def contains_point(self, x: int, y: int) -> bool:
        """Проверяет, содержит ли узел точку."""
        x1, y1, x2, y2 = self.get_bounds()
        return x1 <= x <= x2 and y1 <= y <= y2


class ConnectionLine:
    """Линия соединения между узлами."""
    
    def __init__(self, canvas: tk.Canvas, from_node: NodeWidget, 
                 to_node: NodeWidget, line_id: Optional[str] = None):
        """
        Args:
            canvas: Холст Tkinter
            from_node: Исходный узел
            to_node: Целевой узел
            line_id: Уникальный ID линии
        """
        self.canvas = canvas
        self.from_node = from_node
        self.to_node = to_node
        self.line_id = line_id or f"line_{id(self)}"
        
        self._create_line()
    
    def _create_line(self) -> None:
        """Создает линию на холсте."""
        from_x, from_y = self.from_node.get_position()
        to_x, to_y = self.to_node.get_position()
        
        # Смещаем начало и конец линии к краям узлов
        from_x += self.from_node.width // 2
        to_x -= self.to_node.width // 2
        
        self.line_id = self.canvas.create_line(
            from_x, from_y,
            to_x, to_y,
            fill="gray",
            width=2,
            arrow=tk.LAST,
            tags=(self.line_id, "connection")
        )
    
    def update(self) -> None:
        """Обновляет позицию линии."""
        from_x, from_y = self.from_node.get_position()
        to_x, to_y = self.to_node.get_position()
        
        from_x += self.from_node.width // 2
        to_x -= self.to_node.width // 2
        
        self.canvas.coords(self.line_id, from_x, from_y, to_x, to_y)
    
    def delete(self) -> None:
        """Удаляет линию с холста."""
        self.canvas.delete(self.line_id)

