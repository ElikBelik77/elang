from models import *
from collections import Counter


class Checker:
    def check(self, function: Function):
        pass


class FunctionArgumentShadowing(Checker):
    def check(self, function: Function):
        for variable in function.get_mentions():
            if variable in [v.name for v in function.arguments]:
                raise Exception("Function argument {0} is being shadowed by a variable".format(variable))


class RepeatingArgumentDeclaration(Checker):
    def check(self, function: Function):
        counter = Counter([argument.name for argument in function.arguments])
        if len(function.arguments) is not 0 and counter.most_common(1)[0][1] > 1:
            raise Exception("Function argument is declared twice")


class RepeatingVariableDeclaration(Checker):
    def check(self, function: Function):
        all_scopes = [function.scope] + function.scope.get_childrens()
        vars_declared = []
        for scope in all_scopes:
            for key in scope.defined_variables.keys():
                if key in vars_declared:
                    raise Exception(
                        "Variable {0} declared more than once in function {1}".format(key["name"], function.signature))
                else:
                    vars_declared.append(key)


class VariableDeclarationCheck(Checker):
    def check(self, function: Function):
        for idx, statement in enumerate(function.body):
            if isinstance(statement, VariableDeclaration):
                continue
            for variable_mention in statement.get_mentions():
                if variable_mention in [v.name for v in function.arguments]:
                    continue
                var_entry = function.scope.search_variable(variable_mention)
                if var_entry is None or (var_entry["scope"] == function.scope and var_entry["define_line"] > idx) or (
                        var_entry["scope"] != function.scope and var_entry["scope"].is_child_of(function.scope)):
                    raise Exception(
                        "Undefined variable {0}, in function {1}".format(variable_mention, function.signature))


class SemanticChecker(Checker):
    def __init__(self, checklist: [Checker]):
        self.checklist = checklist

    def check(self, program: Program):
        for checker in self.checklist:
            for function in program.functions:
                checker.check(function)

    def add_all(self):
        self.checklist += [VariableDeclarationCheck(), RepeatingArgumentDeclaration(), RepeatingVariableDeclaration(),
                           FunctionArgumentShadowing()]
        return self