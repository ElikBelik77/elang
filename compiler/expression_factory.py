from expressions import *
from parsing_models import *



class ReturnFactory:
    def produce(self, function, statement):
        if isinstance(statement, ConstantMatch):
            return Return(ConstantValue(statement))
