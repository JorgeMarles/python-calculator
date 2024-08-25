from re import sub
from typing import List


class Operator:
    def __init__(self, num: str | int) -> None:
        self.num: int = 0
        if isinstance(num, int) or Operator.isnumeric(num):
            self.num = int(num)
        else:
            raise ValueError(f"{num} does not represent an integer number")

    def __str__(self) -> str:
        return str(self.num)

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def isnumeric(s: str) -> bool:
        if s.startswith("-"):
            s = s[1:]
        # for floating point:
        # return s.replace('.', '', 1).isdigit()
        return s.isdigit()


class Operation:
    def __init__(self, op: str) -> None:
        if not Operation.is_op(op):
            raise Exception(f"Unknown operation: {op}")
        self.op = op

    def __str__(self) -> str:
        return self.op

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, a: int, b: int) -> int:
        if self.op == "+":
            return a + b
        elif self.op == "*":
            return a * b
        elif self.op == "/":
            return a // b
        elif self.op == "%":
            return a % b
        else:
            raise ValueError(f"Unknown operation: {self.op}")

    def get_prior(self) -> int:
        if self.op in "()":
            return 0
        elif self.op in "+":
            return 1
        elif self.op in "*/%":
            return 2
        else:
            raise ValueError(f"Unknown operation: {self.op}")

    @staticmethod
    def is_op(op: str) -> bool:
        return op in ["+", "*", "/", "%", "(", ")"]


class MathExpression:
    def __init__(self, expr: str) -> None:
        if not MathExpression.valid_parenthesis(expr):
            raise ValueError("Unbalanced Parenthesis")
        self.infix = self.normalize(expr)
        # print(f"{expr} => Normalized: {self.infix}")
        self.idx = 0

    def __str__(self) -> str:
        return self.infix

    def __repr__(self) -> str:
        return self.__str__()

    def normalize(self, operation: str) -> str:
        # delete spaces
        operation = operation.replace(" ", "")

        # delete double negatives (-- => +)
        operation = operation.replace("--", "+")
        # normalize substraction form
        operation = operation.replace("+-", "-")
        # convert substraction from x-y to x+-y
        operation = sub(r"(\)|\d)-", r"\1+-", operation)
        # implicit multiplication in parenthesis
        operation = operation.replace(")(", ")*(")

        # manage multiplications of a number and a parenthesis
        operation = sub(r"(\d)\(", r"\1*(", operation)
        operation = sub(r"\)(\d)", r")*\1", operation)

        # manage negative parenthesis
        operation = operation.replace("-(", "-1*(")

        return operation

    def __next__(self) -> Operation | Operator:
        try:
            if self.idx >= len(self.infix):
                self.idx = 0
                raise StopIteration
            token: str = self.infix[self.idx]

            if Operation.is_op(token):
                self.idx += 1
                return Operation(token)

            current = ""
            while self.idx < len(self.infix):
                token = self.infix[self.idx]
                if Operation.is_op(token):
                    break
                current += token
                self.idx += 1

            return Operator(current)
        except Exception as excp:
            raise excp

    def __iter__(self):
        return self

    def to_postfix(self) -> List[Operation | Operator]:
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
                    op_stack.append(element)
            # print(op_stack, postfix)
        while op_stack:
            if op_stack[-1].op != "(":
                postfix.append(op_stack.pop())
        # print(postfix)
        return postfix

    def evaluate(self) -> int:
        postfix = self.to_postfix()
        stack: List[int] = []
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
        print(mathexp.evaluate())
    except Exception as excp:
        print(f"{type(excp).__name__}: {excp}")
