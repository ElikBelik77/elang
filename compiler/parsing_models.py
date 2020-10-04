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


class Scope:
    def __init__(self, name, parent_scope, start_pos, end_pos=-1):
        self.parent_scope = parent_scope
        self.defined_variables = {}
        self.name = name
        self.start_pos = start_pos
        self.end_pos = end_pos

    def search_variable(self, name):
        if name in self.defined_variables:
            return True
        if self.parent_scope is None:
            return False
        return self.parent_scope.search_variable(name)
