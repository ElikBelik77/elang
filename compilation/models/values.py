from typing import List

from compilation.models.base import Compilable


class StringConstantValue:
    def __init__(self, value):
        self.value = value

    def is_constant(self) -> bool:
        return True

    def get_mentions(self) -> List[str]:
        return []

    def evaluate(self):
        return ord(self.value)


class DecimalConstantValue:
    """
    Model for immediate decimal values.
    """

    def __init__(self, value: int):
        self.value = value

    def is_constant(self):
        return True

    def get_mentions(self) -> List[str]:
        return []

    def evaluate(self):
        return self.value

    def has_ptr_type(self):
        return False


class FunctionCall(Compilable):
    """
    Model for function calls
    """

    def __init__(self, name: str, arguments: [], constructor_of: "ElangClass"):
        self.arguments = arguments
        self.name = name
        self.constructor_call = constructor_of

    def get_mentions(self) -> List[str]:
        mentions = []
        for argument in self.arguments:
            mentions += argument.get_mentions()
        return mentions

    def is_constant(self):
        return False

    def get_precedence(self):
        return 3

    def has_ptr_type(self):
        return False  # TODO: take into account return type of function to determine ptr
