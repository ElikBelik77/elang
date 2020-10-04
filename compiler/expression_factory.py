from expressions import *
from parsing_models import *
import queue


def precedence(statement, precedence={'*': 1, '/': '1', '+': 0, '-': 0}):
    if isinstance(statement, FunctionCall):
        return 3
    return precedence[statement.value]


def reversequeue(queue):
    Stack = []
    while (not queue.empty()):
        Stack.append(queue.queue[0])
        queue.get()
    while (len(Stack) != 0):
        queue.put(Stack[-1])
        Stack.pop()


def shunting_yard(statements: []):
    output_queue = queue.Queue()
    operator_stack = []
    while len(statements) is not 0:
        current = statements.pop(0)
        if isinstance(current, ConstantMatch):
            output_queue.put(ConstantValue(current.value))
        if isinstance(current, NameMatch):
            output_queue.put(VariableGet(current.value))
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
    reversequeue(output_queue)
    return build_expression(output_queue)


def build_expression(output_queue):
    expression = output_queue.get()
    if isinstance(expression, Mult) or isinstance(expression, Plus) or isinstance(expression, Div) or isinstance(
            expression, Minus) or isinstance(expression, Assignment):
        expression.right = build_expression(output_queue)
        expression.left = build_expression(output_queue)
    if isinstance(expression, ConstantValue) or isinstance(expression, VariableGet) or isinstance(expression,
                                                                                                  FunctionCall):
        return expression
    return expression


def create_operator(value):
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


class ReturnFactory:
    def produce(self, function, statements):
        expression = shunting_yard(statements[1:])
        function.return_statements.append(Return(expression))
        return [function.return_statements[-1]]


class IntFactory:
    def produce(self, function, statements):
        expression = shunting_yard(statements[1:])
        return [VariableDeclaration(statements[1].value, statements[0].value), expression]
