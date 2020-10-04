from parsing_models import *


class SyntaxConverter:
    def __int__(self):
        self.keywords = {'int': None, 'return': None}

    def convert_statements(self, function, statement):
        if isinstance(statement[0], NameMatch) and statement[0].value in self.keywords:
            yield self.keywords[statement[0].value].produce(function, statement)
