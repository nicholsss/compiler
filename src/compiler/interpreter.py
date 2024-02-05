from typing import Any
from compiler import ast

Value = int | bool | None


class IntepretError(Exception):
    pass


def interpret(node: ast.Expression) -> Value:
    match node:
        case ast.Literal():
            return node.value

        case ast.BinaryOp():
            a: Any = interpret(node.left)
            b: Any = interpret(node.right)
            if node.op == '+':
                return a + b

            if node.op == '-':
                return a - b
    raise IntepretError('error')
