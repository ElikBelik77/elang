class Statement:
    def compile(self, context):
        pass


class HasValue:
    def get_value(self, context):
        pass


class Return(Statement):
    def __init__(self, expression):
        self.expression = expression

    def get_mentions(self):
        return self.expression.get_mentions()


class FunctionCall(Statement):
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


class Mult(Statement):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_mentions(self):
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 2


class Div(Statement):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_mentions(self):
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 2


class Plus(Statement):
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


class Minus(Statement):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_mentions(self):
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 1


class Assignment(Statement):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_mentions(self):
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 3


class VariableGet(Statement, HasValue):
    def __init__(self, name):
        self.name = name

    def get_mentions(self):
        return [self.name]

    def get_value(self, context):
        pass


class VariableDeclaration(Statement):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class ConstantValue(HasValue):
    def __init__(self, value):
        self.value = value

    def get_mentions(self):
        return []

    def get_value(self, context):
        pass
