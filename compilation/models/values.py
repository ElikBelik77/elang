from compilation.models.base import *


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


