def filter_two_digits(numbers):
    try:
        nums = list(map(int, numbers.split()))
        return list(filter(lambda x: 10 <= abs(x) <= 99, nums))
    except ValueError:
        raise ValueError("Введены нечисловые данные")
    except Exception as e:
        raise RuntimeError("Ошибка фильтрации") from e
