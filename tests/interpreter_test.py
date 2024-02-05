from compiler.ast import BinaryOp, Expression,  Literal,  Identifier
from compiler.parser import ParseError, parse
from compiler.tokenizer import Token, tokenize
from compiler.interpreter import IntepretError, interpret


def test_interpreter() -> None:
    assert interpret(parse(tokenize("3 + 5"))) == 8
    assert interpret(parse(tokenize("42"))) == 42
    assert interpret(parse(tokenize("3 - 5"))) == -2
