import concurrent.futures
from generators import circle_area_generator


def threaded_circle_areas(start=10, end=100, workers=8):
    """Многопоточное вычисление площадей кругов."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        radii = range(start, end + 1)
        results = list(ex.map(lambda r: 3.14159 * r * r, radii))
    return results
