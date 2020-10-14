from compilation.parsing_factories.base import *
from compilation.parsing_factories.utils import *
from compilation.models.keywords import *
from compilation.shunting_yard import shunting_yard
from typing import Match, Tuple



class ReturnFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [Return(shunting_yard(match[1:]))]


def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
    return [Return(None)], source_code[len(match.group(0)):].strip()


class PrimitiveFactory(Factory):
    def __init__(self, primitive: "Primitive"):
        self.type = primitive

    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        if len(match) < 2:
            raise Exception("Invalid position of the '{0}' type".format(self.type.name))
        if len(match) == 2:
            return [VariableDeclaration(self.type, self.type.name)]
        return [VariableDeclaration(self.type, self.type.name), shunting_yard(match[1:])]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [VariableDeclaration(self.type, self.type.name)], source_code[len(match.group(0)):].strip()


class WhileFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]) -> Tuple[List, str]:
        source_code = source_code[len(match.group(0).strip()):].strip()
        source_end = find_scope_end(source_code)
        scope = Scope(match.group(0), parent_scope)
        body = [token for token in parser.parse_source_code(source_code[0:source_end], scope)]
        condition = [token for token in parser.parse_source_code(match.group(1), parent_scope)][0]
        if len(condition) > 1:
            raise Exception("Too many expression in an 'while' condition")
        populate_scope(scope, body, match)
        return [While(scope, body, condition)], source_code[source_end + 1:]


class IfFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]) -> Tuple[List, str]:
        source_code = source_code[len(match.group(0).strip()):].strip()
        source_end = find_scope_end(source_code)
        scope = Scope(match.group(0), parent_scope)
        body = [token for token in parser.parse_source_code(source_code[0:source_end], scope)]
        condition = [token for token in parser.parse_source_code(match.group(1), parent_scope)]
        if len(condition) > 1:
            raise Exception("Too many expressions in an 'if' condition")
        condition = condition[0]
        populate_scope(scope, body, match)

        return [If(scope, body, condition)], source_code[source_end + 1:]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid 'if' statement.")


class FunctionDeclarationFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]) -> Tuple[List, str]:
        source_code = source_code[len(match.group(0).strip()):].strip()
        scope_end = find_scope_end(source_code)
        scope = Scope(match.group(0), parent_scope)
        function_name = match.group(3)
        function_source = source_code[0:scope_end].strip()
        function_body = [token for token in parser.parse_source_code(function_source, scope)]
        function_arguments = [VariableDeclaration(name=arg.strip().split(' ')[1], var_type=arg.strip().split(' ')[0])
                              for
                              arg in match.group(4).split(',') if arg is not '']
        populate_scope(scope, function_body, match)
        f = Function(scope, function_name, match.group(0).strip().replace('{', ''), match.group(1), function_body,
                     function_arguments)
        return [f], source_code[scope_end + 1:]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid location to declare a function.")
