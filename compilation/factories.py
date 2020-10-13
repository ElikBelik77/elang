from compilation.models.base_classes import *
from compilation.models.values import *
from compilation.models.operators import *
from compilation.models.keywords import *
from compilation.shunting_yard import shunting_yard
from typing import Match, Tuple


class Factory:
    """
    Class that produces models based on parsed tokens.
    """

    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        """
        Produces a model based on a token from the source code, when the model is the first token in the line.
        :param parser: the parser that parsed the token.
        :param source_code: the source code.
        :param parent_scope: the parent scope of the token.
        :param match: the token that was matched.
        :return: list of expressions that were created by the match.
        """
        pass

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        """
        Produces a model for shunting yard purpose, if it not the first token in the line.
        :param parser: the parser that parsed the token.
        :param source_code: the source code.
        :param parent_scope: the parent scope of the token.
        :param match: the token that was matched.
        :return: (expression, source_code) where expression is the produces shallow expression and source_code is the
        original source code without the current match.
        """
        pass


class ReturnFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [Return(shunting_yard(match[1:]))]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return Return(None), source_code[len(match.group(0)):].strip()


class MinusFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the * operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return SubtractOperator(), source_code[1:]


class MultFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the * operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return MultiplicationOperator(), source_code[1:]


class LogicalAndFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the * operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return LogicalAnd(), source_code[match.span()[1]:]


class LogicalOrFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the * operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return LogicalOr(), source_code[match.span()[1]:]


class LogicalGreaterFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the * operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return LogicalGreater(), source_code[match.span()[1]:]


class EqualFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the == operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return Equal(), source_code[match.span()[1]:]


class DivFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid placemenet of the / operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return DivisionOperator(), source_code[1:]


class PlusFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [shunting_yard(match)]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return AdditionOperator(), source_code[1:]


class LeftParenthesisFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return LeftParenthesis(), source_code[1:]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return LeftParenthesis(), source_code[1:]


class RightParenthesisFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid parenthesis placement")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return RightParenthesis(), source_code[1:]


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
        return FunctionCall(match.group(2), arguments), source_code[end:]

    def find_closing_brackets(self, source_code: str) -> int:
        """
        This function find the right parenthesis that closes the current parenthesis.
        :param source_code: the source code
        :return: the index of the ')' that closes the current '('
        """
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
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [shunting_yard(match)]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return DecimalConstantValue(int(match.group(0))), source_code[len(match.group(0)):].strip()


class VariableFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [shunting_yard(match)]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return Variable(match.group(0)), source_code[len(match.group(0)):].strip()


class IntFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        if len(match) < 2:
            raise Exception("Invalid position of the 'int' keyword")
        if len(match) == 2:
            return [VariableDeclaration(match[1].name, "int")]
        return [VariableDeclaration(match[1].name, "int"), shunting_yard(match[1:])]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return VariableDeclaration(None, "int"), source_code[len(match.group(0)):].strip()


class AssignmentFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]) -> Tuple[List, str]:
        raise Exception("Invalid placement of the = operator")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return Assignment(), source_code[len(match.group(0)):].strip()


class WhileFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]) -> Tuple[List, str]:
        source_code = source_code[len(match.group(0).strip()):].strip()
        source_end = find_scope_end(source_code)
        scope = Scope(match.group(0), parent_scope)
        body = [token for token in parser.parse_source_code(source_code[0:source_end], scope)]
        condition = [token for token in parser.parse_source_code(match.group(1), parent_scope)][0]
        if len(condition) > 1:
            raise Exception("Too many expression in an 'while' condition")
        for idx, statement in enumerate(body):
            if isinstance(statement, VariableDeclaration) and statement.name not in scope.defined_variables:
                scope.defined_variables[statement.name] = {"type": statement.var_type, "define_line": idx,
                                                           "scope": scope}
            elif isinstance(statement, VariableDeclaration):
                raise Exception(
                    "Variable {0} is declared more than once in function {1}".format(statement.name, match.group(0)))

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
        for idx, statement in enumerate(body):
            if isinstance(statement, VariableDeclaration) and statement.name not in scope.defined_variables:
                scope.defined_variables[statement.name] = {"type": statement.var_type, "define_line": idx,
                                                           "scope": scope}
            elif isinstance(statement, VariableDeclaration):
                raise Exception(
                    "Variable {0} is declared more than once in function {1}".format(statement.name, match.group(0)))

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
        for idx, statement in enumerate(function_body):
            if isinstance(statement, VariableDeclaration) and statement.name not in scope.defined_variables:
                scope.defined_variables[statement.name] = {"type": statement.var_type, "define_line": idx,
                                                           "scope": scope}
            elif isinstance(statement, VariableDeclaration):
                raise Exception(
                    "Variable {0} is declared more than once in function {1}".format(statement.name, match.group(0)))
        f = Function(scope, function_name, match.group(0).strip().replace('{', ''), match.group(1), function_body,
                     function_arguments)
        return [f], source_code[scope_end + 1:]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid location to declare a function.")


def find_scope_end(source_code: str) -> int:
    """
    This function find where the current scope ends.
    :param source_code: the source code.
    :return: the index of the end of the current scope.
    """
    count, idx = 1, 0
    while count is not 0:
        if source_code[idx] == "{":
            count += 1
        elif source_code[idx] == "}":
            count -= 1
        if count == 0:
            return idx
        idx += 1
