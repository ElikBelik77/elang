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


class UnaryOperator:
    def get_precedence(self):
        pass


class BinaryOperator:
    """
    Interface for unifying operators.
    """

    def get_precedence(self):
        pass


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


class VariableDeclaration(Compilable):
    """
    Model for variable declaration
    """

    def __init__(self, name: str, var_type: str):
        self.name = name
        self.var_type = var_type

    def get_mentions(self) -> List[str]:
        return [self.name]


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

    def __init__(self, functions: List["Function"]):
        self.functions = functions
