from typing import List, Literal, Tuple
import re
from dataclasses import dataclass


TokenType = Literal["int_literal", "identifier", "parenthesis", "end"]


@dataclass(frozen=True)
class Token:
    type: TokenType
    text: str


def regex_check(expression: re.Pattern, source_code: str, position: int, result: List[Token], tokenType: TokenType) -> Tuple[int, List[Token], bool]:
    match = expression.match(source_code, position)
    success = False
    if match is not None:
        result.append(Token(
            type=tokenType,
            text=source_code[position:match.end()]
        ))
        success = True
        position = match.end()

    return position, result, success


def tokenize(source_code: str) -> List[Token]:
    whitespace_re = re.compile(r'\s+')
    integer_re = re.compile(r'[0-9]+')
    identifier_re = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
    operator_re = re.compile(r'[\\+-\\*]')
    paren_re = re.compile(r'[()]')

    result: list[Token] = []
    position = 0
    while position < len(source_code):

        match = whitespace_re.match(source_code, position)
        if match is not None:
            position = match.end()
            continue

        position, result, success = regex_check(
            identifier_re, source_code, position, result, "identifier")
        if success:
            continue

        position, result, success = regex_check(
            integer_re, source_code, position, result, "int_literal")
        if success:
            continue

        position, result, success = regex_check(
            operator_re, source_code, position, result, "identifier")
        if success:
            continue

        position, result, success = regex_check(
            paren_re, source_code, position, result, "parenthesis")
        if success:
            continue

        raise Exception(
            f'Tokenization failed near{source_code[position:(position + 10)]}...')
        # TODO Refactor these to cleaner.
    return result
