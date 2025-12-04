#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from tasks.circle import calc_area, is_in, is_out, radius, point_1, point_2
from tasks.distance import calc_distances
from tasks.favorite_movies import sort_movies
from tasks.garden import flowers, garden, meadow
from tasks.my_family import get_height
from tasks.operations import res
from tasks.zoo import shake_zoo
from tasks.songs_list import count_1, count_2
from tasks.secret import decrypt
from tasks.shopping import get_sweets
from tasks.store import view_store


class TestCircle:
    def test_calc_area(self):
        area = calc_area()
        assert area == 5541.7693

    def test_is_in(self):
        assert is_in(point_1) == True

    def test_is_out(self):
        assert is_out(point_2) == True

    def test_radius_value(self):
        assert radius == 42


class TestDistance:
    def test_calc_distances(self):
        distances = calc_distances()
        assert ('Moscow', 'Paris') in distances
        assert ('London', 'Moscow') in distances
        assert ('London', 'Paris') in distances
        assert isinstance(distances, dict)


class TestFavoriteMovies:
    def test_sort_movies(self):
        result = sort_movies()
        assert "Терминатор" in result
        assert "Пятый элемент" in result
        assert "Назад в будущее" in result


class TestGarden:
    def test_flowers_function(self):
        result = flowers(garden, meadow)
        assert "ромашка" in result
        assert "роза" in result
        assert "одуванчик" in result


class TestMyFamily:
    def test_get_height(self):
        result = get_height()
        assert "Рост отца" in result
        assert "Общий рост" in result


class TestOperations:
    def test_res_returns_string(self):
        result = res()
        assert result == ""  # Проверяем что возвращается пустая строка


class TestZoo:
    def test_shake_zoo(self):
        result = shake_zoo()
        assert "Лев сидит в клетке" in result
        assert "жаворонок в клетке" in result


class TestSongsList:
    def test_count_1_type(self):
        result = count_1()
        assert isinstance(result, (int, float))

    def test_count_2_type(self):
        result = count_2()
        assert isinstance(result, (int, float))


class TestSecret:
    def test_decrypt(self):
        result = decrypt()
        assert "в бане веник дороже денег" == result


class TestShopping:
    def test_get_sweets(self):
        result = get_sweets()
        assert "печенье" in result
        assert "конфеты" in result
        assert "руб" in result


class TestStore:
    def test_view_store(self):
        result = view_store()
        assert "Лампа" in result
        assert "Стол" in result
        assert "Диван" in result
        assert "Стул" in result
        assert "шт" in result


def test_all_modules_integration():
    calc_area()
    calc_distances()
    sort_movies()
    flowers(garden, meadow)
    get_height()
    res()
    shake_zoo()
    count_1()
    count_2()
    decrypt()
    get_sweets()
    view_store()

    assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])