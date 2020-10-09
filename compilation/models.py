from typing import List


class Compilable:
    def compile(self, context):
        pass

    def get_mentions(self):
        pass


class Scopeable(Compilable):
    def __init__(self, scope: "Scope", body: List[Compilable]):
        self.scope = scope
        self.body = body


class HasValue:
    def get_value(self, context):
        pass


class Return(Compilable):
    def __init__(self, expression: Compilable):
        self.expression = expression

    def get_mentions(self):
        return self.expression.get_mentions()


class FunctionCall(Compilable):
    def __init__(self, name: str, arguments: ["Variable"]):
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
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self):
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 2


class Div(Compilable):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self):
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 2


class Plus(Compilable):
    def __init__(self, left: Compilable = None, right: Compilable = None):
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
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self):
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 1


class Assignment(Compilable):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self):
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def get_precedence(self):
        return 3


class Variable(Compilable, HasValue):
    def __init__(self, name: str):
        self.name = name

    def get_mentions(self):
        return [self.name]

    def get_value(self, context):
        pass


class VariableDeclaration(Compilable):
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type

    def get_mentions(self):
        return [self.name]


class DecimalConstantValue(HasValue):
    def __init__(self, value: int):
        self.value = value

    def get_mentions(self):
        return []

    def get_value(self, context):
        pass


class Scope:
    def __init__(self, name: str, parent_scope: "Scope"):
        self.parent_scope = parent_scope
        self.children: [Scope] = []
        if parent_scope is not None:
            self.parent_scope.children.append(self)
        self.defined_variables = {}
        self.name = name

    def get_childrens(self):
        children = []
        for child in self.children:
            children += child.get_childrens()
        return children + self.children

    def is_child_of(self, parent):
        p = self.parent_scope
        while p is not None:
            if p == parent:
                return True
        return False

    def search_variable(self, name: str):
        if name in self.defined_variables:
            return self.defined_variables[name]
        if self.parent_scope is None:
            return None
        return self.parent_scope.search_variable(name)


class Function(Scopeable):
    def __init__(self, scope: Scope, name: str, signature: str, return_type: str, body: List[Compilable],
                 arguments: List[VariableDeclaration]):
        super(Function, self).__init__(scope, body)
        self.name = name
        self.signature = signature
        self.return_type = return_type
        self.arguments = arguments

    def get_mentions(self):
        mentions = []
        for expression in self.body:
            mentions += expression.get_mentions()
        return mentions


class Program(Compilable):
    def __init__(self, functions: List[Function]):
        self.functions = functions
