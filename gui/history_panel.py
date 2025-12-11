"""
Панель истории операций и вычислений.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any, Optional
from datetime import datetime


class HistoryPanel(ttk.Frame):
    """Панель истории вычислений."""
    
    def __init__(self, parent):
        """
        Args:
            parent: Родительский виджет
        """
        super().__init__(parent)
        
        # Заголовок
        title_label = ttk.Label(self, text="История вычислений", font=("Arial", 12, "bold"))
        title_label.pack(pady=5)
        
        # Список истории
        self.tree = ttk.Treeview(
            self,
            columns=("function", "arguments", "result", "timestamp"),
            show="headings",
            height=10
        )
        
        # Настройка колонок
        self.tree.heading("function", text="Функция")
        self.tree.heading("arguments", text="Аргументы")
        self.tree.heading("result", text="Результат")
        self.tree.heading("timestamp", text="Время")
        
        self.tree.column("function", width=150)
        self.tree.column("arguments", width=100)
        self.tree.column("result", width=100)
        self.tree.column("timestamp", width=150)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещение
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_entry(self, function_name: str, arguments: List[int], result: int) -> None:
        """
        Добавляет запись в историю.
        
        Args:
            function_name: Имя функции
            arguments: Аргументы
            result: Результат
        """
        args_str = ", ".join(str(a) for a in arguments)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.tree.insert(
            "",
            "end",
            values=(function_name, args_str, str(result), timestamp)
        )
        
        # Прокрутка к последней записи
        children = self.tree.get_children()
        if children:
            self.tree.see(children[-1])
    
    def load_history(self, history: List[Dict[str, Any]]) -> None:
        """
        Загружает историю из базы данных.
        
        Args:
            history: Список записей истории
        """
        # Очищаем текущую историю
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавляем записи
        for entry in history:
            function_name = entry.get("function_name", "Unknown")
            arguments = entry.get("arguments", [])
            result = entry.get("result", "")
            timestamp = entry.get("timestamp", "")
            
            args_str = ", ".join(str(a) for a in arguments) if isinstance(arguments, list) else str(arguments)
            
            self.tree.insert(
                "",
                "end",
                values=(function_name, args_str, str(result), timestamp)
            )
    
    def clear(self) -> None:
        """Очищает историю."""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def get_selected_entry(self) -> Optional[Dict[str, Any]]:
        """
        Возвращает выбранную запись.
        
        Returns:
            Словарь с данными записи или None
        """
        selection = self.tree.selection()
        if not selection:
            return None
        
        item = self.tree.item(selection[0])
        values = item["values"]
        
        if len(values) >= 4:
            return {
                "function": values[0],
                "arguments": values[1],
                "result": values[2],
                "timestamp": values[3]
            }
        
        return None

