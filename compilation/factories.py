from models import *
from parsing import Parser
from shunting_yard import shunting_yard
from typing import Pattern, Match


class Factory:
    def produce(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        pass


class ReturnFactory(Factory):
    def produce(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return [Return(shunting_yard(match[1:]))]

    def produce_shallow(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return Return(None), source_code[len(match.group(0)):].strip()


class MinusFactory(Factory):
    def produce(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the * operator")

    def produce_shallow(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return Minus(), source_code[1:]


class MultFactory(Factory):
    def produce(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the * operator")

    def produce_shallow(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return Mult(), source_code[1:]


class DivFactory(Factory):
    def produce(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the / operator")

    def produce_shallow(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return Div(), source_code[1:]


class PlusFactory(Factory):
    def produce(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return [shunting_yard(match)]

    def produce_shallow(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return Plus(), source_code[1:]


class LeftParenthesisFactory(Factory):
    def produce(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return LeftParenthesis(), source_code[1:]

    def produce_shallow(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return LeftParenthesis(), source_code[1:]


class RightParenthesisFactory(Factory):
    def produce(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid parenthesis placement")

    def produce_shallow(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return RightParenthesis(), source_code[1:]


class FunctionCallFactory(Factory):
    def produce(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return [match[0]]

    def produce_shallow(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        start, end = self.find_closing_brackets(source_code)
        arguments_list = source_code[start + 1:end - 1].split(',')
        arguments = []
        for arg in arguments_list:
            if len(arg) is not 0:
                arguments += parser.parse_source_code(arg, parent_scope)
        return FunctionCall(match.group(2), arguments), source_code[end:]

    def find_closing_brackets(self, source_code: str):
        count, idx = 1, 0
        start = 0
        first = True
        while count is not 0:
            if source_code[idx] == "(" and first:
                first = False
                start = idx
            elif source_code[idx] == "(" and not first:
                count += 1
            elif source_code[idx] == ")":
                count -= 1
            if count == 0:
                return start, idx + 1
            idx += 1


class DecimalConstantFactory():
    def produce(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return [shunting_yard(match)]

    def produce_shallow(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return DecimalConstantValue(int(match.group(0))), source_code[len(match.group(0)):].strip()


class VariableFactory(Factory):
    def produce(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return [shunting_yard(match)]

    def produce_shallow(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return Variable(match.group(0)), source_code[len(match.group(0)):].strip()


class IntFactory(Factory):
    def produce(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        if len(match) == 2:
            return [VariableDeclaration(match[1].name, "int")]
        return [VariableDeclaration(match[1].name, "int"), shunting_yard(match[1:])]

    def produce_shallow(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return VariableDeclaration(None, "int"), source_code[len(match.group(0)):].strip()


class AssignmentFactory(Factory):
    def produce(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placement of the = operator")

    def produce_shallow(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        return Assignment(), source_code[len(match.group(0)):].strip()


class FunctionDeclarationFactory():
    def produce(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        source_code = source_code[len(match.group(0).strip()):].strip()
        scope_end = self.find_scope_end(source_code)
        scope = Scope(match, parent_scope)
        function_name = match.group(3)
        function_source = source_code[1:scope_end].strip()
        function_body = [token for token in parser.parse_source_code(function_source, scope)]
        function_arguments = [VariableDeclaration(name=arg.strip().split(' ')[1], type=arg.strip().split(' ')[0]) for
                              arg in match.group(4).split(',') if arg is not '']
        for idx, statement in enumerate(function_body):
            if isinstance(statement, VariableDeclaration) and statement.name not in scope.defined_variables:
                scope.defined_variables[statement.name] = {"type": statement.type, "define_line": idx, "scope": scope}
            elif isinstance(statement, VariableDeclaration):
                raise Exception(
                    "Variable {0} is declared more than once in function {1}".format(statement.name, match.group(0)))
        f = Function(scope, function_name, match.group(0).strip(), match.group(1), function_body, function_arguments)
        return [f], source_code[scope_end + 1:]

    def find_scope_end(self, source_code: str):
        count, idx = 1, 0
        while count is not 0:
            idx += 1
            if source_code[idx] == "{":
                count += 1
            elif source_code[idx] == "}":
                count -= 1
            if count == 0:
                return idx

    def produce_shallow(self, parser: Parser, source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid location to declare a function.")
