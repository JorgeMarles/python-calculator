from math_expression import MathExpression

class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b

    def sub(self, a: float, b: float) -> float:
        return a - b

    def mul(self, a: float, b: float) -> float:
        return a * b

    def div(self, a: float, b: float) -> float:
        self.check_divisor(b)
        return a / b

    def mod(self, a: float, b: float) -> float:
        self.check_divisor(b)
        return a % b
    
    def evaluate(self, expr: str) -> float:
        mathexpr = MathExpression(expr)
        return mathexpr.evaluate()
    
    def check_divisor(self, b: float) -> None: 
        if b == 0:
            raise ZeroDivisionError("Divisor can't be zero")
        
