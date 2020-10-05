from models import *
from shunting_yard import shunting_yard


class Factory:
    def produce(self, parser, source_code, parent_scope, match):
        pass


class ReturnFactory(Factory):
    def produce(self, parser, source_code, parent_scope, match):
        return [Return(shunting_yard(match[1:]))]

    def produce_shallow(self, parser, source_code, parent_scope, match):
        return Return(None), source_code[len(match.group(0)):].strip()


class MinusFactory(Factory):
    def produce(self, parser, source_code, parent_scope, match):
        pass

    def produce_shallow(self, parser, source_code, parent_scope, match):
        return Minus(), source_code[1:]


class MultFactory(Factory):
    def produce(self, parser, source_code, parent_scope, match):
        pass

    def produce_shallow(self, parser, source_code, parent_scope, match):
        return Mult(), source_code[1:]


class DivFactory(Factory):
    def produce(self, parser, source_code, parent_scope, match):
        pass

    def produce_shallow(self, parser, source_code, parent_scope, match):
        return Div(), source_code[1:]


class PlusFactory(Factory):
    def produce(self, parser, source_code, parent_scope, match):
        pass

    def produce_shallow(self, parser, source_code, parent_scope, match):
        return Plus(), source_code[1:]


class LeftParenthesisFactory(Factory):
    def produce(self, parser, source_code, parent_scope, match):
        pass

    def produce_shallow(self, parser, source_code, parent_scope, match):
        return LeftParenthesis(), source_code[1:]


class RightParenthesisFactory(Factory):
    def produce(self, parser, source_code, parent_scope, match):
        pass

    def produce_shallow(self, parser, source_code, parent_scope, match):
        return RightParenthesis(), source_code[1:]


class DefaultFactory(Factory):
    def produce(self, parser, source_code, parent_scope, match):
        pass


class FunctionCallFactory(Factory):
    def produce(self, parser, source_code, parent_scope, match):
        pass

    def produce_shallow(self, parser, source_code, parent_scope, match):
        end = self.find_closing_brackets(source_code)
        return FunctionCall(match.group(1), None), source_code[end:]

    def find_closing_brackets(self, source_code):
        count, idx = 1, 0
        first = True
        while count is not 0:
            if source_code[idx] == "(" and first:
                first = False
            elif source_code[idx] == "(" and not first:
                count += 1
            elif source_code[idx] == ")":
                count -= 1
            if count == 0:
                return idx+1
            idx += 1


class DecimalConstantFactory():
    def produce(self, parser, source_code, parent_scope, match):
        pass

    def produce_shallow(self, parser, source_code, parent_scope, match):
        return DecimalConstantValue(int(match.group(0))), source_code[len(match.group(0)):].strip()


class VariableFactory(Factory):
    def produce(self, parser, source_code, parent_scope, match):
        return [shunting_yard(match)]

    def produce_shallow(self, parser, source_code, parent_scope, match):
        return Variable(match.group(0)), source_code[len(match.group(0)):].strip()


class IntFactory(Factory):
    def produce(self, parser, source_code, parent_scope, match):
        if len(match) == 2:
            return [VariableDeclaration(match[1], "int")]
        return [VariableDeclaration(match[1], "int"), shunting_yard(match[1:])]

    def produce_shallow(self, parser, source_code, parent_scope, match):
        return VariableDeclaration(None, "int"), source_code[len(match.group(0)):].strip()


class AssignmentFactory(Factory):
    def produce(self, parser, source_code, parent_scope, match):
        pass

    def produce_shallow(self, parser, source_code, parent_scope, match):
        return Assignment(), source_code[len(match.group(0)):].strip()


class FunctionDeclarationFactory():
    def produce(self, parser, source_code, parent_scope, match):
        source_code = source_code[len(match.group(0).strip()):].strip()
        scope_end = self.find_scope_end(source_code)
        scope = Scope(match, parent_scope)
        function_source = source_code[1:scope_end].strip()
        function_body = [token for token in parser.parse_source_code(function_source, scope)]
        f = Function(scope, match, match.group(1), function_body)
        return [f], source_code[scope_end + 1:]

    def find_scope_end(self, source_code):
        count, idx = 1, 0
        while count is not 0:
            idx += 1
            if source_code[idx] == "{":
                count += 1
            elif source_code[idx] == "}":
                count -= 1
            if count == 0:
                return idx
