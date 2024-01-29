from compiler.tokenizer import Token
import compiler.ast as ast


class ParseError(Exception):

    pass


def parse(tokens: list[Token]) -> ast.Expression:
    pos = 0

    def peek() -> Token:
        if pos < len(tokens):
            return tokens[pos]
        else:
            return Token(
                type="end",
                text="",
            )

    def consume(expected: str | list[str] | None = None) -> Token:
        nonlocal pos
        token = peek()
        if isinstance(expected, str) and token.text != expected:
            raise ParseError(f'{token.type}: expected "{expected}"')
        if isinstance(expected, list) and token.text not in expected:
            comma_separated = ", ".join([f'"{e}"' for e in expected])
            raise ParseError(
                f'{token.type}: expected one of: {comma_separated}')
        pos += 1
        return token

    def parse_int_literal() -> ast.Literal:
        if peek().type != 'int_literal':
            raise ParseError(f'{peek().type}: expected an integer literal')
        token = consume()
        return ast.Literal(int(token.text))

    def parse_identifier() -> ast.Identifier:
        if peek().type != 'identifier':
            raise ParseError(f'{peek().type}: expected an identifier')
        token = consume()
        return ast.Identifier(token.text)

    def parse_term() -> ast.Expression:
        if peek().type == 'int_literal':
            return parse_int_literal()
        elif peek().type == 'identifier':
            return parse_identifier()
        else:
            raise ParseError(
                f'{peek().type}: expected an integer literal or an identifier')

    def parse_expression() -> ast.Expression:
        left = parse_term()
        while peek().text in ["+", "-"]:
            operator_token = consume(['+', '-'])
            right = parse_term()
            left = ast.BinaryOp(
                left,
                operator_token.text,
                right
            )
        if peek().type != 'end':
            raise ParseError(f'{peek().type}: expected an end')
        return left

    return parse_expression()
