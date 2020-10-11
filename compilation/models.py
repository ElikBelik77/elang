from typing import List


class Compilable:
    """
    Interface for unifying compilable models.
    """

    def get_mentions(self) -> List[str]:
        """
        This function returns the variable that are mentioned in the compilable.
        :return:
        """
        pass


class Operator:
    """
    Interface for unifying operators.
    """

    def get_precedence(self):
        pass


class Scopeable(Compilable):
    """
    Interface for describing models that have their own scope
    """

    def __init__(self, scope: "Scope", body: List[Compilable]):
        self.scope = scope
        self.body = body

    def get_mentions(self) -> List[str]:
        mentions = []
        for expression in self.body:
            mentions += expression.get_mentions()
        return mentions


class Return(Compilable):
    """
    Model for the 'return' statement
    """

    def __init__(self, expression: Compilable):
        self.expression = expression

    def get_mentions(self) -> List[str]:
        return self.expression.get_mentions()


class FunctionCall(Compilable):
    """
    Model for function calls
    """

    def __init__(self, name: str, arguments: []):
        self.arguments = arguments
        self.name = name

    def get_mentions(self) -> List[str]:
        mentions = []
        for argument in self.arguments:
            mentions += argument.get_mentions()
        return mentions

    def get_precedence(self):
        return 3


class Mult(Compilable, Operator):
    """
    Model for multiplication operator
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 2


class Div(Compilable, Operator):
    """
    Model for divide operator
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 2


class Plus(Compilable, Operator):
    """
    Model for addition operator
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 1


class LeftParenthesis:
    """
    Model for left parenthesis
    """

    def get_precedence(self):
        return -1


class RightParenthesis:
    def get_precedence(self):
        return -1


class Minus(Compilable, Operator):
    """
    Model for subtraction operator
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        return self.left.get_mentions() + self.right.get_mentions()

    def get_precedence(self):
        return 1


class LogicalAnd(Compilable, Operator):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def get_precedence(self):
        return 1


class LogicalOr(Compilable, Operator):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def get_precedence(self):
        return 1


class LogicalGreater(Compilable, Operator):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def get_precedence(self):
        return 1


class Equal(Compilable, Operator):
    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def get_precedence(self):
        return 1


class Assignment(Compilable, Operator):
    """
    Model for assignment operator
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_mentions(self) -> List[str]:
        mentions = self.left.get_mentions() + self.right.get_mentions()
        return mentions

    def get_precedence(self):
        return 3


class Variable(Compilable):
    """
    Model for variable mentions
    """

    def __init__(self, name: str):
        self.name = name

    def get_mentions(self) -> List[str]:
        return [self.name]


class VariableDeclaration(Compilable):
    """
    Model for variable declaration
    """

    def __init__(self, name: str, var_type: str):
        self.name = name
        self.var_type = var_type

    def get_mentions(self) -> List[str]:
        return [self.name]


class DecimalConstantValue:
    """
    Model for immediate decimal values.
    """

    def __init__(self, value: int):
        self.value = value

    def get_mentions(self) -> List[str]:
        return []


class Scope:
    """
    Model for a scope
    """

    def __init__(self, name: str, parent_scope: "Scope"):
        self.parent_scope = parent_scope
        self.children: [Scope] = []
        if parent_scope is not None:
            self.parent_scope.children.append(self)
        self.defined_variables = {}
        self.name = name

    def get_children(self):
        """
        This function gets all of the children of the scope
        :return: list of all the child scopes of this scope
        """
        children = []
        for child in self.children:
            children += child.get_children()
        return children + self.children

    def is_child_of(self, parent):
        """
        This function checks if this scope is a descendant of another scope.
        :param parent: the parent to check.
        :return: True if this scope is a descendant of the parent, false otherwise.
        """
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


class Program(Compilable):
    """
    Model for the entire program
    """

    def __init__(self, functions: List[Function]):
        self.functions = functions


class While(Scopeable):
    def __init__(self, scope: Scope, body: List[Compilable], condition: Compilable):
        super(While, self).__init__(scope, body)
        self.condition = condition
