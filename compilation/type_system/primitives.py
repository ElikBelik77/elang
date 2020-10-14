import re

from compilation.parsing_factories.keywords import PrimitiveFactory


class Primitive:
    def __init__(self, name):
        self.name = name


class PrimitiveSyntax:
    def __init__(self, primitive, regex, parsing_factory):
        self.primitive = primitive
        self.re = regex
        self.parsing_factory = parsing_factory


def get_default_primitives():
    int_p = Primitive("int")
    int_syntax = PrimitiveSyntax(int_p, re.compile(r"\s*int\s+"), PrimitiveFactory(int_p))
    return [int_syntax]
