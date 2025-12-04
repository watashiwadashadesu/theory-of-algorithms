from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTabWidget, QLineEdit, QTextEdit
from generators import circle_area_generator, email_generator
from filters import filter_two_digits
import itertools


class AppUI(QTabWidget):
    def __init__(self):
        super().__init__()

        self.addTab(self.circle_tab(), "Площади кругов")
        self.addTab(self.email_tab(), "Email генератор")
        self.addTab(self.filter_tab(), "Фильтрация чисел")

    def circle_tab(self):
        w = QWidget()
        layout = QVBoxLayout()

        btn = QPushButton("Показать первые 5 значений")
        output = QLabel()

        def show():
            gen = circle_area_generator()
            first5 = list(itertools.islice(gen, 5))
            output.setText("\n".join(f"{v:.2f}" for v in first5))

        btn.clicked.connect(show)
        layout.addWidget(btn)
        layout.addWidget(output)
        w.setLayout(layout)
        return w

    def email_tab(self):
        w = QWidget()
        layout = QVBoxLayout()

        btn = QPushButton("Показать 7 email")
        output = QTextEdit()

        def show():
            gen = email_generator()
            emails = list(itertools.islice(gen, 7))
            output.setText("\n".join(emails))

        btn.clicked.connect(show)
        layout.addWidget(btn)
        layout.addWidget(output)
        w.setLayout(layout)
        return w

    def filter_tab(self):
        w = QWidget()
        layout = QVBoxLayout()

        input_field = QLineEdit()
        btn = QPushButton("Фильтровать")
        output = QLabel()

        def run():
            try:
                res = filter_two_digits(input_field.text())
                output.setText(" ".join(map(str, res)))
            except Exception as e:
                output.setText(str(e))

        btn.clicked.connect(run)
        layout.addWidget(input_field)
        layout.addWidget(btn)
        layout.addWidget(output)
        w.setLayout(layout)
        return w
