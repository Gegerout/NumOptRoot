from numpy import std
from dichotomy import dichotomy_method
from math import log2, tan, pi
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
        if any([f(res) <= 0, f(res - epsilon / 2) <= 0, f(res + epsilon / 2) <= 0]):
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
    x = [modified_solver(f, a, extremum, epsilon, 0), modified_solver(f, extremum, b, epsilon, 0)]
    return [e for e in x if type(e) != str]


# Определение функций
def f(x):
    return x ** 2 - 2.28 * x


def k(x):
    return tan(x)


# Ищем корень для f(x) = x - 2 на интервале [-30000000, 4]
_, c = solver(lambda x: x - 2, -30000000, 4, 0.001, 0)
print(c, "~", num_iterations(-30000000, 4, 0.001))

# Ищем корень для f(x) = x - 2 на интервале [-3, 25]
_, c = solver(lambda x: x - 2, -3, 25, 0.001, 0)
print(c, "~", num_iterations(-3, 25, 0.001))

# Ищем корень для f(x) = x^2 - 2 на интервале [0, 999999999999999999]
_, c = solver(lambda x: x ** 2 - 2, 0, 999999999999999999, 0.001, 0)
print(c, "~", num_iterations(-500, 999999999999999999, 0.001), '\n')


# Рассчитываем среднеквадратичное отклонение для численного решения
print('СКО для функции f(x):', std([2.28, solver(f, 0.00001, 1000, 0.01, 0)[0]]))
print('СКО для функции k(x):', std([pi, solver(k, 2.5252525252, 4.2, 0.0001, 0)[0]]), '\n')


# Обработка случая, когда решения функции на заданном отрезке нет
try:
    root, c = modified_solver(lambda x: x**2 + 2, -3, 5, 0.001, 0)
    print(root)
except MathError as e:
    print(e)


# Смотрим на множественный вывод корней
roots = [e[0] for e in find_all_roots(lambda x: x**2 - 2, -5, 5, 0.0001)]
print('\nКорни:', ', '.join(map(str, roots)))
