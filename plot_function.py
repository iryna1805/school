import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify, lambdify
import os

def plot_and_save_function(expression):
    x = symbols('x')
    expr = sympify(expression)
    f = lambdify(x, expr, 'numpy')

    x_values = np.linspace(-10, 10, 400)
    y_values = []

    for x_val in x_values:
        if '1/(' in expression and f(x_val) == np.inf:
            y_values.append(np.nan)
        else:
            y_values.append(f(x_val))

    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, label=f"f(x) = {expression}")
    plt.title(f'Courbe de {expression}')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    plt.grid(True)
    plt.legend()

    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    plt.savefig('graphs/fonction_graph.png')
    plt.show()
    print("Graph saved to graphs/fonction_graph.png")
