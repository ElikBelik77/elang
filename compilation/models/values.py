from compilation.models.base import *


class Variable(Compilable):
    """
    Model for variable mentions
    """

    def __init__(self, name: str):
        self.name = name

    def is_constant(self):
        return False

    def get_mentions(self) -> List[str]:
        return [self.name]


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


class FunctionCall(Compilable):
    """
    Model for function calls
    """

    def __init__(self, name: str, arguments: []):
        self.arguments = arguments
        self.name = name

    def get_mentions(self) -> List[str]:
        mentions = []
        for argument in self.arguments:
            mentions += argument.get_mentions()
        return mentions

    def is_constant(self):
        return False

    def get_precedence(self):
        return 3
