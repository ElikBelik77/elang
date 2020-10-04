from expressions import *
from parsing_models import *
import queue


def precedence(statement, precedence={'*': 1, '/': '1', '+': 0, '-': 0}):
    if isinstance(statement, FunctionCall):
        return 3
    return precedence[statement.value]


def shunting_yard(statements: [], ):
    output_queue = queue.Queue()
    operator_stack = []
    while len(statements) is not 0:
        current = statements.pop(0)
        if isinstance(current, ConstantMatch):
            output_queue.put(ConstantValue(current.value))
        elif isinstance(current, FunctionCallMatch):
            operator_stack.append(FunctionCall(current.name, current.arguments))
        elif isinstance(current, OperatorMatch):
            token = create_operator(current.value)
            while ((len(operator_stack) is not 0) and (
                    operator_stack[-1].get_precedence() >= token.get_precedence()) and (
                           operator_stack[-1].get_precedence() is not -1)):
                output_queue.put(operator_stack.pop())
            operator_stack.append(token)
        elif isinstance(current, LeftParenthesis):
            operator_stack.append(current)
        elif isinstance(current, RightParenthesis):
            while not isinstance(operator_stack[-1], LeftParenthesis):
                if len(operator_stack) == 1:
                    raise Exception("Unbalanced parenthesis")
                output_queue.put(operator_stack.pop())
            if isinstance(operator_stack[-1], LeftParenthesis):
                operator_stack.pop()
    while len(operator_stack) is not 0:
        output_queue.put(operator_stack.pop())
    while output_queue.qsize() is not 0:
        print(output_queue.get())


def create_operator(value):
    if value == "*":
        return Mult()
    elif value == "/":
        return Div()
    elif value == '-':
        return Minus()
    elif value == '+':
        return Plus()


class ReturnFactory:
    def produce(self, function, statement):
        shunting_yard(statement[1:])
