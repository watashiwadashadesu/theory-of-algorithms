import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.generators import circle_area_generator, email_generator
import itertools


def test_circle_first_value():
    gen = circle_area_generator(10, 10)
    val = next(gen)
    assert round(val, 2) == round(3.14159 * 100, 2)


def test_email_format():
    gen = email_generator()
    email = next(gen)
    assert email.endswith("@mail.ru")
    assert len(email.split("@")[0]) == 8
