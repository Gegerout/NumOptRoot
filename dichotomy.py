from typing import Callable, Tuple, List
import matplotlib.pyplot as plt
import numpy as np


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


def plot_dichotomy_results(a: float, b: float, f, history, intervals, title: str, plot_intervals: bool = True):
    """
    Функция для построения графиков метода дихотомии.

    :param a: Левая граница интервала.
    :param b: Правая граница интервала.
    :param f: Целевая функция.
    :param history: История итераций.
    :param intervals: Длины интервалов неопределенности.
    :param title: Заголовок графика.
    :param plot_intervals: Флаг для отображения графика изменения длины интервала.
    """
    # График с положением точек экстремума на каждой итерации
    x_vals = np.linspace(a, b, 400)
    y_vals = [f(x) for x in x_vals]

    plt.figure(figsize=(12, 6))
    plt.plot(x_vals, y_vals, label="f(x)")

    # Добавление точек итераций
    for i, (x1, x2, mid) in enumerate(history):
        plt.scatter([x1, x2, mid], [f(x1), f(x2), f(mid)], label=f"Iter {i + 1}", alpha=0.7)

    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    plt.show()

    # График изменения длины промежутка неопределенности с возрастанием числа итераций
    if plot_intervals:
        plt.figure(figsize=(12, 6))
        plt.plot(range(1, len(intervals) + 1), intervals, marker="o", label="Длина интервала неопределенности")
        plt.title("Изменение длины интервала неопределенности с итерациями")
        plt.xlabel("Итерация")
        plt.ylabel("Длина интервала")
        plt.legend()
        plt.grid(True)
        plt.show()
