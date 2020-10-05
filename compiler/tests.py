import re
from factories import *
from compiler.parsing import Parser
from compiler.semantic_check import *

keywords = [{"re": re.compile(r"\s*return\s"), "factory": ReturnFactory()},
            {"re": re.compile(r"\s*int\s"), "factory": IntFactory()},
            {"re": re.compile(r"\s*(\w[\w]*)\s+((\w[\w]*)\s*\((.*)\))\s*"), "factory": FunctionDeclarationFactory(),
             "scopeable": True}]
operators = [{"re": re.compile(r"\s*\+\s*"), "factory": PlusFactory()},
             {"re": re.compile(r"\s*-\s*"), "factory": MinusFactory()},
             {"re": re.compile(r"\s*\*\s*"), "factory": MultFactory()},
             {"re": re.compile(r"\s*/\s*"), "factory": DivFactory()},
             {"re": re.compile(r"\s*=\s*"), "factory": AssignmentFactory()}]
valid_tokens = [{"re": re.compile(r"\s*((\w[\w]*)\s*\((.*)\))\s*"), "factory": FunctionCallFactory()},
                {"re": re.compile(r"\s*([a-zA-Z][\w]*)+"), "factory": VariableFactory()},
                {"re": re.compile(r"\s*[\d]+"), "factory": DecimalConstantFactory()},
                {"re": re.compile(r"\s*\(\s*"), "factory": LeftParenthesisFactory()},
                {"re": re.compile(r"\s*\)\s*"), "factory": RightParenthesisFactory()}]

p = Parser(keywords=keywords, operators=operators, valid_tokens=valid_tokens)
sc = SemanticChecker([FunctionArgumentShadowing(), VariableDeclarationCheck()])
parsed = p.parse_file("tests/simple_return.elang")
print(parsed)
