import regex
import re
from collections import deque
from compiler_models import *


class Parser:
    def __init__(self):
        self.operators = r"\s*([\+\-\/\:\*\&\!\=\^]|\*\*)+"
        self.name = r"\s*([a-zA-Z][\w]*)+"
        self.constants = r"\s*[\d]+"
        self.math_expression = r"(({operator})?({name})+)+".format(operator=self.operators, name=self.name)
        self.math_re = re.compile(self.math_expression)
        self.arguments_re = r"\s*((\s*{math}\s*,\s*)|{math}\s*)\s*".format(math=self.math_expression)
        self.function_call_re = re.compile(
            r"\s*((\w[\w]*)\s*\((.*)\))\s*")
        self.names_re = re.compile(self.name)
        self.operators_re = re.compile(self.operators)
        self.constants_re = re.compile(self.constants)

    def try_parse(self, line):
        match = self.function_call_re.match(line)
        if match is not None:
            function_name, arguments, end_index = self.parse_function(match, line)
            return FunctionMatch(function_name, arguments), line[end_index:]
        match = self.names_re.match(line)
        if match is not None:
            return NameMatch(line[match.span()[0]:match.span()[1]]), line[match.span()[1]:]
        match = self.operators_re.match(line)
        if match is not None:
            return OperatorMatch(line[match.span()[0]:match.span()[1]]), line[match.span()[1]:]
        match = self.constants_re.match(line)
        if match is not None:
            return ConstantMatch(line[match.span()[0]:match.span()[1]]), line[match.span()[1]:]
        return None, ""

    def delimit_scopes(self, file):
        scope_stack = [Scope('global', None, 0, len(file))]

        for index, char in enumerate(file):
            if char == "{":
                scope_stack.append(Scope('', scope_stack[-1], index))
            if char == "}":
                scope = scope_stack.pop()
                scope.end_pos = index
                yield scope
        yield scope_stack.pop()

    def extract_tokens(self, line):
        while len(line) is not 0:
            try:
                token, line = self.try_parse(line)
                print(token)
            except:
                break

    def parse_function(self, func, line):
        print("> checking", func)
        arguments_ptr = func[3]
        end_index = func.span()[1]
        func_name = func[2]
        func_args = []
        if not self.parenthesis_balance(arguments_ptr):
            raise Exception("Parenthesis are not balanced")
        arg_candidate = self.math_re.search(arguments_ptr)
        func_arg_candidate = self.function_call_re.search(arguments_ptr)
        count = 0
        while arg_candidate is not None or func_arg_candidate is not None:
            if arg_candidate is not None:
                if self.math_re.search(arg_candidate.group(0)) is None:
                    raise Exception("Invalid function parameter at position #{0}".format(count))
                arguments_ptr = arguments_ptr[arg_candidate.span(0)[1] + 1:]
                func_args.append(ArgumentMatch(arguments_ptr[arg_candidate.span(0)[0]:arg_candidate.span(0)[1]]))
                print("correctly parsed", arg_candidate)
            if func_arg_candidate is not None:
                inner_func_name, inner_func_args, _ = self.parse_function(func_arg_candidate, line)
                func_args.append(FunctionMatch(inner_func_name, inner_func_args))
                arguments_ptr = arguments_ptr[func_arg_candidate.span(0)[1] + 1:]

                print("correctly parsed", func_arg_candidate)
            count += 1
            arg_candidate = self.math_re.search(arguments_ptr)
            func_arg_candidate = self.function_call_re.search(arguments_ptr)
        return func_name, func_args, end_index

    def parenthesis_balance(self, string):
        count = 0
        for char in string:
            if char is "(":
                count += 1
            if char is ")" and count is 0:
                return False
            if char is ")":
                count -= 1
        return True if count == 0 else False

    def get_file_tokens(self, file):
        with open(file, 'r') as fs:
            for line in fs:
                tokens = self.extract_tokens(line)

    def resolve_scope_name(self, scope, file):

        pass

    def parse(self, file):
        with open(file, 'r') as fs:
            file = fs.read()
            scopes = self.delimit_scopes(file)
            self.resolve_scope_name([scope for scope in scopes if scope.parent_scope.name == "global"], file)
