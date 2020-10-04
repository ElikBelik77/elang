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


class Function:
    def __init__(self, name, arguments, return_type, scope, plaintext):
        self.body = []
        self.arguments = arguments
        self.return_statements = None
        self.return_type = return_type
        self.name = name
        self.scope = scope
        self.plain_text = plaintext

    def parse_body(self):
        pass


class Scope:
    def __init__(self, name, parent_scope, start_pos, end_pos=-1):
        self.parent_scope = parent_scope
        self.defined_variables = {}
        self.name = name
        self.start_pos = start_pos
        self.end_pos = end_pos
