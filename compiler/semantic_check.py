from models import *


class Checker:
    def check(self, function: Function):
        pass


class FunctionArgumentShadowing:
    def check(self, function: Function):
        for variable in function.get_mentions():
            if variable in [v.name for v in function.arguments]:
                raise Exception("Function argument {0} is being shadowed by a variable".format(variable))


class VariableDeclarationCheck:
    def check(self, function: Function):
        for statement in function.body:
            if isinstance(statement, VariableDeclaration):
                continue
            for variable_mention in statement.get_mentions():
                if not function.scope.search_variable(variable_mention):
                    raise Exception(
                        "Undefined varialbe {0}, in function {1}".format(variable_mention, function.name))


class SemanticChecker:
    def __init__(self, checklist: [Checker]):
        self.checklist = checklist

    def check_function(self, function: Function):
        for checker in self.checklist:
            checker.check(function)
