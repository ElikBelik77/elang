from compilation.models import *
from collections import Counter


class FunctionChecker:
    """
    Interface defining methods of a semantic function checker.
    """

    def check(self, function: Function):
        """
        This function checks a parsed function for a certain semantic criteria.
        Throws exception if the function doesn't pass the check.
        :param function: the function to check.
        :return: None.
        """
        pass


class GlobalChecker:
    """
    Interface defining methods of a semantic global/program checker.
    """

    def check(self, program: Program):
        """
        This function checks a parsed program for a certain semantic criteria.
        Throws exception if the program doesn't pass the check.
        :param program: the program to check.
        :return: None
        """
        pass


class HasEntryPoint(GlobalChecker):
    """
    This semantic check ensures the program has an entry point names 'main'
    """

    def check(self, program: Program) -> None:
        has_entry = False
        for function in program.functions:
            if function.name == "main":
                has_entry = True
        if not has_entry:
            raise Exception("No entry point for the program.")


class FunctionArgumentShadowing(FunctionChecker):
    """
    This semantic check ensures that function arguments are not being shadowed by local defined variables.
    """

    def check(self, function: Function) -> None:
        for variable in function.get_mentions():
            if variable in [v.name for v in function.arguments]:
                raise Exception("Function argument {0} is being shadowed by a variable".format(variable))


class RepeatingArgumentDeclaration(FunctionChecker):
    """
    This semantic check ensures that a function argument is not appearing twice.
    """

    def check(self, function: Function) -> None:
        counter = Counter([argument.name for argument in function.arguments])
        if len(function.arguments) is not 0 and counter.most_common(1)[0][1] > 1:
            raise Exception("Function argument is declared twice")


class RepeatingVariableDeclaration(FunctionChecker):
    """
    This semantic check ensures that there are no variables that are declared twice.
    """

    def check(self, function: Function) -> None:
        all_scopes = [function.scope] + function.scope.get_children()
        vars_declared = []
        for scope in all_scopes:
            for key in scope.defined_variables.keys():
                if key in vars_declared:
                    raise Exception(
                        "Variable {0} declared more than once in function {1}".format(key["name"], function.signature))
                else:
                    vars_declared.append(key)


class VariableDeclarationCheck(FunctionChecker):
    """
    This semantic check ensures that variables are declared before they are used.
    """

    def check(self, function: Function) -> None:
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


class SemanticChecker:
    """
    Class that checks an entire program and it's function based on the requested semantic checks.
    """

    def __init__(self, function_checklist: List[FunctionChecker] = [], global_checklist: List[GlobalChecker] = []):
        self.function_checklist = function_checklist
        self.global_checklist = global_checklist

    def check(self, program: Program) -> None:
        """
        This funcion applies each of the semantic checks to the program.
        :param program: the program to check.
        :return: None
        """
        for checker in self.function_checklist:
            for function in program.functions:
                checker.check(function)
        for checker in self.global_checklist:
            checker.check(program)

    @staticmethod
    def create_default() -> "SemanticChecker":
        """
        This function creates a default semantic checker. It has all of the default semantic checks.
        :return: a semantic checker.
        """
        return SemanticChecker([VariableDeclarationCheck(), RepeatingArgumentDeclaration(),
                                RepeatingVariableDeclaration(),
                                FunctionArgumentShadowing()],
                               [HasEntryPoint()]
                               )
