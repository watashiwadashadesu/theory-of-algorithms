#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть список песен группы Depeche Mode со временем звучания с точностью до долей минут
violator_songs_list = [
    ['World in My Eyes', 4.86],
    ['Sweetest Perfection', 4.43],
    ['Personal Jesus', 4.56],
    ['Halo', 4.9],
    ['Waiting for the Night', 6.07],
    ['Enjoy the Silence', 4.20],
    ['Policy of Truth', 4.76],
    ['Blue Dress', 4.29],
    ['Clean', 5.83],
]

# Есть словарь песен группы Depeche Mode
violator_songs_dict = {
    'World in My Eyes': 4.76,
    'Sweetest Perfection': 4.43,
    'Personal Jesus': 4.56,
    'Halo': 4.30,
    'Waiting for the Night': 6.07,
    'Enjoy the Silence': 4.6,
    'Policy of Truth': 4.88,
    'Blue Dress': 4.18,
    'Clean': 5.68,
}

def count_1():
    """Время звучания трех песен из списка"""
    halo_time = violator_songs_list[3][1]  # 'Halo'
    enjoy_time = violator_songs_list[5][1]  # 'Enjoy the Silence'
    clean_time = violator_songs_list[8][1]  # 'Clean'
    total_time_list = round(halo_time + enjoy_time + clean_time, 2)
    return total_time_list

def count_2():
    """Время звучания трех других песен из словаря"""
    sweetest_time = violator_songs_dict['Sweetest Perfection']
    policy_time = violator_songs_dict['Policy of Truth']
    blue_time = violator_songs_dict['Blue Dress']
    total_time_dict = round(sweetest_time + policy_time + blue_time, 2)
    return total_time_dict
