from typing import Dict

from models import *


class Compiler:
    def compile(self, program: Program):
        for function in program.functions:
            offset_table = self.produce_offset_table(function)
        pass

    def produce_offset_table(self, scopeable: Scopeable):
        scope_table = {}
        scope_table[scopeable]: Dict[str, int] = {}

        if isinstance(scopeable, Function) and len(scopeable.arguments) > 6:
            for idx, arg in enumerate(scopeable.arguments[7:]):
                scope_table[scopeable][arg.name] = 24 + idx * 8
        scopes: List[Scopeable] = [scopeable]
        while len(scopes) is not 0:
            current_scope = scopes.pop()
            if current_scope not in scope_table:
                scope_table[current_scope]: Dict[str, int] = {}
            for idx, key in enumerate(current_scope.scope.defined_variables):
                scope_table[current_scope][key] = -8 * (idx + 1)
            for compilable in current_scope.body:
                if issubclass(type(compilable), Scopeable):
                    scopes.append(compilable)
        return scope_table
