import regex
import re
from collections import deque
from models import LeftParenthesis, RightParenthesis
from factories import *
from typing import *


class Parser:
    def __init__(self, keywords: [Dict], operators: [Dict], valid_tokens: [Dict]):
        self.keywords = keywords
        self.operators = operators
        self.valid_tokens = valid_tokens

    def parse_file(self, file: str):
        global_scope = Scope('global', None)
        with open(file, "r") as f:
            source_code = f.read().strip()
        return self.parse_source_code(source_code, parent_scope=global_scope)

    def parse_source_code(self, source_code: str, parent_scope: Scope):
        parsed = []
        while len(source_code) is not 0:
            source_code = source_code.strip()
            next_token, match = self.get_maximal_match(source_code)
            if "scopeable" in next_token:
                parsed_token, source_code = next_token["factory"].produce(parser=self, source_code=source_code,
                                                                          parent_scope=parent_scope,
                                                                          match=match)
                parsed += parsed_token
            else:
                factory = next_token["factory"]
                model, source_code = next_token["factory"].produce_shallow(parser=self, source_code=source_code,
                                                                           parent_scope=parent_scope, match=match)
                match_models = [model]
                while len(source_code) is not 0 and source_code[0] is not ';':
                    next_token, match = self.get_maximal_match(source_code)
                    model, source_code = next_token["factory"].produce_shallow(parser=self, source_code=source_code,
                                                                               parent_scope=parent_scope, match=match)
                    match_models.append(model)
                source_code = source_code[1:]
                parsed += factory.produce(parser=self, source_code=None,
                                          parent_scope=parent_scope,
                                          match=match_models)
        return parsed

    def get_maximal_match(self, text: str):
        maximal_match, token_entry = None, None
        for token in self.keywords + self.operators:
            match = token["re"].match(text)
            if match is not None and (maximal_match is None or len(maximal_match.group(0)) < len(match.group(0))):
                maximal_match, token_entry = match, token
        for token in self.valid_tokens:
            match = token["re"].match(text)
            valid = True
            for candidate in self.keywords:
                if candidate["re"].match(text) is not None:
                    valid = False
                    break
            if valid and match is not None and (
                    maximal_match is None or len(maximal_match.group(0)) < len(match.group(0))):
                maximal_match, token_entry = match, token
        return token_entry, maximal_match
