from compiler.tokenizer import tokenize, Token


def test_tokenizer() -> None:
    assert tokenize("hello") == [
        Token(type='identifier', text='hello')
    ]
    assert tokenize("number and 1") == [
        Token(type='identifier', text='number'),
        Token(type='identifier', text='and'),
        Token(type='int_literal', text='1')
    ]
    assert tokenize("3 + 5") == [
        Token(type='int_literal', text='3'),
        Token(type='identifier', text='+'),
        Token(type='int_literal', text='5')
    ]
