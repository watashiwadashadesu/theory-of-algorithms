"""
Модуль для работы с БД в десктопном приложении.
Использует общую логику из shared/database.py
"""
import logging
from pathlib import Path
from datetime import datetime

# Импортируем из shared
from shared.database import BookClubManager as BaseBookClubManager
from shared.database import Book
from shared.exceptions import BookError, BookValidationError, BookNotFoundError

# Настройка логирования для десктопного приложения
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
log_file = LOG_DIR / f"book_club_desktop_{datetime.now().strftime('%Y%m')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)


# Создаем собственный менеджер для десктопного приложения
# который наследует от общего менеджера
class BookClubManager(BaseBookClubManager):
    """Менеджер книжного клуба для десктопного приложения."""

    def __init__(self, db_path: str = "book_club.db"):
        super().__init__(db_path)
        logging.getLogger(__name__).info(f"Десктопный менеджер инициализирован с БД: {db_path}")

    # Можно добавить специфичные для десктопного приложения методы
    def backup_database(self, backup_path: str = None):
        """Создает резервную копию базы данных."""
        import shutil
        from datetime import datetime

        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_book_club_{timestamp}.db"

        shutil.copy2(self.db.db_path, backup_path)
        logging.info(f"Создана резервная копия БД: {backup_path}")
        return backup_path