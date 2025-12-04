"""
Альтернативная точка входа для десктопного приложения.
Для запуска используйте: python main.py
Или используйте run_desktop.py для большей гибкости.
"""
import sys
from PySide6.QtWidgets import QApplication
from app.views.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    sys.exit(app.exec())