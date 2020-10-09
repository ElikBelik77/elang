from typing import Dict
import fstrings
from models import *

function_base_64bit = """
{name}:
pushq rbp
movq rbp, rsp
{body}
movq rsp, rbp
popq rbp
ret
"""


class Compiler:
    def compile(self, program: Program, destination_file: str):
        assembly = ""
        for function in program.functions:
            offset_table = self.produce_offset_table(function)
            assembly += self.compile_function(function, offset_table)

        with open(destination_file, "w") as out:
            out.write(assembly)

    def compile_function(self, function, offset_table):

        assembly = function_base_64bit.format(name=function.name, body=body_assembly)
        return assembly

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
