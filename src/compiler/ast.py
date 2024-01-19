from dataclasses import dataclass


@dataclass
class Expression:
    "Base class for expression AST nodes"


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class Literal():
    value: object
