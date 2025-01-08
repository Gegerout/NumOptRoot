import numpy as np
import matplotlib.pyplot as plt
from dichotomy import dichotomy_method_with_history


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
