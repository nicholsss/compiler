from typing import List, Literal, Tuple
import re
from dataclasses import dataclass


TokenType = Literal["int_literal", "identifier", "parenthesis", "end", ]


@dataclass(frozen=True)
class Token:
    type: TokenType
    text: str


def regex_check(expression: re.Pattern, source_code: str, position: int, result: List[Token], tokenType: TokenType) -> Tuple[int, List[Token], bool]:
    match = expression.match(source_code, position)
    if match is None:
        return position, result, False
    result.append(Token(
        type=tokenType,
        text=source_code[position:match.end()]
    ))
    position = match.end()

    return position, result, True


def tokenize(source_code: str) -> List[Token]:
    whitespace_re = re.compile(r'\s+')
    result: list[Token] = []
    position = 0

    expressions: List[Tuple[re.Pattern, TokenType]] = [
        (re.compile(r'[0-9]+'), "int_literal"),
        (re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*'), "identifier"),
        (re.compile(r'[\\+-\\*]'), "identifier"),
        (re.compile(r'[()]'), "parenthesis")
    ]
    while position < len(source_code):

        match = whitespace_re.match(source_code, position)
        if match is not None:
            position = match.end()
            continue

        success = False
        for (expression, type) in expressions:
            position, result, success = regex_check(
                expression, source_code, position, result, type)
            if success:
                break
        else:
            raise Exception(
                f'Tokenization failed near{source_code[position:(position + 10)]}...')
    return result
