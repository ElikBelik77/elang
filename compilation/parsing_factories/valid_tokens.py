from compilation.parsing_factories.base import *
from compilation.models.values import DecimalConstantValue, FunctionCall
from compilation.parsing_factories.utils import find_closing_parenthesis
from compilation.shunting_yard import shunting_yard


class FunctionCallFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [shunting_yard(match)]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        start, end = find_closing_parenthesis(source_code)
        arguments_list = source_code[start + 1:end - 1].split(',')
        arguments = []
        for arg in arguments_list:
            if len(arg) is not 0:
                arguments += parser.parse_source_code(arg, parent_scope)
        constructor_of = None
        if match.group(2).strip() in parser.parsed_classes:
            constructor_of = parser.parsed_classes[match.group(2).strip()]
        return [FunctionCall(match.group(2).strip(), arguments, constructor_of=constructor_of)], source_code[end:]


class DecimalConstantFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [shunting_yard(match)]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [DecimalConstantValue(int(match.group(0)))], source_code[len(match.group(0)):].strip()


class VariableFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        if len(match) == 1:
            return []
        return [shunting_yard(match)]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [Variable(match.group(0).strip())], source_code[len(match.group(0)):].strip()
