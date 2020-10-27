import re
from typing import *

from compilation.parsing_factories.keywords import *
from compilation.parsing_factories.operators import *
from compilation.parsing_factories.valid_tokens import *
from compilation.type_system.primitives import PrimitiveSyntax, get_default_primitives


class Parser:
    """
    Class responsible for parsing a source file into tokens and expressions.
    """

    @staticmethod
    def create_default():
        """
        This function creates the default parser for the language.
        :return: a default parser.
        """
        keywords = [{"re": re.compile(r"\s*return\s"), "factory": ReturnFactory()},
                    # Add int array keyword
                    {"re": re.compile(r"\s*(\w[\w]*)\s+((\w[\w]*)\s*\((.*)\))\s*{\s*"),
                     "factory": FunctionDeclarationFactory(), "scopeable": True},
                    {"re": re.compile(r"\s*class\s*(\w[\w]*)\s*{\s*"), "factory": ElangClassDeclarationFactory(),
                     "scopeable": True},
                    {"re": re.compile(r"\s*if\s*\((.*)\)\s*{\s*"), "factory": IfFactory(), "scopeable": True},
                    {"re": re.compile(r"\s*export\s*\s*{\s*"), "factory": ExportFactory(), "scopeable": True},
                    {"re": re.compile(r"\s*while\s*\((.*)\)\s*{\s*"), "factory": WhileFactory(), "scopeable": True}]
        operators = [{"re": re.compile(r"\s*\+\s*"), "factory": AdditionFactory()},
                     {"re": re.compile(r"\s*-\s*"), "factory": SubtractionFactory()},
                     {"re": re.compile(r"\s*\*\s*"), "factory": MultiplicationFactory()},
                     {"re": re.compile(r"\s*/\s*"), "factory": DivisionFactory()},
                     {"re": re.compile(r"\s*=\s*"), "factory": AssignmentFactory()},
                     {"re": re.compile(r"\s*==\s"), "factory": EqualFactory()},
                     {"re": re.compile(r"\s*>\s"), "factory": LogicalGreaterFactory()},
                     {"re": re.compile(r"\s*and\s"), "factory": LogicalAndFactory()},
                     {"re": re.compile(r"\s*or\s"), "factory": LogicalOrFactory()},
                     {"re": re.compile(r"\s*\[(.*)]\s*"), "factory": ArrayIndexerFactory()},
                     {"re": re.compile(r"\s*\.\s*"), "factory": DotOperatorFactory()},
                     {"re": re.compile(r"\s*new\s"), "factory": NewOperatorFactory()}]
        valid_tokens = [{"re": re.compile(r"\s*((\w[\w]*)\s*\((.*)\))\s*"), "factory": FunctionCallFactory()},
                        {"re": re.compile(r"\s*([a-zA-Z][\w]*)+"), "factory": VariableFactory()},
                        {"re": re.compile(r"\s*[\d]+"), "factory": DecimalConstantFactory()},
                        {"re": re.compile(r"\s*\(\s*"), "factory": LeftParenthesisFactory()},
                        {"re": re.compile(r"\s*\)\s*"), "factory": RightParenthesisFactory()}]
        return Parser(keywords=keywords, operators=operators, valid_tokens=valid_tokens).add_primitives(
            get_default_primitives())

    def __init__(self, keywords: [Dict], operators: [Dict], valid_tokens: [Dict]):
        """
        Initializes a new parser
        :param keywords: the keywords in the language, expects a regex and an appropriate factory to detect and create
        a keyword.
        :param operators: the operators in the language, expects a regex and an appropriate factory to detect and create
         an operator.
        :param valid_tokens: the tokens that are valid, but are not an operator or a keyword. expects a regex and an
        appropriate factory to detect and create the token
        """
        self.keywords = keywords
        self.operators = operators
        self.valid_tokens = valid_tokens
        self.defined_types = []

    def add_primitives(self, primitives_syntax: List[PrimitiveSyntax]):
        for syntax in primitives_syntax:
            self.keywords.append({"re": syntax.re, "factory": syntax.parsing_factory})
            self.defined_types.append(syntax.primitive)
        return self

    def parse_file(self, file: str) -> Program:
        """
        This function parses a file.
        :param file: the path to the file to parse.
        :return: list of functions that have been parsed.
        """
        global_scope = Scope('global', None)
        with open(file, "r") as f:
            source_code = f.read().strip()
        return self.parse_source_code(source_code, parent_scope=global_scope, top_level=True)

    def parse_source_code(self, source_code: str, parent_scope: Scope, top_level=False):
        """
        This function parses a source code into tokens.
        :param source_code: the source code to parse.
        :param parent_scope: the scope that hold the source code.
        :return: list of expressions that have been parsed.
        """
        parsed = []
        while len(source_code) is not 0:
            source_code = source_code.strip()
            next_token, match = self.get_maximal_match(source_code)
            if "scopeable" in next_token:
                # If the maximal token in the line produces a scope.
                parsed_token, source_code = next_token["factory"].produce(parser=self, source_code=source_code,
                                                                          parent_scope=parent_scope,
                                                                          match=match)
                parsed += parsed_token
            else:
                # Otherwise if the maximal token does not open a scope
                # The parser will parse an entire line (until ';') and then produce an expression.
                factory = next_token["factory"]
                model, source_code = next_token["factory"].produce_shallow(parser=self, source_code=source_code,
                                                                           parent_scope=parent_scope, match=match)
                match_models = [] + model
                while len(source_code) is not 0 and source_code[0] is not ';':
                    next_token, match = self.get_maximal_match(source_code)
                    model, source_code = next_token["factory"].produce_shallow(parser=self, source_code=source_code,
                                                                               parent_scope=parent_scope, match=match)
                    match_models += model
                source_code = source_code[1:]
                parsed += factory.produce(parser=self, source_code=None,
                                          parent_scope=parent_scope,
                                          match=match_models)
        if top_level:
            return Program(*self.classify_entities(parsed))
        return parsed

    def get_maximal_match(self, text: str) -> Tuple[Dict, Match]:
        """
        This function find the maximal regex match in the text.
        Keywords have a priority over valid tokens and operators.
        :param text: the text to search in.
        :return: the next maximal match in the text.
        """
        maximal_match, token_entry = None, None
        for token in self.keywords + self.operators:
            match = token["re"].match(text)
            if match is not None and (maximal_match is None or len(maximal_match.group(0)) < len(match.group(0))):
                maximal_match, token_entry = match, token
        for token in self.valid_tokens:
            match = token["re"].match(text)
            valid = True
            for candidate in self.keywords + self.operators:
                if candidate["re"].match(text) is not None:
                    valid = False
                    break
            if valid and match is not None and (
                    maximal_match is None or len(maximal_match.group(0)) < len(match.group(0))):
                maximal_match, token_entry = match, token
        return token_entry, maximal_match

    def resolve_type(self, name):
        return [vtype for vtype in self.defined_types if vtype.name == name][0]

    def classify_entities(self, tokens):
        globals, globals_initialization, functions, classes, exports = [], [], [], [], []
        for token in tokens:
            if isinstance(token, Function):
                functions.append(token)
            if isinstance(token, ElangClass):
                classes.append(token)
            if isinstance(token, VariableDeclaration):
                globals.append(token)
            if isinstance(token, Export):
                exports.append(token)
            else:
                globals_initialization.append(token)
        return globals, globals_initialization, functions, classes, exports
