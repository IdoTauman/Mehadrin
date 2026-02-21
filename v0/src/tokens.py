from abc import ABC
from enum import Enum

class Token(ABC):
    def __init__(self):
        super().__init__()



class Literal(Token):
    def __init__(self):
        super().__init__()

class IntLiteral(Literal):
    def __init__(self, val: int):
        self.value: int = val
        super().__init__()

class CharLiteral(Literal):
    def __init__(self, val: str):
        if not len(val) == 1: raise ValueError(f"Expected char, got string {val}")
        self.value: str = val
        super().__init__()

class StringLiteral(Literal):
    def __init__(self, val: str):
        self.value = val
        super().__init__()

class FloatLiteral(Literal):
    def __init__(self, val: float):
        self.value = val
        super().__init__()



class Operator(ABC):
    def __init__(self):
        super().__init__()

class PlusOperator(Operator):
    def __init__(self):
        super().__init__()

class MinusOperator(Operator):
    def __init__(self):
        super().__init__()

class MulOperator(Operator):
    def __init__(self):
        super().__init__()

class DivOperator(Operator):
    def __init__(self):
        super().__init__()

class ModOperator(Operator):
    def __init__(self):
        super().__init__()

class AssignmentOperator(Operator):
    def __init__(self):
        super().__init__()

class AddressOperator(Operator):
    def __init__(self):
        super().__init__()

class DerefOperator(Operator):
    def __init__(self):
        super().__init__()

class UplusOperator(Operator):
    def __init__(self):
        super().__init__()

class UminusOperator(Operator):
    def __init__(self):
        super().__init__()

class LogicalNotOperator(Operator):
    def __init__(self):
        super().__init__()

class LogicalAndOperator(Operator):
    def __init__(self):
        super().__init__()

class LogicalOrOperator(Operator):
    def __init__(self):
        super().__init__()

class EqualOperator(Operator):
    def __init__(self):
        super().__init__()

class LessthanOperator(Operator):
    def __init__(self):
        super().__init__()

class LeqOperator(Operator):
    def __init__(self):
        super().__init__()

class GreaterthanOperator(Operator):
    def __init__(self):
        super().__init__()

class GeqOperator(Operator):
    def __init__(self):
        super().__init__()

class NeqOperator(Operator):
    def __init__(self):
        super().__init__()



class Semicolon(Token):
    def __init__(self) -> None:
        super().__init__()

class OpenParenthesis(Token):
    def __init__(self) -> None:
        super().__init__()

class CloseParenthesis(Token):
    def __init__(self) -> None:
        super().__init__()

class OpenBracket(Token):
    def __init__(self) -> None:
        super().__init__()

class CloseBracket(Token):
    def __init__(self) -> None:
        super().__init__()

class OpenBrace(Token):
    def __init__(self) -> None:
        super().__init__()

class CloseBrace(Token):
    def __init__(self) -> None:
        super().__init__()

class Comma(Token):
    def __init__(self):
        super().__init__()

class Dot(Token):
    def __init__(self):
        super().__init__()

class Arrow(Token):
    def __init__(self):
        super().__init__()

class Colon(Token):
    def __init__(self):
        super().__init__()




class KeywordEnum(Enum):
    NUM_KEYWORDS = 25
    INT = 1
    LONG = 2
    SHORT = 3
    VOID = 4
    CHAR = 5
    SIGNED = 6
    UNSIGNED = 7
    FLOAT = 8
    DOUBLE = 9
    CONST = 10
    STRUCT = 11
    UNION = 12
    TYPEDEF = 13
    ENUM = 14
    BREAK = 15
    SWITCH = 16
    CASE = 17
    CONTINUE = 18
    DEFAULT = 19
    DO = 20
    WHILE = 21
    IF = 22
    ELSE = 23
    FOR = 24
    RETURN = 25

class Keyword(Token):
    def __init__(self, val: KeywordEnum):
        self.value: KeywordEnum = val
        super().__init__()



class Identifier(Token):
    def __init__(self, name: str):
        if not name: raise ValueError("Got empty string")
        self.name = name
        super().__init__()



# Ambiguous classes that get resolved by the parser
class StarToken(Token):
    def __init__(self):
        super().__init__()

class AmpersandToken(Token):
    def __init__(self):
        super().__init__()

class PlusToken(Token):
    def __init__(self):
        super().__init__()

class MinusToken(Token):
    def __init__(self):
        super().__init__()