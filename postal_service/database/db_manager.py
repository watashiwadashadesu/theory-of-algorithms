import sqlite3
import os
from datetime import datetime
from typing import List, Optional


class DatabaseManager:
    """Менеджер для работы с SQLite базой данных."""

    def __init__(self, db_path: str = "data/postal_service.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Инициализирует базу данных и создает таблицы."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Таблица для хранения почтовых отправлений
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS postal_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_type TEXT NOT NULL,
                    distance_km REAL NOT NULL,
                    weight_kg REAL NOT NULL,
                    volume_cubic_cm REAL,
                    delivery_type TEXT NOT NULL,
                    is_registered INTEGER,
                    is_fragile INTEGER,
                    calculated_price REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    details TEXT
                )
            ''')

            # Таблица для истории расчетов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS calculation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER,
                    calculation_type TEXT,
                    parameters TEXT,
                    result REAL,
                    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES postal_items (id)
                )
            ''')

            conn.commit()

    def save_postal_item(self, item) -> int:
        """Сохраняет почтовое отправление в базу данных."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Подготавливаем данные
            volume = getattr(item, 'volume_cubic_cm', None)
            is_registered = getattr(item, 'is_registered', None)
            is_fragile = getattr(item, 'is_fragile', None)

            # Сохраняем детали в JSON формате
            details = str(item.get_details()) if hasattr(item, 'get_details') else str(item)

            cursor.execute('''
                INSERT INTO postal_items 
                (item_type, distance_km, weight_kg, volume_cubic_cm, delivery_type, 
                 is_registered, is_fragile, calculated_price, details)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item.name,
                item.distance_km,
                item.weight_kg,
                volume,
                item.delivery_type,
                is_registered,
                is_fragile,
                item.price,
                details
            ))

            item_id = cursor.lastrowid
            conn.commit()
            return item_id

    def get_all_items(self) -> List[dict]:
        """Возвращает все сохраненные отправления."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM postal_items 
                ORDER BY created_at DESC
            ''')

            return [dict(row) for row in cursor.fetchall()]

    def get_items_by_type(self, item_type: str) -> List[dict]:
        """Возвращает отправления по типу."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM postal_items 
                WHERE item_type = ? 
                ORDER BY created_at DESC
            ''', (item_type,))

            return [dict(row) for row in cursor.fetchall()]

    def get_total_statistics(self) -> dict:
        """Возвращает общую статистику по всем отправлениям."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Общее количество отправлений
            cursor.execute('SELECT COUNT(*) FROM postal_items')
            total_count = cursor.fetchone()[0]

            # Общая стоимость
            cursor.execute('SELECT SUM(calculated_price) FROM postal_items')
            total_cost = cursor.fetchone()[0] or 0

            # Количество по типам
            cursor.execute('''
                SELECT item_type, COUNT(*) 
                FROM postal_items 
                GROUP BY item_type
            ''')
            type_counts = dict(cursor.fetchall())

            return {
                'total_count': total_count,
                'total_cost': round(total_cost, 2),
                'type_counts': type_counts,
                'average_cost': round(total_cost / total_count, 2) if total_count > 0 else 0
            }

    def clear_database(self):
        """Очищает базу данных (для тестов)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM postal_items')
            cursor.execute('DELETE FROM calculation_history')
            conn.commit()