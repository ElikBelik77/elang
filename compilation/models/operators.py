from typing import List
from compilation.models.base import *


class MultiplicationOperator(Compilable, Operator):
    """
    Model for multiplication operator
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 2


class DivisionOperator(Compilable, Operator):
    """
    Model for divide operator
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 2


class AdditionOperator(Compilable, Operator):
    """
    Model for addition operator
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 1


class LeftParenthesis:
    """
    Model for left parenthesis
    """

    def get_precedence(self):
        return -1


class RightParenthesis:
    def get_precedence(self):
        return -1


class SubtractOperator(Compilable, Operator):
    """
    Model for subtraction operator
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 1


class LogicalAnd(Compilable, Operator):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def get_precedence(self):
        return 1


class LogicalOr(Compilable, Operator):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def get_precedence(self):
        return 1


class LogicalGreater(Compilable, Operator):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def get_precedence(self):
        return 1


class Equal(Compilable, Operator):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def get_precedence(self):
        return 1


class Assignment(Compilable, Operator):
    """
    Model for assignment operator
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def get_precedence(self):
        return 3


class ArrayIndexer(Compilable, Operator):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def get_precedence(self):
        return 4
