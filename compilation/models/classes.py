from typing import List

from compilation.models.base import Scopeable, Scope, VariableDeclaration, Compilable, Function
from compilation.type_system.base import Type
from compilation.headers import CompileAsPointer


class ElangClass(Scopeable, CompileAsPointer):
    def __init__(self, name: str, scope: Scope, functions: List[Function], member_variables: List[VariableDeclaration],
                 member_variable_initialization: List[Compilable]):
        super(ElangClass, self).__init__(scope, functions + member_variables)
        self.name = name
        self.functions = functions
        self.constructor = None
        self.member_variables = member_variables
        self.member_variable_initialization = member_variable_initialization
        for function in self.functions:
            if function.name == "constructor":
                self.constructor = function
            function.arguments.insert(0, VariableDeclaration("this", self))

    def get_size(self, size_bundle):
        return size_bundle["int"]

    def get_malloc_size(self, size_bundle):
        size = 0
        for member_variable in self.member_variables:
            size += member_variable.var_type.get_size(size_bundle)
        return size
