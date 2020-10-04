from parsing_models import *
from expression_factory import *


class SyntaxConverter:
    def __init__(self):
        self.keywords = {'int': IntFactory(), 'return': ReturnFactory()}

    def convert_function(self, function):
        converted_statements = []
        for statements in function.body:
            for converted_statement in self.convert_statements(function, statements):
                converted_statements += converted_statement
        function.body = converted_statements
        for statement in function.body:
            if isinstance(statement, VariableDeclaration) and function.scope.search_variable(statement.name):
                raise Exception("Variable {0} is defined twice at function {1}".format(statement.name, function.name))
            elif isinstance(statement, VariableDeclaration):
                function.scope.defined_variables[statement.name] = statement.type



    def convert_statements(self, function, statement):
        if isinstance(statement[0], NameMatch) and statement[0].value in self.keywords:
            yield self.keywords[statement[0].value].produce(function, statement)
