from compilation.models import *
import queue


def reversequeue(queue: queue.Queue):
    """
    This function reverses a queue, used by shunting yard to produce the parsed expression.
    :param queue: the queue to reverse.
    :return: a reversed queue.
    """
    stack = []
    while not queue.empty():
        stack.append(queue.queue[0])
        queue.get()
    while len(stack) != 0:
        queue.put(stack[-1])
        stack.pop()


def shunting_yard(expressions: [Compilable]):
    """
    Shunting yard algorithm for parsing expressions.
    :param expressions: the expressions to parse.
    :return: a tree containing the operations and operand in the correct order.
    """
    output_queue = queue.Queue()
    operator_stack = []
    while len(expressions) is not 0:
        current = expressions.pop(0)
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
    """
    This function builds an expression from an output queue given by the shunting yard algorithm.
    :param output_queue: the output_queue from shunting yard.
    :return: an expression tree representing the queue.
    """
    expression = output_queue.get()
    if isinstance(expression, Mult) or isinstance(expression, Plus) or isinstance(expression, Div) or isinstance(
            expression, Minus) or isinstance(expression, Assignment):
        expression.right = build_expression(output_queue)
        expression.left = build_expression(output_queue)
    if isinstance(expression, DecimalConstantValue) or isinstance(expression, Variable) or isinstance(expression,
                                                                                                      FunctionCall):
        return expression
    return expression
