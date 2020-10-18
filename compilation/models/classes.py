from typing import List

from compilation.models.base import Scopeable, Scope, VariableDeclaration, Compilable, Function


class ElangClass(Scopeable):
    def __init__(self, name: str, scope: Scope, functions: List[Function], member_variables: List[VariableDeclaration],
                 member_variable_initialization: List[Compilable]):
        super(ElangClass, self).__init__(scope, functions + member_variables)
        self.name = name
        self.functions = functions
        self.member_variables = member_variables
        self.member_variable_initialization = member_variable_initialization
        for function in self.functions:
            function.arguments.insert(0, VariableDeclaration("this", "int"))

    def get_size(self, size_bundle):
        size = 0
        for member_variable in self.member_variables:
            size += size_bundle[member_variable.var_type]
        size += len(self.functions) * size_bundle["int"]
        return size
