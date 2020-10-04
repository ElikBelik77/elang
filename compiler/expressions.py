class Statement:
    def compile(self, context):
        pass


class HasValue:
    def get_value(self, context):
        pass


class Return(Statement):
    def __init__(self, expression):
        self.expression = expression


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
    def get_precedence(self):
        return -1


class RightParenthesis:
    def get_precedence(self):
        return -1


class Minus(Statement):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_precedence(self):
        return 1


class Assignment(Statement):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_precedence(self):
        return 3


class Variable(Statement, HasValue):
    def __init__(self, name):
        self.name = name

    def get_value(self, context):
        pass


class ConstantValue(HasValue):
    def __init__(self, value):
        self.value = value

    def get_value(self, context):
        pass
