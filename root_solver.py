from dichotomy import dichotomy_method
from math import log2
from typing import Callable, Tuple, List


class MathError(Exception):
    pass


def solver(f: Callable[[float], float], a: float, b: float, epsilon: float, c: int) -> Tuple[float, int]:
    """
    Рекурсивный алгоритм для нахождения решения функции на отрезке [a, b].

    :param f: Функция, для которой ищется корень.
    :param a: Начало отрезка.
    :param b: Конец отрезка.
    :param epsilon: Погрешность, при которой алгоритм завершится.
    :param c: Счетчик количества итераций.
    :return: Кортеж с найденным корнем и количеством итераций.
    """

    # Проверка знаков функции на концах отрезка
    if f(a) * f(b) > 0:
        res = dichotomy_method(a, b, epsilon, f)

        return solver(f, a, res, epsilon, c)  # Рекурсивно ищем корень на уменьшенном отрезке

    # Критерий остановки: если разница между концами отрезка меньше погрешности
    if abs(b - a) < epsilon:
        return (a + b) / 2, c

    c += 1

    # Вычисляем середины отрезка с учетом погрешности
    a1, b1 = (a + b - epsilon / 2) / 2, (a + b + epsilon / 2) / 2

    # Определяем, какой из отрезков выбрать для дальнейшего поиска корня
    tup = (a1, b) if f(a1) * f(a) > 0 else (a, b1)

    return solver(f, *tup, epsilon, c)


def modified_solver(f: Callable[[float], float], a: float, b: float, epsilon: float, c: int) -> Tuple[float, int]:
    """
    Модифицированная версия алгоритма для нахождения решения с проверкой на отсутствие корня.

    :param f: Функция, для которой ищется корень.
    :param a: Начало отрезка.
    :param b: Конец отрезка.
    :param epsilon: Погрешность, при которой алгоритм завершится.
    :param c: Счетчик количества итераций.
    :return: Кортеж с найденным корнем и количеством итераций.
    """

    # Проверка знаков функции на концах отрезка
    if f(a) * f(b) > 0:
        res = dichotomy_method(a, b, epsilon, f)

        # Проверяем, есть ли корень на отрезке, иначе выбрасываем исключение
        if any([f(res) * f(a) <= 0, f(res - epsilon / 2) * f(a) <= 0, f(res + epsilon / 2) * f(a) <= 0]):
            return solver(f, a, res, epsilon, c)
        else:
            raise MathError("Корня нет, либо установить его наличие этим методом невозможно")

    # Критерий остановки: если разница между концами отрезка меньше погрешности
    if abs(b - a) < epsilon:
        return (a + b) / 2, c

    c += 1

    # Вычисляем середины отрезка с учетом погрешности
    a1, b1 = (a + b - epsilon / 2) / 2, (a + b + epsilon / 2) / 2

    # Определяем, какой из отрезков выбрать для дальнейшего поиска корня
    tup = (a1, b) if f(a1) * f(a) > 0 else (a, b1)

    return solver(f, *tup, epsilon, c)


def num_iterations(a: float, b: float, epsilon: float) -> float:
    """
    Рассчитывает теоретическое количество итераций для нахождения корня с заданной погрешностью.

    :param a: Начало отрезка.
    :param b: Конец отрезка.
    :param epsilon: Погрешность, при которой алгоритм завершится.
    :return: Теоретическое количество итераций.
    """
    # Логарифмическая зависимость для количества итераций
    return log2(-(epsilon - 2 * abs(b - a)) / epsilon)


def find_all_roots(f: Callable[[float], float], a: float, b: float, epsilon: float) -> List:
    """
    Ищем все корни функции на заданном отрезке (при условии, что функция строго унимодальна)

    :param f: Функция, для которой ищется корень.
    :param a: Начало отрезка.
    :param b: Конец отрезка.
    :param epsilon: Погрешность, при которой алгоритм завершится.
    :return: Теоретическое количество итераций.
    """
    extremum = dichotomy_method(a, b, epsilon, f)
    intervals = [(a, extremum), (extremum, b)]
    x = []
    for interval in intervals:
        try:
            x += [modified_solver(f, *interval, epsilon, 0)]
        except MathError as e:
            print(e)
    return [e for e in x if type(e) is not str]
