class NameMatch:
    def __init__(self, value):
        self.value = value.strip()


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


class FunctionCallMatch:
    def __init__(self, name, arguments):
        self.arguments = arguments
        self.name = name.strip()


class Function:
    def __init__(self, name, arguments, return_type, scope, plaintext):
        self.body = []
        self.arguments = arguments
        self.return_statements = []
        self.return_type = return_type
        self.name = name
        self.scope = scope
        self.plain_text = plaintext

    def parse_body(self):
        pass



