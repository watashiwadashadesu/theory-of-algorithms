import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.filters import filter_two_digits


def test_filter():
    assert filter_two_digits("1 22 333 44") == [22, 44]


def test_filter_error():
    try:
        filter_two_digits("abc 12")
        assert False
    except ValueError:
        assert True
