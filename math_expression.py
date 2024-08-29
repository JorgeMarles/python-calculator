from re import sub
from typing import List
from calc import Calculator

class Operator:
    def __init__(self, num: str | float) -> None:
        self.num: float = 0
        if isinstance(num, float) or Operator.isnumeric(num):
            self.num = float(num)
        else:
            raise ValueError(f"{num} does not represent a number")

    def __str__(self) -> str:
        return str(self.num)

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def isnumeric(s: str) -> bool:
        if s.startswith("-"):
            return Operator.isnumeric(s[1:])
        return s.replace(".", "", 1).isdigit()


class Operation:
    def __init__(self, op: str, calc: Calculator) -> None:
        if not Operation.is_op(op):
            raise ValueError(f"Unknown operation: {op}")
        self.op = op
        self.calc = calc

    def __str__(self) -> str:
        return self.op

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, a: float, b: float) -> float:
        if self.op == "+":
            return self.calc.add(a, b)
        elif self.op == "*":
            return self.calc.mul(a, b)
        elif self.op == "/":
            return self.calc.div(a, b)
        elif self.op == "%":
            return self.calc.mod(a, b)
        else:
            raise ValueError(f"Unknown operation: {self.op}")

    def get_prior(self) -> float:
        if self.op in ("(", ")"):
            return 0
        elif self.op == "+":
            return 1
        elif self.op in ("*", "/", "%"):
            return 2
        else:
            raise ValueError(f"Unknown operation: {self.op}")

    @staticmethod
    def is_op(op: str) -> bool:
        return op in ("+", "*", "/", "%", "(", ")")


class MathExpression:
    def __init__(self, expr: str, calc: Calculator) -> None:
        if not MathExpression.valid_parenthesis(expr):
            raise ValueError("Unbalanced Parenthesis")
        self.infix = self._normalize(expr)
        self.calc = calc
        self.idx = 0

    def __str__(self) -> str:
        return self.infix

    def __repr__(self) -> str:
        return self.__str__()

    def _normalize(self, operation: str) -> str:
        # delete spaces
        operation = sub(r"\s", "", operation)
        # delete double negatives (-- => +)
        operation = operation.replace("--", "+")
        # normalize substraction form
        operation = operation.replace("+-", "-")
        # convert substraction form (x-y => x+-y)
        operation = sub(r"(\)|\d)-", r"\1+-", operation)
        # implicit multiplication in parenthesis
        operation = operation.replace(")(", ")*(")
        # manage multiplications of a number and a parenthesis
        operation = sub(r"(\d)\(", r"\1*(", operation)
        operation = sub(r"\)(\d)", r")*\1", operation)
        # manage negative parenthesis
        operation = operation.replace("-(", "-1*(")
        # manage reduntand positives (+a) => (a)
        operation = sub(r"(\(|^)\+(\d)", r"\1\2", operation)
        return operation

    def __next__(self) -> Operation | Operator:
        if self.idx >= len(self.infix):
            self.idx = 0
            raise StopIteration

        token: str = self.infix[self.idx]
        if Operation.is_op(token):
            self.idx += 1
            return Operation(token, self.calc)

        current = ""
        while self.idx < len(self.infix):
            token = self.infix[self.idx]
            if Operation.is_op(token):
                break
            current += token
            self.idx += 1

        return Operator(current)

    def __iter__(self):
        return self

    def _to_postfix(self) -> List[Operation | Operator]:
        postfix: List[Operation | Operator] = []
        op_stack: List[Operation] = []
        for element in self:
            if isinstance(element, Operator):
                postfix.append(element)
            else:
                if element.op == "(":
                    op_stack.append(element)
                elif element.op == ")":
                    while op_stack and op_stack[-1].op != "(":
                        postfix.append(op_stack.pop())
                    if op_stack:
                        op_stack.pop()
                else:
                    if op_stack:
                        prior_top = op_stack[-1].get_prior()
                        prior_elm = element.get_prior()
                        prior_ok = prior_elm <= prior_top
                        while op_stack and op_stack[-1].op != "(" and prior_ok:
                            postfix.append(op_stack.pop())
                            prior_top = op_stack[-1].get_prior()
                            prior_ok = prior_elm <= prior_top
                    op_stack.append(element)
        while op_stack:
            if op_stack[-1].op != "(":
                postfix.append(op_stack.pop())
        return postfix

    def evaluate(self) -> float:
        postfix = self._to_postfix()
        stack: List[float] = []
        for element in postfix:
            if isinstance(element, Operation):
                try:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(element(b, a))
                except IndexError:
                    raise ValueError("Missing numbers in expression") from IndexError
            else:
                stack.append(element.num)
        try:
            return stack.pop()
        except IndexError:
            raise ValueError("Missing numbers in expression") from IndexError

    @staticmethod
    def valid_parenthesis(s: str) -> bool:
        x = 0
        ok = True
        for c in s:
            if c == "(":
                x += 1
            elif c == ")":
                x -= 1
                if x < 0:
                    ok = False
                    break
        return x == 0 and ok


if __name__ == "__main__":
    expresion = input()
    try:
        mathexp = MathExpression(expresion)
        # print("infix ="," ".join([str(el) for el in mathexp]))
        print(mathexp.evaluate())
    except Exception as excp:
        print(f"{type(excp).__name__}: {excp}")
