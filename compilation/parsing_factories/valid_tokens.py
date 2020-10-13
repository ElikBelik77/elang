from compilation.parsing_factories.base import *
from compilation.models.values import DecimalConstantValue, FunctionCall, Variable
from shunting_yard import shunting_yard


class FunctionCallFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [match[0]]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        start, end = self.find_closing_brackets(source_code)
        arguments_list = source_code[start + 1:end - 1].split(',')
        arguments = []
        for arg in arguments_list:
            if len(arg) is not 0:
                arguments += parser.parse_source_code(arg, parent_scope)
        return [FunctionCall(match.group(2), arguments)], source_code[end:]


class DecimalConstantFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [shunting_yard(match)]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [DecimalConstantValue(int(match.group(0)))], source_code[len(match.group(0)):].strip()


class VariableFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [shunting_yard(match)]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [Variable(match.group(0))], source_code[len(match.group(0)):].strip()
