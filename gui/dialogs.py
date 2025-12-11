"""
Диалоговые окна для PRF Constructor.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from typing import Optional, List, Dict, Any, Callable
import json


class FunctionDialog:
    """Диалог создания/редактирования функции."""
    
    def __init__(self, parent, function_name: str = "", 
                 description: str = "", on_save: Optional[Callable] = None):
        """
        Args:
            parent: Родительское окно
            function_name: Имя функции (для редактирования)
            description: Описание функции
            on_save: Callback при сохранении
        """
        self.result = None
        self.on_save = on_save
        
        # Создаем модальное окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Сохранить функцию" if function_name else "Новая функция")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Поля ввода
        ttk.Label(self.dialog, text="Имя функции:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(self.dialog, width=30)
        self.name_entry.insert(0, function_name)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text="Описание:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.desc_text = tk.Text(self.dialog, width=30, height=5)
        self.desc_text.insert("1.0", description)
        self.desc_text.grid(row=1, column=1, padx=5, pady=5)
        
        # Кнопки
        button_frame = ttk.Frame(self.dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Сохранить", command=self._on_save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Отмена", command=self._on_cancel).pack(side="left", padx=5)
        
        # Фокус на поле имени
        self.name_entry.focus()
        
        # Обработка Enter
        self.dialog.bind("<Return>", lambda e: self._on_save())
        self.dialog.bind("<Escape>", lambda e: self._on_cancel())
    
    def _on_save(self) -> None:
        """Обработчик сохранения."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Имя функции не может быть пустым")
            return
        
        description = self.desc_text.get("1.0", "end-1c").strip()
        
        self.result = {
            "name": name,
            "description": description
        }
        
        if self.on_save:
            self.on_save(name, description)
        
        self.dialog.destroy()
    
    def _on_cancel(self) -> None:
        """Обработчик отмены."""
        self.dialog.destroy()
    
    def show(self) -> Optional[Dict[str, str]]:
        """
        Показывает диалог и возвращает результат.
        
        Returns:
            Словарь с name и description или None
        """
        self.dialog.wait_window()
        return self.result


class LoadFunctionDialog:
    """Диалог загрузки функции из базы данных."""
    
    def __init__(self, parent, functions: List[Dict[str, Any]], 
                 on_load: Optional[Callable] = None):
        """
        Args:
            parent: Родительское окно
            functions: Список функций из базы данных
            on_load: Callback при загрузке
        """
        self.result = None
        self.on_load = on_load
        
        # Создаем модальное окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Загрузить функцию")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.geometry("500x400")
        
        # Список функций
        ttk.Label(self.dialog, text="Выберите функцию:").pack(pady=5)
        
        frame = ttk.Frame(self.dialog)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Treeview для списка функций
        self.tree = ttk.Treeview(frame, columns=("description",), show="tree headings", height=10)
        self.tree.heading("#0", text="Имя функции")
        self.tree.heading("description", text="Описание")
        self.tree.column("#0", width=200)
        self.tree.column("description", width=250)
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Заполняем список
        for func in functions:
            desc = func.get("description", "") or ""
            self.tree.insert("", "end", text=func["name"], values=(desc,))
        
        # Кнопки
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Загрузить", command=self._on_load).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Отмена", command=self._on_cancel).pack(side="left", padx=5)
        
        # Двойной клик для загрузки
        self.tree.bind("<Double-1>", lambda e: self._on_load())
    
    def _on_load(self) -> None:
        """Обработчик загрузки."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите функцию для загрузки")
            return
        
        function_name = self.tree.item(selection[0])["text"]
        self.result = function_name
        
        if self.on_load:
            self.on_load(function_name)
        
        self.dialog.destroy()
    
    def _on_cancel(self) -> None:
        """Обработчик отмены."""
        self.dialog.destroy()
    
    def show(self) -> Optional[str]:
        """
        Показывает диалог и возвращает имя выбранной функции.
        
        Returns:
            Имя функции или None
        """
        self.dialog.wait_window()
        return self.result


class SettingsDialog:
    """Диалог настроек приложения."""
    
    def __init__(self, parent, current_settings: Optional[Dict[str, Any]] = None):
        """
        Args:
            parent: Родительское окно
            current_settings: Текущие настройки
        """
        self.result = None
        current_settings = current_settings or {}
        
        # Создаем модальное окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Настройки")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Настройки вычислений
        ttk.Label(self.dialog, text="Максимальная глубина рекурсии:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.max_depth_var = tk.StringVar(value=str(current_settings.get("max_depth", 1000)))
        ttk.Entry(self.dialog, textvariable=self.max_depth_var, width=20).grid(
            row=0, column=1, padx=5, pady=5
        )
        
        ttk.Label(self.dialog, text="Максимальное количество шагов:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.max_steps_var = tk.StringVar(value=str(current_settings.get("max_steps", 100000)))
        ttk.Entry(self.dialog, textvariable=self.max_steps_var, width=20).grid(
            row=1, column=1, padx=5, pady=5
        )
        
        # Кнопки
        button_frame = ttk.Frame(self.dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Сохранить", command=self._on_save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Отмена", command=self._on_cancel).pack(side="left", padx=5)
    
    def _on_save(self) -> None:
        """Обработчик сохранения."""
        try:
            max_depth = int(self.max_depth_var.get())
            max_steps = int(self.max_steps_var.get())
            
            if max_depth < 1 or max_steps < 1:
                raise ValueError("Values must be positive")
            
            self.result = {
                "max_depth": max_depth,
                "max_steps": max_steps
            }
            
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")
    
    def _on_cancel(self) -> None:
        """Обработчик отмены."""
        self.dialog.destroy()
    
    def show(self) -> Optional[Dict[str, int]]:
        """
        Показывает диалог и возвращает настройки.
        
        Returns:
            Словарь с настройками или None
        """
        self.dialog.wait_window()
        return self.result


def show_about_dialog(parent) -> None:
    """Показывает диалог "О программе"."""
    about_text = """PRF Constructor
Визуальный конструктор примитивно-рекурсивных функций

Версия: 1.0
Лицензия: MIT License

Разработано для изучения теории вычислимости
и примитивно-рекурсивных функций."""
    
    messagebox.showinfo("О программе", about_text)


def show_help_dialog(parent) -> None:
    """Показывает диалог справки."""
    help_text = """Руководство пользователя PRF Constructor

1. Создание функций:
   - Используйте кнопки на панели инструментов для добавления базовых функций
   - Перетаскивайте узлы для изменения их позиции
   - Соединяйте узлы для создания композиций

2. Вычисление:
   - Введите аргументы в поле "Аргументы"
   - Нажмите "Вычислить" для получения результата

3. Сохранение:
   - Используйте меню "Файл" -> "Сохранить функцию"
   - Функции сохраняются в локальную базу данных SQLite

4. Загрузка:
   - Используйте меню "Файл" -> "Загрузить функцию"
   - Выберите функцию из списка

Для получения дополнительной информации см. README.md"""
    
    messagebox.showinfo("Справка", help_text)

