from PySide6.QtWidgets import QApplication
from ui import AppUI
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = AppUI()
    wnd.setWindowTitle("Лабораторная №4 — Генераторы")
    wnd.resize(500, 300)
    wnd.show()
    sys.exit(app.exec())
