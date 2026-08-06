import sympy as sp

def calculate(expression):
    try:
        result = sp.sympify(expression)
        return result
    except:
        return "Invalid calculation"

while True:
    user = input("Calculate: ")

    if user == "exit":
        break

    print("Answer:", calculate(user))
