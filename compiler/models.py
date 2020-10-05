class Compilable:
    def compile(self, context):
        pass


class HasValue:
    def get_value(self, context):
        pass


class Return(Compilable):
    def __init__(self, expression):
        self.expression = expression

    def get_mentions(self):
        return self.expression.get_mentions()


class FunctionCall(Compilable):
    def __init__(self, name, arguments):
        self.arguments = arguments
        self.name = name

    def get_mentions(self):
        mentions = []
        for argument in self.arguments:
            mentions += argument.get_mentions()
        return mentions

    def get_precedence(self):
        return 3


class Mult(Compilable):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_mentions(self):
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 2


class Div(Compilable):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_mentions(self):
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 2


class Plus(Compilable):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_mentions(self):
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 1


class LeftParenthesis:
    def get_precedence(self):
        return -1


class RightParenthesis:
    def get_precedence(self):
        return -1


class Minus(Compilable):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_mentions(self):
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 1


class Assignment(Compilable):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_mentions(self):
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def get_precedence(self):
        return 3


class Variable(Compilable, HasValue):
    def __init__(self, name):
        self.name = name

    def get_mentions(self):
        return [self.name]

    def get_value(self, context):
        pass


class VariableDeclaration(Compilable):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def get_mentions(self):
        return [self.name]


class DecimalConstantValue(HasValue):
    def __init__(self, value):
        self.value = value

    def get_mentions(self):
        return []

    def get_value(self, context):
        pass


class Scope:
    def __init__(self, name, parent_scope: "Scope"):
        self.parent_scope = parent_scope
        self.defined_variables = {}
        self.name = name

    def search_variable(self, name):
        if name in self.defined_variables:
            return True
        if self.parent_scope is None:
            return False
        return self.parent_scope.search_variable(name)


class Function:
    def __init__(self, scope, signature, return_type, body, arguments):
        self.scope = scope
        self.signature = signature
        self.return_type = return_type
        self.body = body
        self.arguments = arguments

    def get_mentions(self):
        mentions = []
        for expression in self.body:
            mentions += expression.get_mentions()
        return mentions