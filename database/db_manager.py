"""
Модуль для управления базой данных SQLite.

Обеспечивает сохранение, загрузку и поиск функций и истории вычислений.
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import shutil


class DatabaseManager:
    """Менеджер базы данных для PRF Constructor."""
    
    def __init__(self, db_path: str = "prf_constructor.db"):
        """
        Args:
            db_path: Путь к файлу базы данных
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self._initialize_database()
    
    def _initialize_database(self) -> None:
        """Инициализирует базу данных и создает таблицы."""
        schema_path = Path(__file__).parent / "schema.sql"
        
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
        
        # Читаем и выполняем схему
        if schema_path.exists():
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = f.read()
            self.conn.executescript(schema)
        else:
            # Создаем таблицы программно, если schema.sql не найден
            self._create_tables()
        
        self.conn.commit()
    
    def _create_tables(self) -> None:
        """Создает таблицы базы данных."""
        cursor = self.conn.cursor()
        
        # Таблица функций
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS functions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                definition TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                description TEXT
            )
        """)
        
        # Таблица истории
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                function_id INTEGER,
                arguments TEXT NOT NULL,
                result TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(function_id) REFERENCES functions(id) ON DELETE CASCADE
            )
        """)
        
        # Таблица примитивов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS primitives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                arity INTEGER,
                proj_index INTEGER,
                name TEXT
            )
        """)
        
        # Индексы
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_functions_name ON functions(name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_history_function_id ON history(function_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_history_timestamp ON history(timestamp)")
    
    def save_function(self, name: str, definition: Dict[str, Any], 
                     description: Optional[str] = None) -> int:
        """
        Сохраняет функцию в базу данных.
        
        Args:
            name: Имя функции
            definition: Определение функции (словарь)
            description: Описание функции
            
        Returns:
            ID сохраненной функции
            
        Raises:
            sqlite3.IntegrityError: Если функция с таким именем уже существует
        """
        cursor = self.conn.cursor()
        definition_json = json.dumps(definition, ensure_ascii=False)
        
        try:
            cursor.execute("""
                INSERT INTO functions (name, definition, description)
                VALUES (?, ?, ?)
            """, (name, definition_json, description))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Обновляем существующую функцию
            cursor.execute("""
                UPDATE functions 
                SET definition = ?, description = ?, created_at = CURRENT_TIMESTAMP
                WHERE name = ?
            """, (definition_json, description, name))
            self.conn.commit()
            cursor.execute("SELECT id FROM functions WHERE name = ?", (name,))
            row = cursor.fetchone()
            return row[0] if row else None
    
    def load_function(self, function_id: Optional[int] = None, 
                     name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Загружает функцию из базы данных.
        
        Args:
            function_id: ID функции
            name: Имя функции
            
        Returns:
            Словарь с данными функции или None, если не найдена
        """
        cursor = self.conn.cursor()
        
        if function_id:
            cursor.execute("SELECT * FROM functions WHERE id = ?", (function_id,))
        elif name:
            cursor.execute("SELECT * FROM functions WHERE name = ?", (name,))
        else:
            return None
        
        row = cursor.fetchone()
        if row:
            return {
                "id": row["id"],
                "name": row["name"],
                "definition": json.loads(row["definition"]),
                "created_at": row["created_at"],
                "description": row["description"]
            }
        return None
    
    def list_functions(self) -> List[Dict[str, Any]]:
        """
        Возвращает список всех функций.
        
        Returns:
            Список словарей с данными функций
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM functions ORDER BY name")
        rows = cursor.fetchall()
        
        return [
            {
                "id": row["id"],
                "name": row["name"],
                "definition": json.loads(row["definition"]),
                "created_at": row["created_at"],
                "description": row["description"]
            }
            for row in rows
        ]
    
    def delete_function(self, function_id: Optional[int] = None, 
                       name: Optional[str] = None) -> bool:
        """
        Удаляет функцию из базы данных.
        
        Args:
            function_id: ID функции
            name: Имя функции
            
        Returns:
            True, если функция была удалена
        """
        cursor = self.conn.cursor()
        
        if function_id:
            cursor.execute("DELETE FROM functions WHERE id = ?", (function_id,))
        elif name:
            cursor.execute("DELETE FROM functions WHERE name = ?", (name,))
        else:
            return False
        
        self.conn.commit()
        return cursor.rowcount > 0
    
    def search_functions(self, query: str) -> List[Dict[str, Any]]:
        """
        Ищет функции по имени.
        
        Args:
            query: Поисковый запрос
            
        Returns:
            Список найденных функций
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM functions WHERE name LIKE ? ORDER BY name",
            (f"%{query}%",)
        )
        rows = cursor.fetchall()
        
        return [
            {
                "id": row["id"],
                "name": row["name"],
                "definition": json.loads(row["definition"]),
                "created_at": row["created_at"],
                "description": row["description"]
            }
            for row in rows
        ]
    
    def save_history(self, function_id: int, arguments: List[int], result: int) -> int:
        """
        Сохраняет запись в историю вычислений.
        
        Args:
            function_id: ID функции
            arguments: Аргументы
            result: Результат
            
        Returns:
            ID записи истории
        """
        cursor = self.conn.cursor()
        args_json = json.dumps(arguments)
        
        cursor.execute("""
            INSERT INTO history (function_id, arguments, result)
            VALUES (?, ?, ?)
        """, (function_id, args_json, str(result)))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_history(self, function_id: Optional[int] = None, 
                   limit: int = 100) -> List[Dict[str, Any]]:
        """
        Возвращает историю вычислений.
        
        Args:
            function_id: ID функции (None для всех функций)
            limit: Максимальное количество записей
            
        Returns:
            Список записей истории
        """
        cursor = self.conn.cursor()
        
        if function_id:
            cursor.execute("""
                SELECT h.*, f.name as function_name
                FROM history h
                LEFT JOIN functions f ON h.function_id = f.id
                WHERE h.function_id = ?
                ORDER BY h.timestamp DESC
                LIMIT ?
            """, (function_id, limit))
        else:
            cursor.execute("""
                SELECT h.*, f.name as function_name
                FROM history h
                LEFT JOIN functions f ON h.function_id = f.id
                ORDER BY h.timestamp DESC
                LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        
        return [
            {
                "id": row["id"],
                "function_id": row["function_id"],
                "function_name": row["function_name"],
                "arguments": json.loads(row["arguments"]),
                "result": row["result"],
                "timestamp": row["timestamp"]
            }
            for row in rows
        ]
    
    def backup_database(self, backup_path: str) -> bool:
        """
        Создает резервную копию базы данных.
        
        Args:
            backup_path: Путь для сохранения резервной копии
            
        Returns:
            True, если копия создана успешно
        """
        try:
            if self.conn:
                self.conn.close()
            shutil.copy2(self.db_path, backup_path)
            self._initialize_database()
            return True
        except Exception as e:
            print(f"Backup failed: {e}")
            return False
    
    def export_functions(self, export_path: str) -> bool:
        """
        Экспортирует все функции в JSON файл.
        
        Args:
            export_path: Путь для сохранения экспорта
            
        Returns:
            True, если экспорт успешен
        """
        try:
            functions = self.list_functions()
            export_data = {
                "export_date": datetime.now().isoformat(),
                "functions": functions
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False
    
    def import_functions(self, import_path: str) -> int:
        """
        Импортирует функции из JSON файла.
        
        Args:
            import_path: Путь к файлу импорта
            
        Returns:
            Количество импортированных функций
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            count = 0
            for func_data in import_data.get("functions", []):
                try:
                    self.save_function(
                        func_data["name"],
                        func_data["definition"],
                        func_data.get("description")
                    )
                    count += 1
                except Exception as e:
                    print(f"Failed to import function {func_data.get('name')}: {e}")
            
            return count
        except Exception as e:
            print(f"Import failed: {e}")
            return 0
    
    def close(self) -> None:
        """Закрывает соединение с базой данных."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def __del__(self):
        """Деструктор - закрывает соединение."""
        self.close()

