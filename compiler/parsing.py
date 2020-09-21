import regex
import re


class Parser:
    def __init__(self):
        self.operators = r"([\+\-\/\:\*\&\!\=\^]|\*\*)+"
        self.name = r"([a-zA-Z][\w]*)+"
        self.constants = r"[\d]+"
        self.math_expression = r"(({operator})?({name})+)+".format(operator=self.operators, name=self.name)
        self.math_re = re.compile(self.math_expression)
        self.arguments_re = r"\s*((\s*{math}\s*,\s*)|{math}\s*)\s*".format(math=self.math_expression)
        self.function_re = re.compile(
            r"(\w[\w]*\s*\((.*)\))\s*")
        self.names_re = re.compile(self.name)
        self.operators_re = re.compile(self.operators)
        self.constants_re = re.compile(self.constants)

    def extract_tokens(self, line):
        print("\n")
        print(line)
        print("functions", self.function_re.findall(line))
        for func in self.function_re.findall(line):
            print("check is :", self.check_function(func))
        print("names:", self.names_re.findall(line))
        print("operators:", self.operators_re.findall(line))
        print("constants:", self.constants_re.findall(line))
        pass

    def check_function(self, func):
        print("> checking", func)
        arguments = func[1]
        if not self.parenthesis_balance(arguments):
            raise Exception("Parenthesis are not balanced")
        arg = self.math_re.search(arguments)
        func_arg = self.function_re.search(arguments)
        count = 0
        while arg is not None or func_arg is not None:
            if arg is not None:
                if self.math_re.search(arg.group(0)) is None:
                    raise Exception("Invalid function parameter at position #{0}".format(count))
                arguments = arguments[arg.span(0)[1]+1:]
            if func_arg is not None:
                if not self.check_function(func_arg.group(0)):
                    raise Exception("Invalid function parameter at position #{0}".format(count))
                arguments = arguments[func_arg.span(0)[1]+1:]
            count += 1
            arg = self.math_re.search(arguments)
            func_arg = self.function_re.search(arguments)
        return True



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

    def parse(self, file):
        with open(file, 'r') as fs:
            for line in fs:
                tokens = self.extract_tokens(line)
