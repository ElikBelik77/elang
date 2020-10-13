from compilation.models.keywords import *
from typing import Match


class Factory:
    """
    Class that produces models based on parsed tokens.
    """

    def produce(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        """
        Produces a model based on a token from the source code, when the model is the first token in the line.
        :param parser: the parser that parsed the token.
        :param source_code: the source code.
        :param parent_scope: the parent scope of the token.
        :param match: the token that was matched.
        :return: list of expressions that were created by the match.
        """
        pass

    def produce_shallow(self, parser: "Parser", source_code: str, parent_scope: Scope, match: [Match]):
        """
        Produces a model for shunting yard purpose, if it not the first token in the line.
        :param parser: the parser that parsed the token.
        :param source_code: the source code.
        :param parent_scope: the parent scope of the token.
        :param match: the token that was matched.
        :return: (expression, source_code) where expression is the produces shallow expression and source_code is the
        original source code without the current match.
        """
        pass
