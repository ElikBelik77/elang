from compilation.models.base import *


class MultiplicationOperator(Compilable, BinaryOperator):
    """
    Model for multiplication operator
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def is_constant(self):
        return self.left.is_constant() and self.right.is_constant()

    def get_mentions(self) -> List[str]:
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 2

    def evaluate(self):
        return self.left * self.right


class DivisionOperator(Compilable, BinaryOperator):
    """
    Model for divide operator
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        return self.left.get_mentions() + self.right.get_mentions()

    def is_constant(self):
        return self.left.is_constant() and self.right.is_constant()

    def get_precedence(self):
        return 2

    def evaluate(self):
        return self.left // self.right


class AdditionOperator(Compilable, BinaryOperator):
    """
    Model for addition operator
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        return self.left.get_mentions() + self.right.get_mentions()

    def is_constant(self):
        return self.left.is_constant() and self.right.is_constant()

    def get_precedence(self):
        return 1

    def evaluate(self):
        return self.left + self.right


class LeftParenthesis:
    """
    Model for left parenthesis
    """

    def get_precedence(self):
        return -1


class RightParenthesis:
    def get_precedence(self):
        return -1


class SubtractOperator(Compilable, BinaryOperator):
    """
    Model for subtraction operator
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        return self.left.get_mentions() + self.right.get_mentions()

    def is_constant(self):
        return self.left.is_constant() and self.right.is_constant()

    def get_precedence(self):
        return 1

    def evaluate(self):
        return self.left - self.right


class LogicalAnd(Compilable, BinaryOperator):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def is_constant(self):
        return self.left.is_constant() and self.right.is_constant()

    def get_precedence(self):
        return 1

    def evaluate(self):
        return 1 if self.left and self.right else 0


class LogicalOr(Compilable, BinaryOperator):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def is_constant(self):
        return self.left.is_constant() and self.right.is_constant()

    def get_precedence(self):
        return 1

    def evaluate(self):
        return 1 if self.left or self.right else 0


class LogicalGreater(Compilable, BinaryOperator):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def is_constant(self):
        return self.left.is_constant() and self.right.is_constant()

    def get_precedence(self):
        return 1

    def evaluate(self):
        return 1 if self.left > self.right else 0


class Equal(Compilable, BinaryOperator):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def is_constant(self):
        return self.left.is_constant() and self.right.is_constant()

    def get_precedence(self):
        return 1

    def evaluate(self):
        return 1 if self.left == self.right else 0


class Assignment(Compilable, BinaryOperator):
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
        return 0


class ArrayIndexer(Compilable, BinaryOperator):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def get_precedence(self):
        return 4

    def is_constant(self):
        return False
