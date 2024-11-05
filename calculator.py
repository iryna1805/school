import tkinter as tk
import math
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, diff, integrate, solve, sympify, lambdify
import os
from plot_function import plot_and_save_function


root = tk.Tk()
root.title("Calculatrice Scientifique: Roshen")
root.geometry("450x650")
root.config(bg="#330000")

entry = tk.Entry(root, width=30, font=('Arial', 24), justify=tk.RIGHT, bd=10, bg="#D8BFD8", state='disabled')
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=20)

button_params = {
    'font': ('Arial', 14),
    'bg': "#73605B",
    'fg': "#D09683",
    'width': 5,
    'height': 2
}

calculator_on = False

def enable_calculator():
    global calculator_on
    calculator_on = True
    entry.config(state='normal')

def disable_calculator():
    global calculator_on
    calculator_on = False
    entry.delete(0, tk.END)
    entry.config(state='disabled')

def button_click(value):
    if calculator_on:
        current = entry.get()
        entry.delete(0, tk.END)
        entry.insert(tk.END, current + value)

def clear_entry():
    if calculator_on:
        entry.delete(0, tk.END)

def backspace():
    if calculator_on:
        current = entry.get()
        entry.delete(0, tk.END)
        entry.insert(tk.END, current[:-1])

def evaluate():
    if calculator_on:
        expression = entry.get()
        expression = expression.replace('÷', '/').replace('^', '**')
        
        if '/0' in expression:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Erreur: Division par 0")
            return
        
        if validate_expression(expression):
            result = eval(expression)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        else:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Erreur")

def validate_expression(expression):
    allowed_chars = "0123456789.+-*/()x "
    for char in expression:
        if char not in allowed_chars:
            return False
    return True

def apply_sqrt():
    if calculator_on:
        value = entry.get()
        if value != "" and value.isnumeric():
            value = float(value)
            result = math.sqrt(value)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        else:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Erreur")

def apply_ln():
    if calculator_on:
        value = entry.get()
        if value != "" and value.replace('.', '', 1).isdigit():
            value = float(value)
            if value > 0:
                result = math.log(value)
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(result))
            else:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Erreur: Positif requis")
        else:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Erreur")

def apply_exp():
    if calculator_on:
        value = entry.get()
        if value != "" and value.replace('.', '', 1).isdigit():
            value = float(value)
            result = math.exp(value)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        else:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Erreur")

def plot_function():
    if calculator_on:
        expression = entry.get().replace('^', '**').replace('÷', '/')
        if 'x' in expression:
            plot_and_save_function(expression)
        else:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Erreur: Fonction non valide")

x = symbols('x')

def derivee():
    if calculator_on:
        expression = entry.get().replace('^', '**').replace('÷', '/')
        if 'x' in expression:
            expr = sympify(expression)
            derivative = diff(expr, x)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(derivative))

def primitive():
    if calculator_on:
        expression = entry.get().replace('^', '**').replace('÷', '/')
        if 'x' in expression:
            expr = sympify(expression)
            primitive_expr = integrate(expr, x)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(primitive_expr))

def resoudre():
    if calculator_on:
        expression = entry.get().replace('^', '**').replace('÷', '/')
        if 'x' in expression:
            expr = sympify(expression)
            solutions = solve(expr, x)
            entry.delete(0, tk.END)
            entry.insert(tk.END, ', '.join(map(str, solutions)))


buttons = [
    'On', 'Off', 'x', 'ln(x)',
    'Graph', 'Dérivée', 'Primitive', 'Résoudre',
    '√', '^', 'e^x', 'C',
    '(', ')', '⌫', '÷',
    '7', '8', '9', '*',
    '4', '5', '6', '-',
    '1', '2', '3', '+',
    '.', '0', '=', 'Entrer'
]

row_val = 1
col_val = 0

for button in buttons:
    if button == '=':
        action = evaluate
    elif button == 'C':
        action = clear_entry
    elif button == '⌫':
        action = backspace
    elif button == '√':
        action = apply_sqrt
    elif button == 'ln(x)':
        action = apply_ln
    elif button == 'e^x':
        action = apply_exp
    elif button == 'Graph':
        action = plot_function
    elif button == 'Dérivée':
        action = derivee
    elif button == 'Primitive':
        action = primitive
    elif button == 'Résoudre':
        action = resoudre
    elif button == 'x':
        action = lambda: button_click('x')
    elif button == 'Entrer':
        action = evaluate
    elif button == 'On':
        action = enable_calculator
    elif button == 'Off':
        action = disable_calculator
    else:
        action = lambda b=button: button_click(b)

    btn = tk.Button(root, text=button, command=action, **button_params)
    btn.grid(row=row_val, column=col_val, sticky="nsew", padx=0, pady=0)

    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

for i in range(10):
    root.grid_rowconfigure(i, weight=1)

for i in range(4):
    root.grid_columnconfigure(i, weight=1)

root.mainloop()