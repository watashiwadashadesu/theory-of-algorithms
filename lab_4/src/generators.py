import math
import random
from string import ascii_lowercase, ascii_uppercase


def circle_area_generator(start=10, end=100):
    """Генератор площадей кругов."""
    try:
        for r in range(start, end + 1):
            yield math.pi * r * r
    except Exception as e:
        raise RuntimeError("Ошибка в генераторе площадей кругов") from e


to_emails = ascii_lowercase + ascii_uppercase + "0123456789_"


def email_generator(domain="mail.ru"):
    """Бесконечный генератор email-адресов."""
    try:
        while True:
            name = "".join(random.choice(to_emails) for _ in range(8))
            yield f"{name}@{domain}"
    except Exception as e:
        raise RuntimeError("Ошибка в генераторе email-адресов") from e
