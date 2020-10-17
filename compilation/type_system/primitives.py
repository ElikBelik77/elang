import re
from compilation.parsing_factories.keywords import PrimitiveFactory
from typing import Dict, List


class Primitive:
    """
    Class for primitive types.
    """

    def __init__(self, name):
        self.name = name

    def get_size(self, bundle: Dict):
        """
        Returns the size of this primitive based on the bundle.
        :param bundle: the compilation bundle to use.
        :return: the size of this primitive.
        """
        return bundle[self.name]


class PrimitiveSyntax:
    """
    Class for identifying primitives.
    """

    def __init__(self, primitive, regex):
        """
        Initializes a primitive syntax
        :param primitive: the primitive
        :param regex: the regex that detects the primitive
        :param parsing_factory: the factory that parses the primitive
        """
        self.primitive = primitive
        self.re = regex
        self.parsing_factory = PrimitiveFactory(primitive)


def get_default_primitives() -> List[PrimitiveSyntax]:
    """
    This function returns the default primitives of the language.
    :return: list of the primitive syntax of the language.
    """
    int_syntax = PrimitiveSyntax(Primitive("int"), re.compile(r"\s*int(\s+|\[)"))
    char_syntax = PrimitiveSyntax(Primitive("char"), re.compile(r"\s*char(\s+|\[)"))
    return [int_syntax, char_syntax]
