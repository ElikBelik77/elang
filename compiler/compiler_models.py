class NameMatch:
    def __init__(self, value):
        self.value = value


class OperatorMatch:
    def __init__(self, value):
        self.value = value


class ArgumentMatch:
    def __init__(self, value):
        self.value = value


class ConstantMatch:
    def __init__(self, value):
        self.value = value


class StringMatch:
    def __init__(self, value):
        self.value = value


class FunctionMatch:
    def __init__(self, name, arguments):
        self.arguments = arguments
        self.name = name
