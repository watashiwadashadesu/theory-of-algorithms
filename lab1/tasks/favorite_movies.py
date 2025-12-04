#!/usr/bin/env python3
# -*- coding: utf-8 -*-

my_favorite_movies = 'Терминатор, Пятый элемент, Аватар, Чужие, Назад в будущее'


def sort_movies():
    """Извлечение фильмов из строки"""
    # Первый фильм
    comma_pos = 0
    while my_favorite_movies[comma_pos] != ',':
        comma_pos += 1
    first_movie = my_favorite_movies[:comma_pos]

    # Последний фильм
    comma_pos = len(my_favorite_movies) - 1
    while my_favorite_movies[comma_pos] != ',':
        comma_pos -= 1
    last_movie = my_favorite_movies[comma_pos + 2:]

    # Второй фильм
    first_comma_pos = 0
    while my_favorite_movies[first_comma_pos] != ',':
        first_comma_pos += 1

    second_comma_pos = first_comma_pos + 1
    while my_favorite_movies[second_comma_pos] != ',':
        second_comma_pos += 1

    second_movie = my_favorite_movies[first_comma_pos + 2:second_comma_pos]

    # Второй с конца
    last_comma_pos = len(my_favorite_movies) - 1
    while my_favorite_movies[last_comma_pos] != ',':
        last_comma_pos -= 1

    prev_comma_pos = last_comma_pos - 1
    while my_favorite_movies[prev_comma_pos] != ',':
        prev_comma_pos -= 1

    second_last_movie = my_favorite_movies[prev_comma_pos + 2:last_comma_pos]

    return (f"Первый: {first_movie}, второй: {second_movie}, предпоследний: "
            f"{second_last_movie}, последний: {last_movie}")
