from compilation.models.base import *


class Return(Compilable):
    """
    Model for the 'return' statement
    """

    def __init__(self, expression: Compilable):
        self.expression = expression

    def get_mentions(self) -> List[str]:
        return self.expression.get_mentions()


class If(Scopeable):
    """
    Model for if statements
    """

    def __init__(self, scope: Scope, body: List[Compilable], condition: Compilable):
        super(If, self).__init__(scope, body)
        self.condition = condition


class While(Scopeable):
    def __init__(self, scope: Scope, body: List[Compilable], condition: Compilable):
        super(While, self).__init__(scope, body)
        self.condition = condition
