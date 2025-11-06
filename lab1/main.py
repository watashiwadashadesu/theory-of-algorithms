from tasks.circle import calc_area, is_in, is_out, point_1, point_2
from tasks.distance import calc_distances
from tasks.favorite_movies import sort_movies
from tasks.garden import flowers, garden, meadow
from tasks.my_family import get_height
from tasks.operations import res
from tasks.secret import decrypt
from tasks.shopping import get_sweets
from tasks.songs_list import count_1, count_2
from tasks.store import view_store
from tasks.zoo import shake_zoo

print("=" * 50)
print("Задание 1: circle")
print("=" * 50)
print(f"Площадь: {calc_area()}, точка 1: {is_in(point_1)}, точка 2: {is_out(point_2)}")
print("\n" + "=" * 50)

print("Задание 2: distance")
print("=" * 50)
print(calc_distances())
print("\n" + "=" * 50)

print("Задание 3: favorite_movies")
print("=" * 50)
print(sort_movies())

print("Задание 4: garden")
print("=" * 50)
print(flowers(garden, meadow))
print("\n" + "=" * 50)


print("Задание 5: my_family")
print("=" * 50)
print(get_height())
print("\n" + "=" * 50)

print("Задание 6: operations")
print("=" * 50)
print(res())
print("\n" + "=" * 50)

print("Задание 7: secret")
print("=" * 50)
print(decrypt())
print("\n" + "=" * 50)

print("Задание 8: shopping")
print("=" * 50)
print(get_sweets())
print("\n" + "=" * 50)

print("Задание 9: songs_list")
print("=" * 50)
print(f'Три песни звучат {count_1()} минут')
print(f'А другие три песни звучат {count_2()} минут')
print("\n" + "=" * 50)

print("Задание 10: store")
print("=" * 50)
print(view_store())
print("=" * 50)

print("Задание 11: zoo")
print("=" * 50)
print(shake_zoo())
print("\n" + "=" * 50)



