import re

from compilation.parsing_factories.base import *
from compilation.parsing_factories.utils import *
from compilation.models.keywords import *
from compilation.shunting_yard import shunting_yard
from compilation.models.arrays import ArrayInitializer, Array, HeapLayer, StackLayer
from typing import Match, Tuple
import os
from compilation.models.values import FunctionCall


class IncludeFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        source_code = source_code[len(match.group(0).strip()):].strip()
        source_end = find_scope_end(source_code)
        tokens = [token.strip() for token in source_code[:source_end].split(',')]
        includes = [Include(token) for token in tokens]
        var_declarations = []
        for include in includes:
            dirname = os.path.dirname(parser.path)
            filename = os.path.join(dirname, include.file_name)
            include.program = parser.parse_file(filename)
            # TODO: change primitive constructor to reference to parser type
            var_declarations.append(VariableDeclaration(include.module_name, include.program))
        return includes + var_declarations, source_code[source_end + 1:]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid include statement.")


class ExportFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        source_code = source_code[len(match.group(0).strip()):].strip()
        source_end = find_scope_end(source_code)
        tokens = [token.strip() for token in source_code[:source_end].split(',')]
        return [Export(token) for token in tokens], source_code[source_end + 1:]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid export statement.")


class ConstructorFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid position for the constructor function")

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        start, end = find_closing_parenthesis(source_code)
        arguments_list = source_code[start + 1:end - 1].split(',')
        arguments = []
        for arg in arguments_list:
            if len(arg) is not 0:
                arguments += parser.parse_source_code(arg, parent_scope)
        constructor_of = None
        if match.group(1).strip() in parser.parsed_classes:
            constructor_of = parser.parsed_classes[match.group(1).strip()]
        return [FunctionCall(match.group(1), arguments, constructor_of=constructor_of)], source_code[end:]


class ReturnFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [Return(shunting_yard(match[1:]))]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        return [Return(None)], source_code[len(match.group(0)):].strip()


class ElangClassDeclarationFactory(Factory):
    def __init__(self):
        self.subclass_depth = 0
        self.subclass_prefix = []

    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        source_code = source_code[len(match.group(0).strip()):].strip()
        source_end = find_scope_end(source_code)
        scope = Scope(match.group(1), parent_scope)
        body, member_variables, member_variables_initialization, functions, sub_classes = [], [], [], [], []
        self.subclass_depth += 1
        self.subclass_prefix.append(match.group(1).strip())
        for token in parser.parse_source_code(source_code[0:source_end], scope):
            if isinstance(token, ElangClass):
                token.name = ".".join(self.subclass_prefix) + f"{token.name}"
                parser.keywords.append(
                    {"re": re.compile(rf"\s*{token.name.strip()}(\s+|\[)"),
                     "factory": TypeFactory(token)})
                parser.keywords.append(
                    {"re": re.compile(rf"\s*({token.name.strip()})\s*\((.*)\)\s*"),
                     "factory": ConstructorFactory()})
                parser.keywords.append(
                    {"re": re.compile(rf"\s*{parser.prog_name}.{token.name.strip()}(\s+|\[)"),
                     "factory": TypeFactory(token)})
                parser.keywords.append(
                    {"re": re.compile(rf"\s*({parser.prog_name}.{token.name.strip()})\s*\((.*)\)\s*"),
                     "factory": ConstructorFactory()})
                sub_classes.append(token)
                parser.parsed_classes[token.name] = token
                parser.parsed_classes[parser.prog_name + '.' + token.name] = token
        member_variables = [token for token in parser.parse_source_code(source_code[0:source_end], scope) if
                            isinstance(token, VariableDeclaration)]

        member_variables_initialization = [token for token in parser.parse_source_code(source_code[0:source_end], scope)
                                           if not isinstance(token, VariableDeclaration)
                                           and not isinstance(token, Function) and not isinstance(token, ElangClass)]

        functions = [token for token in parser.parse_source_code(source_code[0:source_end], scope) if
                     isinstance(token, Function)]
        elang_class = ElangClass(match.group(1), scope, functions, member_variables,
                                 member_variables_initialization, sub_classes)
        if self.subclass_depth == 1:
            parser.keywords.append(
                {"re": re.compile(rf"\s*{match.group(1).strip()}(\s+|\[)"), "factory": TypeFactory(elang_class)})
            parser.keywords.append(
                {"re": re.compile(rf"\s*({match.group(1).strip()})\s*\((.*)\)\s*"),
                 "factory": ConstructorFactory()})
            parser.keywords.append(
                {"re": re.compile(rf"\s*{parser.prog_name}.{match.group(1).strip()}(\s+|\[)"),
                 "factory": TypeFactory(elang_class)})
            parser.keywords.append(
                {"re": re.compile(rf"\s*({parser.prog_name}.{match.group(1).strip()})\s*\((.*)\)\s*"),
                 "factory": ConstructorFactory()})
            parser.parsed_classes[elang_class.name] = elang_class
            parser.parsed_classes[parser.prog_name + '.' + elang_class.name] = elang_class
        self.subclass_depth -= 1
        self.subclass_prefix = self.subclass_prefix[:-1]

        parser.defined_types.append(elang_class)
        return [elang_class], source_code[source_end + 1:]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid location to declare a class.")


class TypeFactory(Factory):
    def __init__(self, type):
        self.type = type
        self.array_re_lookahead = re.compile(r"(s*\[(.*)]\s*)+")

    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        if len(match) < 2:
            raise Exception("Invalid position of the '{0}' type".format(self.type.name))
        if len(match) == 2:
            if isinstance(match[0].var_type, Array):
                return [VariableDeclaration(match[1].name, match[0].var_type),
                        ArrayInitializer(match[0].var_type, match[1].name)]
            else:
                return [VariableDeclaration(match[1].name, match[0].var_type)]

        if isinstance(match[0].var_type, Array):
            return [VariableDeclaration(match[1].name, match[0].var_type),
                    ArrayInitializer(match[0].var_type, match[1].name), shunting_yard(match[1:])]
        return [VariableDeclaration(match[1].name, match[0].var_type), shunting_yard(match[1:])]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        lookahead_match = self.array_re_lookahead.match(source_code[len(match.group(0)) - 1:])
        if lookahead_match is None:
            return [VariableDeclaration(None, self.type)], source_code[len(match.group(0)):].strip()
        last_stack_layer = 0
        stack_settled = False
        layers = []
        brackets_end = 0
        for idx, brackets in enumerate(find_bracket_pairs(lookahead_match.group(0))):
            brackets_start, brackets_end = brackets
            if brackets_start == brackets_end - 1 and not stack_settled:
                last_stack_layer = idx - 1
                stack_settled = True
            if brackets_start == brackets_end - 1 and stack_settled:
                raise Exception(
                    "Cannot use stack dimension declaration after defining array dimension {0} to be heap based.".format(
                        last_stack_layer + 1))
            if brackets_start != brackets_end - 1:
                layers.append(StackLayer(shunting_yard(
                    [token for token in
                     parser.parse_source_code(lookahead_match.group(0)[brackets_start + 1:brackets_end],
                                              parent_scope)])))
            else:
                layers.append(HeapLayer())
        return [VariableDeclaration(None, Array(self.type, layers))], source_code[len(match.group(0)) + brackets_end:]


class WhileFactory(Factory):
    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]) -> Tuple[List, str]:
        source_code = source_code[len(match.group(0).strip()):].strip()
        source_end = find_scope_end(source_code)
        scope = Scope(match.group(0), parent_scope)
        body = [token for token in parser.parse_source_code(source_code[0:source_end], scope)]
        condition = [token for token in parser.parse_source_code(match.group(1), parent_scope)][0]
        if len(condition) > 1:
            raise Exception("Too many expression in an 'while' condition")
        populate_scope(scope, body)
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
        populate_scope(scope, body)

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
        populate_scope(scope, function_body)
        f = Function(scope, function_name, match.group(0).strip().replace('{', ''),
                     parser.resolve_type(match.group(1).strip()), function_body,
                     function_arguments)
        return [f], source_code[scope_end + 1:]

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        raise Exception("Invalid location to declare a function.")
