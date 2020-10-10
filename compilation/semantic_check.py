from compilation.models import *
from collections import Counter


class FunctionChecker:
    def check(self, function: Function):
        pass

class GlobalChecker:
    def check(self, program: Program):
        pass

class HasEntryPoint(GlobalChecker):
    def check(self,  program: Program):
        has_entry = False
        for function in program.functions:
            if function.name is "main":
                has_entry = True
        if not has_entry:
            raise Exception("No entry point for the program.")



class FunctionArgumentShadowing(FunctionChecker):
    def check(self, function: Function):
        for variable in function.get_mentions():
            if variable in [v.name for v in function.arguments]:
                raise Exception("Function argument {0} is being shadowed by a variable".format(variable))


class RepeatingArgumentDeclaration(FunctionChecker):
    def check(self, function: Function):
        counter = Counter([argument.name for argument in function.arguments])
        if len(function.arguments) is not 0 and counter.most_common(1)[0][1] > 1:
            raise Exception("Function argument is declared twice")


class RepeatingVariableDeclaration(FunctionChecker):
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


class VariableDeclarationCheck(FunctionChecker):
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


class SemanticChecker():
    def __init__(self, function_checklist: [FunctionChecker] = [], ):
        self.function_checklist = function_checklist

    def check(self, program: Program):
        for checker in self.function_checklist:
            for function in program.functions:
                checker.check(program, function)

    def add_all(self):
        self.function_checklist += [VariableDeclarationCheck(), RepeatingArgumentDeclaration(),
                                    RepeatingVariableDeclaration(),
                                    FunctionArgumentShadowing()]
        self.global_checklist += [HasEntryPoint()]
        return self
