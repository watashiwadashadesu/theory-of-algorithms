from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

def save_to_excel(postal_items, filename="postal_report.xlsx"):
    """
    Сохраняет список почтовых отправлений в файл Excel.

    Args:
        postal_items (list): Список объектов PostalItem.
        filename (str): Имя файла для сохранения.
    """

    print(f"Сохраняем {len(postal_items)} отправлений в {filename}")

    # Создаем папку если ее нет
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "Отчет по почтовым отправлениям"

    # Создаем заголовки
    headers = ["Тип отправления", "Расстояние (км)", "Вес (кг)", "Объем (см³)", "Тип доставки", "Доп. информация", "Стоимость"]
    ws.append(headers)
    print("Заголовки созданы")

    # Форматируем заголовки
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')

    # Заполняем данными
    print("Начинаем заполнение данных...")
    for i, item in enumerate(postal_items):
        print(f"Обрабатываем отправление {i + 1}: {item.name}")

        try:
            # Базовые данные для всех типов
            row = [
                item.name,
                item.distance_km,
                item.weight_kg,
                getattr(item, 'volume_cubic_cm', 'N/A'),
                item.delivery_type
            ]
            print(f"Базовые данные: {row}")

            # Дополнительная информация
            extra_info = ""
            if item.name == "Письмо":
                extra_info = "Заказное" if item.is_registered else "Обычное"
            elif item.name == "Посылка":
                extra_info = "Хрупкая" if item.is_fragile else "Обычная"
            elif item.name == "Бандероль":
                volume = getattr(item, 'volume_cubic_cm', 0)
                extra_info = "Объемная" if volume > 5000 else "Стандартная"

            row.append(extra_info)
            row.append(item.price)  # Используем property
            print(f"Полная строка: {row}")

            ws.append(row)
            print(f"Строка {i + 1} добавлена в Excel")

        except Exception as e:
            print(f"Ошибка при обработке элемента {item}: {e}")
            continue

    # Автоматически подгоняем ширину колонок
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 2

    # Сохраняем файл
    wb.save(filename)
    print(f"\nОтчёт успешно сохранён в файл: {filename}")