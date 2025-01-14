import sympy as sp
from dichotomy import dichotomy_method, dichotomy_method_with_history, plot_dichotomy_results
from root_solver import find_all_roots
import sys


sys.setrecursionlimit(10000)


def parse_function(input_function):
    try:
        x = sp.Symbol('x')

        allowed_functions = {
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'ctg': sp.cot,
            'sec': sp.sec,
            'csc': sp.csc,
            'asin': sp.asin,
            'acos': sp.acos,
            'atan': sp.atan,
            'acot': sp.acot,
            'asec': sp.asec,
            'acsc': sp.acsc,
            'sinh': sp.sinh,
            'cosh': sp.cosh,
            'tanh': sp.tanh,
            'coth': sp.coth,
            'sech': sp.sech,
            'csch': sp.csch,
            'asinh': sp.asinh,
            'acosh': sp.acosh,
            'atanh': sp.atanh,
            'acoth': sp.acoth,
            'asech': sp.asech,
            'acsch': sp.acsch,
            'exp': sp.exp,
            'ln': sp.log,
            'log': sp.log,
            'sqrt': sp.sqrt,
            'pow': sp.Pow,
            'e': sp.E,
            'pi': sp.pi,
            'abs': sp.Abs,
            'floor': sp.floor,
            'ceil': sp.ceiling,
            'sign': sp.sign,
            'gamma': sp.gamma,
            'factorial': sp.factorial
        }

        expr = sp.sympify(input_function, locals=allowed_functions)

        func = sp.lambdify(x, expr, 'numpy')
        return func

    except Exception as e:
        print(f"Ошибка при парсинге функции: {e}")
        return None


if __name__ == "__main__":
    while True:
        print("\nМеню:")
        print("1 - Метод дихотомии для поиска минимума")
        print("2 - Метод дихотомии для поиска минимума с визуализацией")
        print("3 - Решение уравнения f(x) = 0")
        print("4 - Выход")

        choice = input("Выберите опцию: ")

        if choice == "4":
            print("Выход из программы.")
            break

        user_function = input("Введите функцию f(x): ")
        f = parse_function(user_function)

        if f is None:
            continue

        a = float(input("Введите начальную точку интервала (a): "))
        b = float(input("Введите конечную точку интервала (b): "))
        epsilon = float(input("Введите точность (epsilon): "))

        if choice == "1":
            x_min = dichotomy_method(a, b, epsilon, f)
            print(f"Минимум функции: x = {x_min:.5f}, f(x) = {f(x_min):.5f}")
        elif choice == "2":
            x_min, f_min, history, intervals = dichotomy_method_with_history(a, b, epsilon, f)
            print(f"Минимум функции: x = {x_min:.5f}, f(x) = {f_min:.5f}")
            plot_dichotomy_results(a, b, f, history, intervals, "Метод дихотомии: приближение к минимуму f(x)")
        elif choice == "3":
            roots = find_all_roots(f, a, b, epsilon)
            if roots:
                print("Найденные корни уравнения f(x) = 0:")
                for i, (root, iterations) in enumerate(roots, start=1):
                    print(f"Корень {i}: x = {root:.5f}, найден за {iterations} итераций")
            else:
                print("Корни на заданном интервале не найдены.")
        else:
            print("Неверный выбор, попробуйте снова.")
