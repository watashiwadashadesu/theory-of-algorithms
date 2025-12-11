"""
Главное окно приложения PRF Constructor.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Dict, Any, List
import json

from core.prf import PrimitiveFunction, function_from_dict, create_addition, create_multiplication, create_factorial
from core.evaluator import Evaluator
from core.validator import Validator
from database.db_manager import DatabaseManager
from gui.canvas_widget import CanvasWidget
from gui.history_panel import HistoryPanel
from gui.dialogs import FunctionDialog, LoadFunctionDialog, SettingsDialog, show_about_dialog, show_help_dialog
from utils.exporter import export_to_latex, export_to_json


class MainWindow:
    """Главное окно приложения."""
    
    def __init__(self):
        """Инициализирует главное окно."""
        self.root = tk.Tk()
        self.root.title("PRF Constructor - Визуальный конструктор примитивно-рекурсивных функций")
        self.root.geometry("1200x800")
        
        # Менеджер базы данных
        self.db_manager = DatabaseManager()
        
        # Вычислитель
        self.evaluator = Evaluator()
        
        # Текущая функция
        self.current_function: Optional[PrimitiveFunction] = None
        self.current_function_name: Optional[str] = None
        self.current_function_id: Optional[int] = None
        
        # Настройки
        self.settings = {
            "max_depth": 300000,
            "max_steps": 100000000
        }
        
        self._create_menu()
        self._create_toolbar()
        self._create_main_layout()
        self._create_status_bar()
        
        # Загружаем историю
        self._refresh_history()
    
    def _create_menu(self) -> None:
        """Создает меню приложения."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новая функция", command=self._new_function, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Сохранить функцию", command=self._save_function, accelerator="Ctrl+S")
        file_menu.add_command(label="Загрузить функцию", command=self._load_function, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Экспорт в JSON", command=self._export_json)
        file_menu.add_command(label="Экспорт в LaTeX", command=self._export_latex)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self._on_exit, accelerator="Ctrl+Q")
        
        # Меню "Правка"
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Отменить", command=self._undo, accelerator="Ctrl+Z", state="disabled")
        edit_menu.add_command(label="Повторить", command=self._redo, accelerator="Ctrl+Y", state="disabled")
        edit_menu.add_separator()
        edit_menu.add_command(label="Очистить", command=self._clear_canvas)
        
        # Меню "Вычисление"
        compute_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вычисление", menu=compute_menu)
        compute_menu.add_command(label="Вычислить", command=self._compute_function, accelerator="F5")
        compute_menu.add_command(label="Пошаговое вычисление", command=self._step_compute, accelerator="F6")
        
        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="Справка", command=lambda: show_help_dialog(self.root))
        help_menu.add_command(label="О программе", command=lambda: show_about_dialog(self.root))
        
        # Горячие клавиши
        self.root.bind("<Control-n>", lambda e: self._new_function())
        self.root.bind("<Control-s>", lambda e: self._save_function())
        self.root.bind("<Control-o>", lambda e: self._load_function())
        self.root.bind("<Control-q>", lambda e: self._on_exit())
        self.root.bind("<F5>", lambda e: self._compute_function())
        self.root.bind("<F6>", lambda e: self._step_compute())
    
    def _create_toolbar(self) -> None:
        """Создает панель инструментов."""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side="top", fill="x", padx=5, pady=5)
        
        # Кнопки для базовых функций
        ttk.Label(toolbar, text="Базовые функции:").pack(side="left", padx=5)
        
        ttk.Button(toolbar, text="Z(x)", command=lambda: self._add_primitive("zero")).pack(side="left", padx=2)
        ttk.Button(toolbar, text="S(x)", command=lambda: self._add_primitive("successor")).pack(side="left", padx=2)
        ttk.Button(toolbar, text="P", command=lambda: self._add_primitive("projection")).pack(side="left", padx=2)
        
        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=5)
        
        # Кнопки для операторов
        ttk.Label(toolbar, text="Операторы:").pack(side="left", padx=5)
        ttk.Button(toolbar, text="Composition", command=lambda: self._add_primitive("composition")).pack(side="left", padx=2)
        ttk.Button(toolbar, text="Recursion", command=lambda: self._add_primitive("primitive_recursion")).pack(side="left", padx=2)
        
        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=5)
        
        # Кнопка построения функции
        ttk.Button(toolbar, text="Построить функцию", command=self._build_function_from_nodes).pack(side="left", padx=5)
        
        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=5)
        
        # Предопределенные функции
        ttk.Label(toolbar, text="Примеры:").pack(side="left", padx=5)
        ttk.Button(toolbar, text="add(x,y)", command=self._load_predefined_addition).pack(side="left", padx=2)
        ttk.Button(toolbar, text="mult(x,y)", command=self._load_predefined_multiplication).pack(side="left", padx=2)
        ttk.Button(toolbar, text="fact(x)", command=self._load_predefined_factorial).pack(side="left", padx=2)
    
    def _create_main_layout(self) -> None:
        """Создает основную компоновку окна."""
        # Главный контейнер
        main_container = ttk.PanedWindow(self.root, orient="horizontal")
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Левая панель - холст
        left_panel = ttk.Frame(main_container)
        main_container.add(left_panel, weight=3)
        
        # Холст для построения функций
        canvas_label = ttk.Label(left_panel, text="Рабочая область", font=("Arial", 10, "bold"))
        canvas_label.pack(pady=5)
        
        self.canvas_widget = CanvasWidget(left_panel, on_function_change=self._on_function_change)
        self.canvas_widget.pack(fill="both", expand=True)
        
        # Правая панель - параметры и вычисления
        right_panel = ttk.PanedWindow(main_container, orient="vertical")
        main_container.add(right_panel, weight=1)
        
        # Панель параметров
        params_frame = ttk.LabelFrame(right_panel, text="Параметры функции", padding=10)
        right_panel.add(params_frame, weight=1)
        
        ttk.Label(params_frame, text="Тип:").grid(row=0, column=0, sticky="w", pady=2)
        self.function_type_label = ttk.Label(params_frame, text="Не выбрано")
        self.function_type_label.grid(row=0, column=1, sticky="w", pady=2)
        
        ttk.Label(params_frame, text="Арность:").grid(row=1, column=0, sticky="w", pady=2)
        self.arity_label = ttk.Label(params_frame, text="-")
        self.arity_label.grid(row=1, column=1, sticky="w", pady=2)
        
        # Панель вычислений
        compute_frame = ttk.LabelFrame(right_panel, text="Вычисление", padding=10)
        right_panel.add(compute_frame, weight=1)
        
        ttk.Label(compute_frame, text="Аргументы (через запятую):").pack(anchor="w", pady=2)
        self.args_entry = ttk.Entry(compute_frame, width=30)
        self.args_entry.pack(fill="x", pady=2)
        self.args_entry.bind("<Return>", lambda e: self._compute_function())
        
        ttk.Button(compute_frame, text="Вычислить", command=self._compute_function).pack(pady=5)
        
        ttk.Label(compute_frame, text="Результат:").pack(anchor="w", pady=2)
        self.result_text = tk.Text(compute_frame, height=5, width=30, wrap="word")
        self.result_text.pack(fill="both", expand=True, pady=2)
        
        # Панель истории
        history_frame = ttk.LabelFrame(right_panel, text="История", padding=10)
        right_panel.add(history_frame, weight=1)
        
        self.history_panel = HistoryPanel(history_frame)
        self.history_panel.pack(fill="both", expand=True)
    
    def _create_status_bar(self) -> None:
        """Создает строку состояния."""
        self.status_bar = ttk.Label(self.root, text="Готов", relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")
    
    def _update_status(self, message: str) -> None:
        """Обновляет строку состояния."""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def _add_primitive(self, function_type: str) -> None:
        """Добавляет примитивную функцию на холст."""
        self.canvas_widget.add_node(function_type)
        self._update_status(f"Добавлена функция: {function_type}")
    
    def _load_predefined_addition(self) -> None:
        """Загружает предопределенную функцию сложения."""
        try:
            func = create_addition()
            self.current_function = func
            self.current_function_name = "addition"
            self.canvas_widget.load_function(func)
            self._update_function_info()
            self._update_status("Загружена функция сложения")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить функцию: {e}")
    
    def _load_predefined_multiplication(self) -> None:
        """Загружает предопределенную функцию умножения."""
        try:
            func = create_multiplication()
            self.current_function = func
            self.current_function_name = "multiplication"
            self.canvas_widget.load_function(func)
            self._update_function_info()
            self._update_status("Загружена функция умножения")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить функцию: {e}")
    
    def _load_predefined_factorial(self) -> None:
        """Загружает предопределенную функцию факториала."""
        try:
            func = create_factorial()
            self.current_function = func
            self.current_function_name = "factorial"
            self.canvas_widget.load_function(func)
            self._update_function_info()
            self._update_status("Загружена функция факториала")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить функцию: {e}")
    
    def _update_function_info(self) -> None:
        """Обновляет информацию о функции в панели параметров."""
        if self.current_function:
            func_type = type(self.current_function).__name__
            arity = self.current_function.arity()
            
            self.function_type_label.config(text=func_type)
            self.arity_label.config(text=str(arity))
        else:
            self.function_type_label.config(text="Не выбрано")
            self.arity_label.config(text="-")
    
    def _on_function_change(self) -> None:
        """Обработчик изменения функции на холсте."""
        # Пытаемся построить функцию из узлов
        func = self.canvas_widget.build_function()
        if func:
            self.current_function = func
            self._update_function_info()
            self._update_status("Функция построена из узлов")
    
    def _build_function_from_nodes(self) -> None:
        """Строит функцию из узлов на холсте."""
        func = self.canvas_widget.build_function()
        if func:
            self.current_function = func
            self._update_function_info()
            self._update_status("Функция построена из узлов")
            messagebox.showinfo("Успех", f"Функция построена! Тип: {type(func).__name__}, Арность: {func.arity()}")
        else:
            messagebox.showwarning("Предупреждение", "Не удалось построить функцию. Убедитесь, что узлы правильно соединены.")
    
    def _compute_function(self) -> None:
        """Вычисляет функцию с заданными аргументами."""
        # Пытаемся построить функцию из узлов, если её нет
        if not self.current_function:
            func = self.canvas_widget.build_function()
            if func:
                self.current_function = func
                self._update_function_info()
            else:
                messagebox.showwarning("Предупреждение", "Функция не выбрана. Постройте функцию из узлов или загрузите готовую.")
                return
        
        if not self.current_function:
            messagebox.showwarning("Предупреждение", "Функция не выбрана")
            return
        
        # Парсим аргументы
        args_str = self.args_entry.get().strip()
        if not args_str:
            messagebox.showwarning("Предупреждение", "Введите аргументы")
            return
        
        try:
            args = [int(x.strip()) for x in args_str.split(",")]
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат аргументов")
            return
        
        # Валидация аргументов
        from core.validator import Validator
        error = Validator.validate_arguments(self.current_function, args)
        if error:
            messagebox.showerror("Ошибка", error)
            return
        
        # Вычисление
        try:
            self.evaluator.max_depth = self.settings["max_depth"]
            self.evaluator.max_steps = self.settings["max_steps"]
            
            result = self.evaluator.evaluate(self.current_function, args, track_steps=False)
            
            # Выводим результат
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", f"Результат: {result}\n\n")
            
            # Статистика
            stats = self.evaluator.get_statistics()
            self.result_text.insert("end", f"Шагов: {stats['total_steps']}\n")
            self.result_text.insert("end", f"Глубина: {stats['max_depth']}\n")
            
            # Предупреждения
            warnings = self.evaluator.get_warnings()
            if warnings:
                self.result_text.insert("end", f"\nПредупреждения:\n")
                for warning in warnings:
                    self.result_text.insert("end", f"  - {warning}\n")
            
            # Сохраняем в историю
            if self.current_function_id:
                self.db_manager.save_history(self.current_function_id, args, result)
                self._refresh_history()
            
            # Добавляем в панель истории
            func_name = self.current_function_name or "Unknown"
            self.history_panel.add_entry(func_name, args, result)
            
            self._update_status(f"Вычислено: {result}")
        
        except RecursionError as e:
            messagebox.showerror("Ошибка", f"Превышена максимальная глубина рекурсии: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка вычисления: {e}")
    
    def _step_compute(self) -> None:
        """Пошаговое вычисление функции."""
        # Упрощенная версия - можно расширить
        self._compute_function()
    
    def _save_function(self) -> None:
        """Сохраняет текущую функцию в базу данных."""
        if not self.current_function:
            messagebox.showwarning("Предупреждение", "Нет функции для сохранения")
            return
        
        # Валидация
        errors = Validator.validate(self.current_function)
        if errors:
            messagebox.showerror("Ошибка", f"Функция некорректна:\n" + "\n".join(errors))
            return
        
        # Диалог сохранения
        dialog = FunctionDialog(
            self.root,
            function_name=self.current_function_name or "",
            description="",
            on_save=None
        )
        
        result = dialog.show()
        if result:
            try:
                func_dict = self.current_function.to_dict()
                func_id = self.db_manager.save_function(
                    result["name"],
                    func_dict,
                    result["description"]
                )
                
                self.current_function_name = result["name"]
                self.current_function_id = func_id
                
                self._update_status(f"Функция '{result['name']}' сохранена")
                messagebox.showinfo("Успех", "Функция успешно сохранена")
            
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить функцию: {e}")
    
    def _load_function(self) -> None:
        """Загружает функцию из базы данных."""
        functions = self.db_manager.list_functions()
        
        if not functions:
            messagebox.showinfo("Информация", "В базе данных нет сохраненных функций")
            return
        
        dialog = LoadFunctionDialog(self.root, functions, on_load=None)
        function_name = dialog.show()
        
        if function_name:
            try:
                func_data = self.db_manager.load_function(name=function_name)
                if func_data:
                    self.current_function = function_from_dict(func_data["definition"])
                    self.current_function_name = func_data["name"]
                    self.current_function_id = func_data["id"]
                    
                    self.canvas_widget.load_function(self.current_function)
                    self._update_function_info()
                    self._refresh_history()
                    
                    self._update_status(f"Функция '{function_name}' загружена")
                    messagebox.showinfo("Успех", "Функция успешно загружена")
                else:
                    messagebox.showerror("Ошибка", "Функция не найдена")
            
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить функцию: {e}")
    
    def _new_function(self) -> None:
        """Создает новую функцию."""
        self.canvas_widget.clear()
        self.current_function = None
        self.current_function_name = None
        self.current_function_id = None
        self._update_function_info()
        self.result_text.delete("1.0", "end")
        self.args_entry.delete(0, "end")
        self._update_status("Создана новая функция")
    
    def _clear_canvas(self) -> None:
        """Очищает холст."""
        if messagebox.askyesno("Подтверждение", "Очистить рабочую область?"):
            self.canvas_widget.clear()
            self.current_function = None
            self._update_function_info()
            self._update_status("Холст очищен")
    
    def _export_json(self) -> None:
        """Экспортирует функцию в JSON."""
        if not self.current_function:
            messagebox.showwarning("Предупреждение", "Нет функции для экспорта")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                func_dict = self.current_function.to_dict()
                export_data = {
                    "name": self.current_function_name or "function",
                    "definition": func_dict
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                self._update_status(f"Функция экспортирована в {filename}")
                messagebox.showinfo("Успех", "Функция успешно экспортирована")
            
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать функцию: {e}")
    
    def _export_latex(self) -> None:
        """Экспортирует функцию в LaTeX."""
        if not self.current_function:
            messagebox.showwarning("Предупреждение", "Нет функции для экспорта")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".tex",
            filetypes=[("LaTeX files", "*.tex"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                latex_code = export_to_latex(self.current_function, self.current_function_name)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(latex_code)
                
                self._update_status(f"Функция экспортирована в LaTeX: {filename}")
                messagebox.showinfo("Успех", "Функция успешно экспортирована в LaTeX")
            
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать функцию: {e}")
    
    def _refresh_history(self) -> None:
        """Обновляет панель истории."""
        if self.current_function_id:
            history = self.db_manager.get_history(function_id=self.current_function_id, limit=50)
            self.history_panel.load_history(history)
        else:
            history = self.db_manager.get_history(limit=50)
            self.history_panel.load_history(history)
    
    def _undo(self) -> None:
        """Отменяет последнее действие."""
        # TODO: Реализовать систему отмены/повтора
        pass
    
    def _redo(self) -> None:
        """Повторяет последнее действие."""
        # TODO: Реализовать систему отмены/повтора
        pass
    
    def _on_exit(self) -> None:
        """Обработчик выхода из приложения."""
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.db_manager.close()
            self.root.quit()
    
    def run(self) -> None:
        """Запускает главный цикл приложения."""
        self.root.mainloop()

