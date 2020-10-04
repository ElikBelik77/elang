from parsing_models import *
from expression_factory import *


class SyntaxConverter:
    def __init__(self):
        self.keywords = {'int': IntFactory(), 'return': ReturnFactory()}

    def convert_statements(self, function, statement):
        if isinstance(statement[0], NameMatch) and statement[0].value in self.keywords:
            yield self.keywords[statement[0].value].produce(function, statement)

