from models import VariableDeclaration, Variable


class VariableDeclarationCheck:
    def check(self, function):
        for statement in function.body:
            if isinstance(statement, VariableDeclaration):
                continue
            for variable_mention in statement.get_mentions():
                if not function.scope.search_variable(variable_mention):
                    raise Exception(
                        "Undefined varialbe {0}, in function {1}".format(variable_mention, function.name))


class SemanticChecker:
    def __init__(self, checklist):
        self.checklist = checklist

    def check_function(self, function):
        for checker in self.checklist:
            checker.check(function)