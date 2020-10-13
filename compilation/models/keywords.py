from compilation.models.base_classes import *


class Return(Compilable):
    """
    Model for the 'return' statement
    """

    def __init__(self, expression: Compilable):
        self.expression = expression

    def get_mentions(self) -> List[str]:
        return self.expression.get_mentions()


class VariableDeclaration(Compilable):
    """
    Model for variable declaration
    """

    def __init__(self, name: str, var_type: str):
        self.name = name
        self.var_type = var_type

    def get_mentions(self) -> List[str]:
        return [self.name]


class If(Scopeable):
    """
    Model for if statements
    """

    def __init__(self, scope: Scope, body: List[Compilable], condition: Compilable):
        super(If, self).__init__(scope, body)
        self.condition = condition


class Function(Scopeable):
    """
    Model for functions
    """

    def __init__(self, scope: Scope, name: str, signature: str, return_type: str, body: List[Compilable],
                 arguments: List[VariableDeclaration]):
        super(Function, self).__init__(scope, body)
        self.name = name
        self.signature = signature
        self.return_type = return_type
        self.arguments = arguments


class While(Scopeable):
    def __init__(self, scope: Scope, body: List[Compilable], condition: Compilable):
        super(While, self).__init__(scope, body)
        self.condition = condition
