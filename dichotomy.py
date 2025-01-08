from typing import Callable, Tuple, List


def dichotomy_method(a: float, b: float, epsilon: float, f: Callable[[float], float]) -> float:
    """
    Метод дихотомии для поиска минимума функции на заданном отрезке [a, b].

    :param a: Левая граница интервала поиска минимума.
    :param b: Правая граница интервала поиска минимума.
    :param epsilon: Точность поиска минимума.
    :param f: Целевая функция, минимум которой ищется. Должна принимать float и возвращать float.
    :return: Приближённое значение минимума функции x_min.
    """
    delta = epsilon / 2
    while (b - a) > epsilon:
        y = (a + b - delta) / 2
        z = (a + b + delta) / 2

        if f(y) <= f(z):
            b = z
        else:
            a = y

    x_min = (a + b) / 2
    return x_min


def dichotomy_method_with_history(a: float, b: float, epsilon: float, f: Callable[[float], float]) -> Tuple[
        float, float, List[Tuple[float, float, float]], List[float]]:
    """
    Метод дихотомии для поиска минимума функции на заданном отрезке [a, b] с сохранением данных о каждой итерации.

    :param a: Левая граница интервала поиска минимума.
    :param b: Правая граница интервала поиска минимума.
    :param epsilon: Точность поиска минимума.
    :param f: Целевая функция, минимум которой ищется. Должна принимать float и возвращать float.
    :return: Кортеж, содержащий:
        - x_min (float): Приближённое значение минимума функции.
        - f(x_min) (float): Значение функции в точке минимума.
        - iterations (int): Количество итераций, затраченных на поиск минимума.
        - history (List[Tuple[float, float, float]]): История итераций с границами интервалов и их серединой.
        - intervals (List[float]): Длины интервалов на каждой итерации.
    """
    delta = epsilon / 2  # Малое смещение от середины
    iterations = 0
    intervals = []  # Список для хранения длин интервалов на каждой итерации
    history = []  # Список для хранения данных о каждой итерации

    while (b - a) > epsilon:
        iterations += 1

        # Сохраняем текущую длину интервала
        intervals.append(b - a)

        # Вычисление точек y и z
        y = (a + b - delta) / 2
        z = (a + b + delta) / 2

        # Сохраняем историю для отображения
        history.append((a, b, (a + b) / 2))

        # Выбор нового интервала
        if f(y) <= f(z):
            b = z
        else:
            a = y

    # Итоговое приближение минимума
    x_min = (a + b) / 2
    return x_min, f(x_min), history, intervals
