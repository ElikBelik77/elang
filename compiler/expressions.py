class Statement:
    def compile(self, context):
        pass


class HasValue:
    def get_value(self, context):
        pass


class Return(Statement):
    def __init__(self, var):
        self.return_var = var


class FunctionCall(Statement):
    def __init__(self, name, arguments):
        self.arguments = arguments
        self.name = name

    def get_precedence(self):
        return 3


class Mult(Statement):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_precedence(self):
        return 2


class Div(Statement):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_precedence(self):
        return 2


class Plus(Statement):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_precedence(self):
        return 1


class LeftParenthesis:
    def get_precendence(self):
        return -1


class Minus(Statement):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_precedence(self):
        return 1


class Int(Statement, HasValue):
    def __init__(self, name):
        self.name = name

    def get_value(self, context):
        pass


class ConstantValue(HasValue):
    def __init__(self, value):
        self.value = value

    def get_value(self, context):
        pass
