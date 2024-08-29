from console import Console
from calc import Calculator

console = Console()
calculator = Calculator()
opts = [
    ("1", "Add 2 numbers"),
    ("2", "Substract 2 numbers"),
    ("3", "Multiply 2 numbers"),
    ("4", "Divide 2 numbers"),
    ("5", "Modulo of 2 numbers"),
    ("6", "Evaluate mathematical expression"),
    ("7", "Credits"),
    ("8", "Exit")
]
title = """Arithmetic Calculator
This calculator lets you do mathematical operation such as add, substract, multiply
divide, or get the modulo of two floating-point numbers.
Also, you can evaluate a mathematical expression made of parenthesis and the 
aforementioned operations."""

mathexpr_info = """This tool will let you evaluate mathematical expressions with the 
allowed operations (+,-,*,/,%) and parenthesis.

Example:
8+9(7-8)+4*(5/78)%4
Result = -0.7435897435897436
"""

def read_2_numbers():
    a = console.read_float("Enter the first number: ")
    b = console.read_float("Enter the second number: ")
    return a, b

console.print(title)
while True:
    selected = console.select_from_menu("Select any of these options", opts)
    try:
        if selected == "1":
            a, b = read_2_numbers()
            console.print(f"Result = {calculator.add(a,b)}")
        elif selected == "2":
            a, b = read_2_numbers()
            console.print(f"Result = {calculator.sub(a,b)}")
            
        elif selected == "3":
            a, b = read_2_numbers()
            console.print(f"Result = {calculator.mul(a,b)}")
            
        elif selected == "4":
            a, b = read_2_numbers()
            console.print(f"Result = {calculator.div(a,b)}")
            
        elif selected == "5":
            a, b = read_2_numbers()
            console.print(f"Result = {calculator.mod(a,b)}")
            
        elif selected == "6":
            console.print(mathexpr_info)
            expression = console.read_string("Enter the mathematical expression: ")
            console.print(f"Result = {calculator.evaluate(expression)}")
            
        elif selected == "7":
            console.credits()
        else:
            break
    except (ValueError, ZeroDivisionError) as valerr:
        console.error(str(valerr))
    console.print("Press Enter to continue...")
    console.read_string()

