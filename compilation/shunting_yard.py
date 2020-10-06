from models import *
import queue


def reversequeue(queue: queue.Queue):
    Stack = []
    while (not queue.empty()):
        Stack.append(queue.queue[0])
        queue.get()
    while (len(Stack) != 0):
        queue.put(Stack[-1])
        Stack.pop()


def shunting_yard(statements: [Compilable]):
    output_queue = queue.Queue()
    operator_stack = []
    while len(statements) is not 0:
        current = statements.pop(0)
        if isinstance(current, DecimalConstantValue) or isinstance(current, Variable):
            output_queue.put(current)
        elif isinstance(current, FunctionCall):
            operator_stack.append(FunctionCall(current.name, current.arguments))
        elif isinstance(current, Assignment) or isinstance(current, Mult) or isinstance(current, Div) or isinstance(
                current, Plus) or isinstance(current, Minus):
            while ((len(operator_stack) is not 0) and (
                    operator_stack[-1].get_precedence() >= current.get_precedence()) and (
                           operator_stack[-1].get_precedence() is not -1)):
                output_queue.put(operator_stack.pop())
            operator_stack.append(current)
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
    reversequeue(output_queue)
    return build_expression(output_queue)


def build_expression(output_queue: queue.Queue):
    expression = output_queue.get()
    if isinstance(expression, Mult) or isinstance(expression, Plus) or isinstance(expression, Div) or isinstance(
            expression, Minus) or isinstance(expression, Assignment):
        expression.right = build_expression(output_queue)
        expression.left = build_expression(output_queue)
    if isinstance(expression, DecimalConstantValue) or isinstance(expression, Variable) or isinstance(expression,
                                                                                                      FunctionCall):
        return expression
    return expression


def create_operator(value: str):
    if value == "*":
        return Mult()
    elif value == "/":
        return Div()
    elif value == '-':
        return Minus()
    elif value == '+':
        return Plus()
    elif value == "=":
        return Assignment()
