import math


class Parser:
    def __init__(self):
        pass

    # Using decorator @staticmethod, you need to throw away "self" argument
    @staticmethod
    def __convert_type(value_str):
        result = 0
        if "." in value_str:
            result = float(value_str)
        else:
            result = int(value_str)
        return result


    @staticmethod
    def _determination(expression):
        symbols = "+-*/^"
        op = ""
        for char in expression:
            if char == expression[0]:
                if char in "-":
                    continue
                elif char in "sl":
                    op = char
                    break
            elif char in symbols:
                op = char
                break
        return op

    def _parse(self, expression):
        symbols = "+-*/^"
        op = self._determination(expression)
        try:
            if op in symbols:
                a, b = expression.split(op)
                a = a.replace("(", "").replace(")", "")
                b = b.replace("(", "").replace(")", "")
            elif op == "s":
                a = expression.replace("sqrt", "").replace("(", "").replace(")", "")
                b = "0"
            elif op == "l":
                expression = expression.replace("log", "").replace("(", "").replace(")", "")
                a, b = expression.split(",")
            return self.__convert_type(a), self.__convert_type(b), op
        except:
            print("""Something wrong, check your expression.
The calculator supports following functions:
a+b, a-b, a*b, a/b, a^b, sqrt(a), log(a, b)""")
            return 0, 0, "+"


class Core:
    def __init__(self):
        self._parser = Parser()
        self._functions = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "^": lambda a, b: a ** b,
            "s": lambda a, b: math.sqrt(a + b),
            "l": math.log
        }

    def _calculate(self, expression):
        a, b, op = self._parser._parse(expression)
        result = self._functions.get(op)(a, b)
        return result


class Interface:
    def __init__(self):
        self._core = Core()

    def run(self):
        while True:
            print("Enter your expression:")
            expression = input()
            result = self._core._calculate(expression)
            print("Result is {}".format(result))
            print("=" * 10)


if __name__ == "__main__":
    calculator = Interface()
    calculator.run()
