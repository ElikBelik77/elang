from typing import List

from compilation.models.base import Scopeable, Scope, VariableDeclaration, Compilable, Function
from compilation.type_system.base import Type
from compilation.headers import CompileAsPointer


class ElangClass(Scopeable, CompileAsPointer, Type):
    """
    Class model for classes that are defined in a source code.
    """
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
            function.arguments.append(VariableDeclaration("this", self))
        scope.defined_variables["this"] = {"type": self}
        for mv in member_variables:
            scope.defined_variables[mv.name] = {"type": mv.var_type}

    def get_size(self, size_bundle):
        return size_bundle["int"]

    def get_malloc_size(self, size_bundle):
        """
        This function returns the size of this class on the heap.
        :param size_bundle: the size bundle of the compiler.
        :return: the size of this class on heap allocation.
        """
        size = 0
        for member_variable in self.member_variables:
            size += member_variable.var_type.get_size(size_bundle)
        return size
