from compilation.parsing_factories.base import *
from compilation.models.operators import *
from compilation.shunting_yard import shunting_yard
from typing import Match, Tuple

from parsing_factories.utils import find_closing_brackets


class AssignmentFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]) -> Tuple[List, str]:
        raise Exception("Invalid placement of the = operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [Assignment()], source_code[len(match.group(0)):].strip()


class SubtractionFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the * operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [SubtractOperator()], source_code[1:]


class MultiplicationFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the * operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [MultiplicationOperator()], source_code[1:]


class LogicalAndFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the * operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [LogicalAnd()], source_code[match.span()[1]:]


class LogicalOrFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the * operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [LogicalOr()], source_code[match.span()[1]:]


class LogicalGreaterFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the * operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [LogicalGreater()], source_code[match.span()[1]:]


class EqualFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the == operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [Equal()], source_code[match.span()[1]:]


class DivisionFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the / operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [DivisionOperator()], source_code[1:]


class AdditionFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [shunting_yard(match)]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [AdditionOperator()], source_code[1:]


class LeftParenthesisFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [LeftParenthesis()], source_code[1:]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [LeftParenthesis()], source_code[1:]


class RightParenthesisFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid parenthesis placement")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [RightParenthesis()], source_code[1:]


class ArrayIndexerFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid position for the array indexer opeartor")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        bracket_start, bracket_end = find_closing_brackets(source_code)
        index_expression = shunting_yard(
            [token for token in parser.parse_source_code(source_code[bracket_start:bracket_end])])
        return [ArrayIndexer(), index_expression], source_code[bracket_end + 1:]
