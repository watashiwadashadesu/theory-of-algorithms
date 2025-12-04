import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                               QPushButton, QComboBox, QMessageBox, QMenuBar,
                               QMenu, QStatusBar, QFormLayout, QGroupBox,
                               QHeaderView, QDoubleSpinBox, QSpinBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QAction, QFont

# Импортируем из shared
from shared.database import BookClubManager, Book
from shared.exceptions import BookError


class MainWindow(QMainWindow):
    """Главное окно приложения."""

    def __init__(self, manager=None):  # ✅ Изменено: принимает manager
        super().__init__()
        self.manager = manager if manager else BookClubManager()  # ✅ Используем переданный или создаем новый
        self.init_ui()
        self.load_books_to_table()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        self.setWindowTitle("Менеджер книжного клуба")
        self.setGeometry(100, 100, 1200, 700)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # ЛЕВАЯ ПАНЕЛЬ: Форма ввода и кнопки
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Группа "Добавить/Изменить книгу"
        form_group = QGroupBox("Добавить / Изменить книгу")
        form_layout = QFormLayout()

        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.year_input = QSpinBox()
        self.year_input.setRange(1900, 2100)
        self.year_input.setValue(2023)
        self.genre_input = QComboBox()
        self.genre_input.addItems(["Роман", "Фэнтези", "Научная фантастика", "Детектив",
                                   "Нон-фикшн", "Биография", "Поэзия", "Другое"])
        self.status_input = QComboBox()
        self.status_input.addItems(["В наличии", "Читается", "Прочитана"])
        self.reader_input = QLineEdit()
        self.reader_input.setPlaceholderText("Имя читателя (если книга на руках)")
        self.rating_input = QDoubleSpinBox()
        self.rating_input.setRange(0.0, 10.0)
        self.rating_input.setSingleStep(0.5)
        self.rating_input.setSpecialValueText("Не оценена")

        form_layout.addRow("Название*:", self.title_input)
        form_layout.addRow("Автор*:", self.author_input)
        form_layout.addRow("Год издания*:", self.year_input)
        form_layout.addRow("Жанр:", self.genre_input)
        form_layout.addRow("Статус:", self.status_input)
        form_layout.addRow("Читатель:", self.reader_input)
        form_layout.addRow("Рейтинг (0-10):", self.rating_input)

        form_group.setLayout(form_layout)
        left_layout.addWidget(form_group)

        # Кнопки действий
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить книгу")
        self.add_button.clicked.connect(self.add_book)
        self.update_button = QPushButton("Обновить книгу")
        self.update_button.clicked.connect(self.update_book)
        self.update_button.setEnabled(False)
        self.delete_button = QPushButton("Удалить книгу")
        self.delete_button.clicked.connect(self.delete_book)
        self.delete_button.setEnabled(False)
        self.clear_button = QPushButton("Очистить форму")
        self.clear_button.clicked.connect(self.clear_form)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)
        left_layout.addLayout(button_layout)

        # Статистика
        stats_group = QGroupBox("Статистика клуба")
        stats_layout = QVBoxLayout()
        self.stats_label = QLabel("Всего книг: 0 | Средний рейтинг: 0.00")
        stats_layout.addWidget(self.stats_label)
        stats_group.setLayout(stats_layout)
        left_layout.addWidget(stats_group)

        left_layout.addStretch()
        main_layout.addWidget(left_panel, stretch=1)

        # ПРАВАЯ ПАНЕЛЬ: Таблица и график
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Таблица книг
        table_group = QGroupBox("Каталог книг клуба")
        table_layout = QVBoxLayout()
        self.books_table = QTableWidget()
        self.books_table.setColumnCount(8)
        self.books_table.setHorizontalHeaderLabels(
            ["ID", "Название", "Автор", "Год", "Жанр", "Статус", "Читатель", "Рейтинг"]
        )
        self.books_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.books_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.books_table.itemSelectionChanged.connect(self.on_book_selected)

        table_layout.addWidget(self.books_table)
        table_group.setLayout(table_layout)
        right_layout.addWidget(table_group, stretch=2)

        # График (круговой для статусов)
        chart_group = QGroupBox("Распределение книг по статусам")
        chart_layout = QVBoxLayout()
        self.chart_view = QChartView()
        self.chart_view.setMinimumHeight(250)
        chart_layout.addWidget(self.chart_view)
        chart_group.setLayout(chart_layout)
        right_layout.addWidget(chart_group, stretch=1)

        main_layout.addWidget(right_panel, stretch=2)

        # Создание меню
        self.create_menu()

        # Статус бар
        self.statusBar().showMessage("Готово")

        # Обновляем статистику и график
        self.update_statistics()

        search_group = QGroupBox("Поиск книг")
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию или автору...")
        self.search_button = QPushButton("🔍 Поиск")
        self.search_button.clicked.connect(self.search_books)
        self.clear_search_button = QPushButton("Очистить")
        self.clear_search_button.clicked.connect(self.clear_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.clear_search_button)
        search_group.setLayout(search_layout)

        # Добавить эту группу в left_layout ПЕРЕД stats_group
        # Найти строку: left_layout.addWidget(stats_group)
        # И добавить перед ней:
        left_layout.addWidget(search_group)

    def search_books(self):
        """Выполняет поиск книг."""
        search_text = self.search_input.text().strip()
        if not search_text:
            self.load_books_to_table()
            return

        try:
            books = self.manager.search_books(title=search_text, author=search_text)
            self.display_books(books)
            self.statusBar().showMessage(f"Найдено {len(books)} книг по запросу '{search_text}'", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка поиска", f"Произошла ошибка: {e}")

    def clear_search(self):
        """Очищает поиск и показывает все книги."""
        self.search_input.clear()
        self.load_books_to_table()
        self.statusBar().showMessage("Поиск очищен", 2000)

    def display_books(self, books: list):
        """Отображает список книг в таблице."""
        self.books_table.setRowCount(len(books))

        for row, book in enumerate(books):
            self.books_table.setItem(row, 0, QTableWidgetItem(str(book.id)))
            self.books_table.setItem(row, 1, QTableWidgetItem(book.title))
            self.books_table.setItem(row, 2, QTableWidgetItem(book.author))
            self.books_table.setItem(row, 3, QTableWidgetItem(str(book.year)))
            self.books_table.setItem(row, 4, QTableWidgetItem(book.genre))
            self.books_table.setItem(row, 5, QTableWidgetItem(book.status))

            reader = book.reader if book.reader else "-"
            self.books_table.setItem(row, 6, QTableWidgetItem(reader))

            rating = str(book.rating) if book.rating is not None else "-"
            self.books_table.setItem(row, 7, QTableWidgetItem(rating))

    def create_menu(self):
        """Создает меню приложения."""
        menubar = self.menuBar()

        # Меню Файл
        file_menu = menubar.addMenu("Файл")

        export_action = QAction("Экспорт данных...", self)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню Справка
        help_menu = menubar.addMenu("Справка")
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def load_books_to_table(self):
        """Загружает книги из менеджера в таблицу."""
        books = self.manager.get_all_books()
        self.books_table.setRowCount(len(books))

        for row, book in enumerate(books):
            self.books_table.setItem(row, 0, QTableWidgetItem(str(book.id)))
            self.books_table.setItem(row, 1, QTableWidgetItem(book.title))
            self.books_table.setItem(row, 2, QTableWidgetItem(book.author))
            self.books_table.setItem(row, 3, QTableWidgetItem(str(book.year)))
            self.books_table.setItem(row, 4, QTableWidgetItem(book.genre))
            self.books_table.setItem(row, 5, QTableWidgetItem(book.status))

            reader = book.reader if book.reader else "-"
            self.books_table.setItem(row, 6, QTableWidgetItem(reader))

            rating = str(book.rating) if book.rating is not None else "-"
            self.books_table.setItem(row, 7, QTableWidgetItem(rating))

        self.update_statistics()

    def update_statistics(self):
        """Обновляет статистику и график."""
        stats = self.manager.get_statistics()

        if stats:
            self.stats_label.setText(
                f"Всего книг: {stats['total_books']} | "
                f"Средний рейтинг: {stats['average_rating']}"
            )

            # Обновление круговой диаграммы
            chart = QChart()
            chart.setTitle("Статусы книг в клубе")
            chart.setAnimationOptions(QChart.SeriesAnimations)

            series = QPieSeries()
            for status, count in stats['status_counts'].items():
                series.append(f"{status} ({count})", count)

            chart.addSeries(series)
            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)

            self.chart_view.setChart(chart)
        else:
            self.stats_label.setText("Всего книг: 0 | Средний рейтинг: 0.00")

    def clear_form(self):
        """Очищает поля ввода."""
        self.title_input.clear()
        self.author_input.clear()
        self.year_input.setValue(2023)
        self.genre_input.setCurrentIndex(0)
        self.status_input.setCurrentIndex(0)
        self.reader_input.clear()
        self.rating_input.setValue(0.0)

        # Возвращаем кнопки в исходное состояние
        self.add_button.setEnabled(True)
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        # Снимаем выделение с таблицы
        self.books_table.clearSelection()
        self.statusBar().showMessage("Форма очищена")

    def get_book_from_form(self) -> Book:
        """Создает объект Book из данных формы."""
        rating = self.rating_input.value()
        return Book(
            title=self.title_input.text().strip(),
            author=self.author_input.text().strip(),
            year=self.year_input.value(),
            genre=self.genre_input.currentText(),
            status=self.status_input.currentText(),
            reader=self.reader_input.text().strip() or None,
            rating=rating if rating > 0 else None
        )

    def add_book(self):
        """Добавляет новую книгу."""
        try:
            book = self.get_book_from_form()
            self.manager.add_book(book)
            self.load_books_to_table()
            self.clear_form()
            self.statusBar().showMessage(f"Книга '{book.title}' успешно добавлена!", 3000)
        except BookError as e:
            QMessageBox.warning(self, "Ошибка добавления", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Неизвестная ошибка", f"Произошла ошибка: {e}")

    def on_book_selected(self):
        """Обрабатывает выбор книги в таблице."""
        selected_rows = self.books_table.selectedItems()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        book_id = int(self.books_table.item(row, 0).text())

        # Находим книгу в менеджере
        books = self.manager.get_all_books()
        book = next((b for b in books if b.id == book_id), None)

        if book:
            # Заполняем форму данными выбранной книги
            self.title_input.setText(book.title)
            self.author_input.setText(book.author)
            self.year_input.setValue(book.year)
            self.genre_input.setCurrentText(book.genre)
            self.status_input.setCurrentText(book.status)
            self.reader_input.setText(book.reader or "")
            self.rating_input.setValue(book.rating if book.rating is not None else 0.0)

            # Меняем режим кнопок
            self.add_button.setEnabled(False)
            self.update_button.setEnabled(True)
            self.delete_button.setEnabled(True)

            self.statusBar().showMessage(f"Выбрана книга: {book.title}")

    def update_book(self):
        """Обновляет выбранную книгу."""
        selected_rows = self.books_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите книгу для обновления.")
            return

        row = selected_rows[0].row()
        book_id = int(self.books_table.item(row, 0).text())

        try:
            updated_book = self.get_book_from_form()
            self.manager.update_book(book_id, updated_book.__dict__)
            self.load_books_to_table()
            self.clear_form()
            self.statusBar().showMessage(f"Книга успешно обновлена!", 3000)
        except BookError as e:
            QMessageBox.warning(self, "Ошибка обновления", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Неизвестная ошибка", f"Произошла ошибка: {e}")

    def delete_book(self):
        """Удаляет выбранную книгу."""
        selected_rows = self.books_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите книгу для удаления.")
            return

        row = selected_rows[0].row()
        book_id = int(self.books_table.item(row, 0).text())
        book_title = self.books_table.item(row, 1).text()

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить книгу '{book_title}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.manager.delete_book(book_id)
                self.load_books_to_table()
                self.clear_form()
                self.statusBar().showMessage(f"Книга '{book_title}' удалена.", 3000)
            except BookError as e:
                QMessageBox.warning(self, "Ошибка удаления", str(e))
            except Exception as e:
                QMessageBox.critical(self, "Неизвестная ошибка", f"Произошла ошибка: {e}")

    def show_about(self):
        """Показывает окно 'О программе'."""
        QMessageBox.about(
            self,
            "О программе",
            "<h2>Менеджер книжного клуба v1.0</h2>"
            "<p>Программа для учета книг в книжном клубе.</p>"
            "<p>Лабораторная работа №3 по Python.</p>"
            "<p>Вариант 6: Система учета книг в книжном клубе.</p>"
        )