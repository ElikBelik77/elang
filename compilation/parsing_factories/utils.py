from typing import Tuple

from compilation.models.keywords import VariableDeclaration


def find_scope_end(source_code: str) -> int:
    """
    This function find where the current scope ends.
    :param source_code: the source code.
    :return: the index of the end of the current scope.
    """
    count, idx = 1, 0
    while count is not 0:
        if source_code[idx] == "{":
            count += 1
        elif source_code[idx] == "}":
            count -= 1
        if count == 0:
            return idx
        idx += 1


def find_closing_parenthesis(source_code: str) -> Tuple[int, int]:
    """
    This function find the right parenthesis that closes the current parenthesis.
    :param source_code: the source code
    :return: the index of the ')' that closes the current '('
    """
    count, idx = 1, 0
    start = 0
    first = True
    while count is not 0:
        if source_code[idx] == "(" and first:
            first = False
            start = idx
        elif source_code[idx] == "(" and not first:
            count += 1
        elif source_code[idx] == ")":
            count -= 1
        if count == 0:
            return start, idx + 1
        idx += 1


def find_closing_brackets(source_code: str) -> Tuple[int, int]:
    """
    This function find the right parenthesis that closes the current parenthesis.
    :param source_code: the source code
    :return: the index of the ')' that closes the current '('
    """
    count, idx = 1, 0
    start = 0
    first = True
    while count is not 0:
        if source_code[idx] == "[" and first:
            first = False
            start = idx
        elif source_code[idx] == "[" and not first:
            count += 1
        elif source_code[idx] == "]":
            count -= 1
        if count == 0:
            return start, idx + 1
        idx += 1


def find_bracket_pairs(text: str):
    count, idx = 1, 1
    start = 0
    while idx < len(text):
        if (text[idx] != "[" and text[idx] != "]") and idx is not 0 and count is 0:
            break
        if text[idx] == "[":
            count += 1
            start = idx
        if text[idx] == "]":
            count -= 1
            if count == 0:
                yield (start, idx)
        idx += 1


def populate_scope(scope, body, match):
    for idx, statement in enumerate(body):
        if isinstance(statement, VariableDeclaration) and statement.name not in scope.defined_variables:
            scope.defined_variables[statement.name] = {"type": statement.var_type, "define_line": idx,
                                                       "scope": scope}
        elif isinstance(statement, VariableDeclaration):
            raise Exception(
                "Variable {0} is declared more than once in scope {1}".format(statement.name, match.group(0)))
