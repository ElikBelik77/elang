from typing import List

from compilation.models.base import Function, Variable, Scopeable, Scope


class ElangClass(Scopeable):
    def __init__(self, name: str, scope: Scope, functions: List[Function], member_variables: List[Variable]):
        super(ElangClass, self).__init__(scope, functions + member_variables)
        self.name = name
        self.functions = functions
        self.member_variables = member_variables