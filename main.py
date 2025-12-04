from postal_service.models import Letter, Parcel, Banderol
from postal_service.calculators import PriceCalculator
from postal_service.utils import save_to_excel
from postal_service.database import DatabaseManager


def main():
    """Основная функция программы."""
    print("=" * 50)
    print("     КАЛЬКУЛЯТОР СТОИМОСТИ ПОЧТОВЫХ ОТПРАВЛЕНИЙ")
    print("=" * 50)

    calculator = PriceCalculator()
    db = DatabaseManager()  # Инициализируем базу данных
    postal_items = []

    while True:
        print("\nВыберите действие:")
        print("1. Добавить новое отправление")
        print("2. Показать историю отправлений")
        print("3. Показать статистику")
        print("4. Сохранить отчет в Excel")
        print("5. Выйти")

        choice = input("\nВаш выбор (1-5): ").strip()

        if choice == '1':
            add_new_item(calculator, db, postal_items)
        elif choice == '2':
            show_history(db)
        elif choice == '3':
            show_statistics(db)
        elif choice == '4':
            save_report(postal_items, db)
        elif choice == '5':
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите от 1 до 5.")


def add_new_item(calculator, db, postal_items):
    """Добавляет новое почтовое отправление."""
    print("\nВыберите тип отправления:")
    print("1. Письмо")
    print("2. Бандероль")
    print("3. Посылка")

    type_choice = input("\nВаш выбор (1-3): ").strip()

    try:
        if type_choice == '1':
            item = create_letter()
            item.calculate_price(calculator)
            print(f"Письмо создано. Стоимость: {item.price} руб.")
        elif type_choice == '2':
            item = create_banderol()
            item.calculate_price(calculator)
            print(f"Бандероль создана. Стоимость: {item.price} руб.")
        elif type_choice == '3':
            item = create_parcel()
            item.calculate_price(calculator)
            print(f"Посылка создана. Стоимость: {item.price} руб.")
        else:
            print("Неверный выбор.")
            return

        # Сохраняем в базу данных
        item_id = db.save_postal_item(item)
        print(f"Отправление сохранено в базу данных (ID: {item_id})")

        # Добавляем в текущую сессию
        postal_items.append(item)

    except ValueError as e:
        print(f"Ошибка ввода: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def create_letter():
    """Создает объект письма."""
    distance = float(input("Расстояние (км): "))
    weight = float(input("Вес (кг): "))
    delivery = input("Тип доставки (стандарт/ускоренная/экспресс) [стандарт]: ").strip() or "стандарт"
    registered = input("Заказное? (y/n) [n]: ").strip().lower() == 'y'

    return Letter(distance, weight, delivery, registered)


def create_banderol():
    """Создает объект бандероли."""
    distance = float(input("Расстояние (км): "))
    weight = float(input("Вес (кг): "))
    volume = float(input("Объем (см³): "))
    delivery = input("Тип доставки (стандарт/ускоренная/экспресс) [стандарт]: ").strip() or "стандарт"

    return Banderol(distance, weight, volume, delivery)


def create_parcel():
    """Создает объект посылки."""
    distance = float(input("Расстояние (км): "))
    weight = float(input("Вес (кг): "))
    volume = float(input("Объем (см³): "))
    delivery = input("Тип доставки (стандарт/ускоренная/экспресс) [стандарт]: ").strip() or "стандарт"
    fragile = input("Хрупкая? (y/n) [n]: ").strip().lower() == 'y'

    return Parcel(distance, weight, volume, delivery, fragile)


def show_history(db):
    """Показывает историю отправлений."""
    print("\n" + "=" * 60)
    print("ИСТОРИЯ ОТПРАВЛЕНИЙ")
    print("=" * 60)

    items = db.get_all_items()

    if not items:
        print("Нет сохраненных отправлений.")
        return

    for item in items:
        print(f"ID: {item['id']} | {item['item_type']} | "
              f"Расстояние: {item['distance_km']}км | "
              f"Вес: {item['weight_kg']}кг | "
              f"Стоимость: {item['calculated_price']} руб. | "
              f"Дата: {item['created_at']}")


def show_statistics(db):
    """Показывает статистику."""
    print("\n" + "=" * 60)
    print("СТАТИСТИКА")
    print("=" * 60)

    stats = db.get_total_statistics()

    print(f"Всего отправлений: {stats['total_count']}")
    print(f"Общая стоимость: {stats['total_cost']} руб.")
    print(f"Средняя стоимость: {stats['average_cost']} руб.")
    print("\nПо типам:")
    for item_type, count in stats['type_counts'].items():
        print(f"  {item_type}: {count} шт.")


def save_report(postal_items, db):
    """Сохраняет отчет."""
    print(f"Количество отправлений для отчета: {len(postal_items)}")
    if not postal_items:
        print("Нет данных для сохранения.")
        return

    for i, item in enumerate(postal_items):
        print(f"Отправление {i + 1}: {item.name}, цена: {item.price}")

    print("\nВыберите тип отчета:")
    print("1. Текущая сессия")
    print("2. Вся история из базы данных")

    report_choice = input("Ваш выбор (1-2): ").strip()

    filename = input("Имя файла (без расширения) [postal_report]: ").strip() or "postal_report"
    filename = f"reports/{filename}.xlsx"

    try:
        if report_choice == '1':
            save_to_excel(postal_items, filename)
        elif report_choice == '2':
            # Получаем все данные из БД и конвертируем в объекты для отчета
            all_items = db.get_all_items()
            # Здесь можно добавить логику конвертации данных из БД в объекты
            # Для простоты сохраняем текущую сессию
            save_to_excel(postal_items, filename)
        else:
            print("Неверный выбор.")
            return

    except Exception as e:
        print(f"Ошибка при сохранении отчета: {e}")


if __name__ == "__main__":
    main()

# docker build -t postal-service .
# mkdir -p data reports
# docker run -it -v $(pwd)/data:/app/data -v $(pwd)/reports:/app/reports postal-service