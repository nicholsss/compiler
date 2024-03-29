from compiler.ast import BinaryOp, Expression,  Literal,  Identifier
from compiler.parser import ParseError, parse
from compiler.tokenizer import Token, tokenize


def test_ast() -> None:
    assert parse([Token(type='identifier', text='hello'), ]
                 ) == Identifier("hello")

    assert parse([Token(type='int_literal', text='2'), ]
                 ) == Literal(2)

    assert parse([
        Token(type='int_literal', text='2'),
        Token(type='identifier', text='+'),
        Token(type='identifier', text='x'),
    ]) == BinaryOp(
        left=Literal(value=2),
        op="+",
        right=Identifier(name='x'),
    )

    assert parse([
        Token(type='int_literal', text='2'),
        Token(type='identifier', text='+'),
        Token(type='identifier', text='x'),
        Token(type='identifier', text='-'),
        Token(type='identifier', text='y'),
    ]) == BinaryOp(
        left=BinaryOp(left=Literal(value=2), op="+",
                      right=Identifier(name='x')),
        op="-",
        right=Identifier(name="y")
    )

    assert parse([
        Token(type='int_literal', text='2'),
        Token(type='identifier', text='+'),
        Token(type='identifier', text='x'),
        Token(type='identifier', text='-'),
        Token(type='identifier', text='y'),
        Token(type='identifier', text='+'),
        Token(type='identifier', text='z'),
    ]) == BinaryOp(
        left=BinaryOp(
            left=BinaryOp(left=Literal(value=2), op="+",
                          right=Identifier(name='x')),
            op="-",
            right=Identifier(name="y")),
        op="+",
        right=Identifier("z")
    )

    assert parse(tokenize('1 - (2 + 3)')) == BinaryOp(
        left=Literal(value=1),
        op="-",
        right=BinaryOp(left=Literal(value=2), op='+', right=Literal(3))
    )

    try:
        parse([
            Token(type='int_literal', text='2'),
            Token(type='identifier', text='x'),
        ])
        assert False
    except ParseError:
        pass

    try:
        parse(tokenize('2)'))
        assert False
    except ParseError:
        pass
