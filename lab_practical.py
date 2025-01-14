import numpy as np
from dichotomy import dichotomy_method_with_history, plot_dichotomy_results
from math import tan, pi
from root_solver import solver, num_iterations, modified_solver, MathError, find_all_roots


"""
Задание 1
"""
# Определение функции
def f(x):
    return x * np.cos(x / 2.28) + np.sin(52)


# Первый интервал
a, b, epsilon = -4, 0, 1e-5
x_min, f_min, history, intervals = dichotomy_method_with_history(a, b, epsilon, f)
print(f"Минимум функции: x = {x_min:.5f}, f(x) = {f_min:.5f}")
plot_dichotomy_results(a, b, f, history, intervals, "Метод дихотомии: приближение к минимуму f(x)")

# Второй интервал (с неоднозначностью)
c, d = 0.0, 200.0
x_min, f_min, history, intervals = dichotomy_method_with_history(c, d, epsilon, f)
print(f"Минимум функции: x = {x_min:.5f}, f(x) = {f_min:.5f}")
plot_dichotomy_results(c, d, f, history, intervals, "Метод дихотомии на неунимодальном интервале", plot_intervals=False)


"""
Задание 2
"""
# Определение функций
def g(x):
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
print('СКО для функции f(x):', np.std([2.28, solver(g, 0.00001, 1000, 0.01, 0)[0]]))
print('СКО для функции k(x):', np.std([pi, solver(k, 2.5252525252, 4.2, 0.0001, 0)[0]]), '\n')


# Обработка случая, когда решения функции на заданном отрезке нет
try:
    root, c = modified_solver(lambda x: x**2 + 2, -3, 5, 0.001, 0)
    print(root)
except MathError as e:
    print(e)


# Смотрим на множественный вывод корней
roots = [e[0] for e in find_all_roots(lambda x: x**2 - 2.28*x, 0.0001, 10000, 0.0001) if type(e[0]) != str]
print('\nКорни:', ', '.join(map(str, roots)))
