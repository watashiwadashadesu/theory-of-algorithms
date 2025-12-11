"""
Виджет холста для визуального построения функций.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Dict, List, Callable, Any
from gui.node_widget import NodeWidget, ConnectionLine
from core.prf import PrimitiveFunction, function_from_dict
from utils.helpers import get_function_color


class CanvasWidget(ttk.Frame):
    """Холст для построения функций."""
    
    def __init__(self, parent, on_function_change: Optional[Callable] = None):
        """
        Args:
            parent: Родительский виджет
            on_function_change: Callback при изменении функции
        """
        super().__init__(parent)
        
        self.on_function_change = on_function_change
        
        # Создаем холст с прокруткой
        self.canvas = tk.Canvas(
            self,
            bg="white",
            scrollregion=(0, 0, 2000, 2000)
        )
        
        # Полосы прокрутки
        v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Размещение
        self.canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Данные
        self.nodes: Dict[str, NodeWidget] = {}
        self.connections: List[ConnectionLine] = []
        self.selected_node: Optional[NodeWidget] = None
        self.current_function: Optional[PrimitiveFunction] = None
        
        # Режим соединения узлов
        self.connection_mode = False
        self.connection_source: Optional[NodeWidget] = None
        
        # Дополнительные данные узлов для построения функций
        self.node_data: Dict[str, Dict[str, Any]] = {}  # node_id -> {params, connections}
        
        # Привязка событий
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<Button-3>", self._on_canvas_right_click)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Double-Button-1>", self._on_double_click)
        
        # Перетаскивание холста
        self.canvas.bind("<ButtonPress-2>", self._on_middle_press)
        self.canvas.bind("<B2-Motion>", self._on_middle_drag)
        self.last_pan_x = 0
        self.last_pan_y = 0
    
    def _on_canvas_click(self, event: tk.Event) -> None:
        """Обработчик клика по холсту."""
        # Снимаем выбор со всех узлов
        if self.selected_node:
            self.selected_node.deselect()
            self.selected_node = None
    
    def _on_canvas_right_click(self, event: tk.Event) -> None:
        """Обработчик правого клика по холсту."""
        # Проверяем, кликнули ли по узлу
        clicked_node = None
        for node in self.nodes.values():
            if node.contains_point(event.x, event.y):
                clicked_node = node
                break
        
        if clicked_node:
            self._show_node_context_menu(event, clicked_node)
        else:
            self._show_canvas_context_menu(event)
    
    def _on_double_click(self, event: tk.Event) -> None:
        """Обработчик двойного клика - начало соединения."""
        clicked_node = None
        for node in self.nodes.values():
            if node.contains_point(event.x, event.y):
                clicked_node = node
                break
        
        if clicked_node:
            self.connection_mode = True
            self.connection_source = clicked_node
            clicked_node.select()
    
    def _show_node_context_menu(self, event: tk.Event, node: NodeWidget) -> None:
        """Показывает контекстное меню для узла."""
        menu = tk.Menu(self.canvas, tearoff=0)
        
        if node.function_type == "projection":
            menu.add_command(label="Настроить проекцию...", 
                           command=lambda: self._configure_projection(node))
        
        menu.add_separator()
        menu.add_command(label="Удалить", command=lambda: self.delete_node(node.node_id))
        menu.add_separator()
        menu.add_command(label="Соединить с...", 
                        command=lambda: self._start_connection(node))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def _show_canvas_context_menu(self, event: tk.Event) -> None:
        """Показывает контекстное меню для холста."""
        menu = tk.Menu(self.canvas, tearoff=0)
        menu.add_command(label="Построить функцию", command=self._try_build_function)
        menu.add_separator()
        menu.add_command(label="Очистить", command=self.clear)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def _start_connection(self, node: NodeWidget) -> None:
        """Начинает режим соединения узлов."""
        self.connection_mode = True
        self.connection_source = node
        node.select()
    
    def _configure_projection(self, node: NodeWidget) -> None:
        """Настраивает параметры проекции."""
        from tkinter import simpledialog
        
        n = simpledialog.askinteger("Проекция", "Введите арность (n):", minvalue=1, maxvalue=10)
        if n:
            i = simpledialog.askinteger("Проекция", f"Введите индекс (от 1 до {n}):", 
                                       minvalue=1, maxvalue=n)
            if i:
                if node.node_id not in self.node_data:
                    self.node_data[node.node_id] = {}
                self.node_data[node.node_id]["n"] = n
                self.node_data[node.node_id]["i"] = i
                # Обновляем отображение
                node.function_type = f"projection_{n}_{i}"
                self.canvas.itemconfig(node.text_id, text=f"P_{i}^{n}")
                self._try_build_function()
    
    def _on_mousewheel(self, event: tk.Event) -> None:
        """Обработчик прокрутки колесика мыши."""
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _on_middle_press(self, event: tk.Event) -> None:
        """Обработчик нажатия средней кнопки мыши."""
        self.last_pan_x = event.x
        self.last_pan_y = event.y
    
    def _on_middle_drag(self, event: tk.Event) -> None:
        """Обработчик перетаскивания средней кнопкой мыши."""
        dx = event.x - self.last_pan_x
        dy = event.y - self.last_pan_y
        
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.last_pan_x = event.x
        self.last_pan_y = event.y
    
    def add_node(self, function_type: str, x: Optional[int] = None, 
                 y: Optional[int] = None) -> NodeWidget:
        """
        Добавляет узел на холст.
        
        Args:
            function_type: Тип функции
            x, y: Координаты (если None, то в центр)
            
        Returns:
            Созданный узел
        """
        if x is None or y is None:
            # Размещаем в центре видимой области
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2
        
        node = NodeWidget(
            self.canvas,
            x, y,
            function_type,
            on_select=self._on_node_select,
            on_drag=self._on_node_drag
        )
        
        self.nodes[node.node_id] = node
        return node
    
    def _on_node_select(self, node: NodeWidget) -> None:
        """Обработчик выбора узла."""
        if self.connection_mode and self.connection_source:
            # Создаем соединение
            if self.connection_source != node:
                self.add_connection(self.connection_source.node_id, node.node_id)
                self._try_build_function()
            self.connection_mode = False
            self.connection_source = None
            if self.selected_node:
                self.selected_node.deselect()
        else:
            if self.selected_node and self.selected_node != node:
                self.selected_node.deselect()
        
        self.selected_node = node
    
    def _on_node_drag(self, node: NodeWidget, dx: int, dy: int) -> None:
        """Обработчик перетаскивания узла."""
        # Обновляем все соединения с этим узлом
        for conn in self.connections:
            if conn.from_node == node or conn.to_node == node:
                conn.update()
    
    def delete_node(self, node_id: str) -> None:
        """Удаляет узел с холста."""
        if node_id in self.nodes:
            node = self.nodes[node_id]
            
            # Удаляем все соединения с этим узлом
            self.connections = [
                conn for conn in self.connections
                if conn.from_node != node and conn.to_node != node
            ]
            for conn in self.connections[:]:
                if conn.from_node == node or conn.to_node == node:
                    conn.delete()
                    self.connections.remove(conn)
            
            # Удаляем узел
            node.delete()
            del self.nodes[node_id]
            
            if self.selected_node == node:
                self.selected_node = None
    
    def add_connection(self, from_node_id: str, to_node_id: str) -> Optional[ConnectionLine]:
        """
        Добавляет соединение между узлами.
        
        Args:
            from_node_id: ID исходного узла
            to_node_id: ID целевого узла
            
        Returns:
            Созданное соединение или None
        """
        if from_node_id not in self.nodes or to_node_id not in self.nodes:
            return None
        
        from_node = self.nodes[from_node_id]
        to_node = self.nodes[to_node_id]
        
        # Проверка на дубликаты
        for conn in self.connections:
            if conn.from_node == from_node and conn.to_node == to_node:
                return conn
        
        conn = ConnectionLine(self.canvas, from_node, to_node)
        self.connections.append(conn)
        return conn
    
    def clear(self) -> None:
        """Очищает холст."""
        # Удаляем все узлы
        for node_id in list(self.nodes.keys()):
            self.delete_node(node_id)
        
        self.nodes.clear()
        self.connections.clear()
        self.node_data.clear()
        self.selected_node = None
        self.current_function = None
        self.connection_mode = False
        self.connection_source = None
    
    def get_selected_node(self) -> Optional[NodeWidget]:
        """Возвращает выбранный узел."""
        return self.selected_node
    
    def build_function(self) -> Optional[PrimitiveFunction]:
        """
        Строит функцию из узлов на холсте.
        
        Returns:
            Построенная функция или None
        """
        if not self.nodes:
            return None
        
        try:
            from core.prf import Zero, Successor, Constant, Projection, Composition, PrimitiveRecursion
            
            # Если только один узел - создаем простую функцию
            if len(self.nodes) == 1:
                node = list(self.nodes.values())[0]
                return self._node_to_function(node)
            
            # Ищем корневой узел (узел без входящих соединений)
            root_nodes = []
            for node in self.nodes.values():
                has_incoming = any(conn.to_node == node for conn in self.connections)
                if not has_incoming:
                    root_nodes.append(node)
            
            if len(root_nodes) == 1:
                # Есть один корневой узел - строим дерево
                return self._build_from_node(root_nodes[0])
            elif len(root_nodes) == 0:
                # Все узлы соединены - берем первый
                return self._build_from_node(list(self.nodes.values())[0])
            else:
                # Несколько корневых узлов - создаем композицию (упрощенно)
                # Пока возвращаем первый
                return self._build_from_node(root_nodes[0])
        
        except Exception as e:
            print(f"Ошибка построения функции: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _node_to_function(self, node: NodeWidget) -> PrimitiveFunction:
        """Преобразует узел в функцию."""
        from core.prf import Zero, Successor, Constant, Projection
        
        if node.function_type == "zero":
            return Zero()
        elif node.function_type == "successor":
            return Successor()
        elif node.function_type == "constant":
            value = self.node_data.get(node.node_id, {}).get("value", 0)
            arity = self.node_data.get(node.node_id, {}).get("arity", 0)
            return Constant(value, arity)
        elif node.function_type.startswith("projection"):
            # Извлекаем параметры из node_data или из типа
            if node.node_id in self.node_data:
                n = self.node_data[node.node_id].get("n", 1)
                i = self.node_data[node.node_id].get("i", 1)
            else:
                # Пытаемся извлечь из типа "projection_n_i"
                parts = node.function_type.split("_")
                if len(parts) >= 3:
                    n = int(parts[1])
                    i = int(parts[2])
                else:
                    n, i = 1, 1
            return Projection(n, i)
        else:
            # По умолчанию - Zero
            return Zero()
    
    def _build_from_node(self, node: NodeWidget) -> PrimitiveFunction:
        """Строит функцию начиная с узла."""
        from core.prf import Composition, PrimitiveRecursion
        
        # Получаем базовую функцию узла
        base_func = self._node_to_function(node)
        
        # Находим исходящие соединения
        outgoing = [conn for conn in self.connections if conn.from_node == node]
        
        if not outgoing:
            return base_func
        
        # Если это композиция или рекурсия
        if node.function_type == "composition":
            # Находим все узлы, соединенные с этим
            connected_nodes = [conn.to_node for conn in outgoing]
            g_list = [self._build_from_node(n) for n in connected_nodes]
            return Composition(base_func, g_list)
        
        elif node.function_type == "primitive_recursion":
            # Для рекурсии нужно два узла: g и h
            if len(outgoing) >= 2:
                g_node = outgoing[0].to_node
                h_node = outgoing[1].to_node
                g = self._build_from_node(g_node)
                h = self._build_from_node(h_node)
                return PrimitiveRecursion(g, h)
            elif len(outgoing) == 1:
                # Упрощенно - используем один узел для обоих
                g_node = outgoing[0].to_node
                g = self._build_from_node(g_node)
                # Для h используем ту же функцию (временное решение)
                return PrimitiveRecursion(g, g)
        
        # Для остальных случаев возвращаем базовую функцию
        return base_func
    
    def _try_build_function(self) -> None:
        """Пытается построить функцию и обновить current_function."""
        func = self.build_function()
        if func:
            self.current_function = func
            if self.on_function_change:
                self.on_function_change()
    
    def load_function(self, function: PrimitiveFunction) -> None:
        """
        Загружает функцию на холст для визуализации.
        
        Args:
            function: Функция для загрузки
        """
        self.clear()
        self.current_function = function
        # Здесь можно добавить логику визуализации структуры функции
        # Пока оставляем упрощенную версию

