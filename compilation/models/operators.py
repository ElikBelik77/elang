from compilation.models.base import *


class MultiplicationOperator(BinaryOperator):
    """
    Model for multiplication operator
    """

    def get_precedence(self):
        return 2

    def evaluate(self):
        return self.left * self.right


class DivisionOperator(BinaryOperator):
    """
    Model for divide operator
    """

    def get_precedence(self):
        return 2

    def evaluate(self):
        return self.left // self.right


class AdditionOperator(BinaryOperator):
    """
    Model for addition operator
    """

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


class SubtractOperator(BinaryOperator):
    """
    Model for subtraction operator
    """

    def get_precedence(self):
        return 1

    def evaluate(self):
        return self.left - self.right


class LogicalAnd(BinaryOperator):

    def get_precedence(self):
        return 1

    def evaluate(self):
        return 1 if self.left and self.right else 0


class LogicalOr(BinaryOperator):

    def get_precedence(self):
        return 1

    def evaluate(self):
        return 1 if self.left or self.right else 0


class LogicalGreater(BinaryOperator):

    def get_precedence(self):
        return 1

    def evaluate(self):
        return 1 if self.left > self.right else 0


class Equal(BinaryOperator):

    def get_precedence(self):
        return 1

    def evaluate(self):
        return 1 if self.left == self.right else 0


class Assignment(BinaryOperator):
    """
    Model for assignment operator
    """

    def get_precedence(self):
        return 0


class ArrayIndexer(BinaryOperator):

    def get_precedence(self):
        return 4


class DotOperator(BinaryOperator):
    def get_precedence(self):
        return 3

    def get_mentions(self) -> List[str]:
        if isinstance(self.left, PointerVariable):  # TODO: properly check semantics of dot operator
            return [self.left.name]
        return []

    def convert_ptr_types(self, var_list):
        if isinstance(self.right, Variable):
            self.right = self.right.to_ptr_type()
        elif isinstance(self.right, BinaryOperator) or isinstance(self.right, UnaryOperator):
            self.right.convert_ptr_types(var_list)
        if isinstance(self.left, Variable):
            self.left = self.left.to_ptr_type()
        elif isinstance(self.left, BinaryOperator) or isinstance(self.left, UnaryOperator):
            self.left.convert_ptr_types(var_list)


class NewOperator(UnaryOperator):
    def get_precedence(self):
        return 3

    def get_mentions(self):
        return []
