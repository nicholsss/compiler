from typing import Any, Callable, Self
from compiler import ast

Value = int | bool | Callable | None


class IntepretError(Exception):
    pass


class SymTab:
    def __init__(self, locals: dict[str, int | bool | Callable], parent: Self | None):
        self.locals: dict[str, Value] = {}
        self.parent: Self | None = parent

    def get(self, varName: str) -> Value:
        if varName in self.locals:
            return self.locals[varName]
        if self.parent:
            return self.parent.get(varName)
        return None

    def set(self, varName: str, value: Value):
        self.locals[varName] = value
    # locals: dict[str, int | bool | Callable]
    # parent: Self | None


def initialize_symbol_table() -> SymTab:
    top_level = SymTab()
    top_level.set('+', lambda a, b: a + b)
    top_level.set('-', lambda a, b: a - b)
    top_level.set('*', lambda a, b: a * b)

    top_level.set('unary_-', lambda a: -a)
    return top_level


def interpret(node: ast.Expression, symbolTable: SymTab) -> Value:
    match node:
        case ast.Literal():
            return node.value

        case ast.BinaryOp():
            a: Any = interpret(node.left, symbolTable)
            b: Any = interpret(node.right, symbolTable)

            operator_val = symbolTable.locals.get(node.op)

            if operator_val is not None:
                return operator_val(a, b)
            else:
                raise IntepretError('error')

        case ast.UnaryOp():
            a = interpret(node.operand, symbolTable)
            operator_func = symbolTable.get(f"unary_{node.op}")
            if operator_func is not None:
                return operator_func(operand)
            else:
                raise IntepretError("Unsupported unary operator")

        case ast.varAssign(name, value):
            exp_value = interpret(value, symbolTable)
            symbolTable.set(name, exp_value)


symbol_table = initialize_symbol_table()
