from abc import ABC
from enum import Enum

class Token(ABC):
    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        if isinstance(self, Literal):
            if isinstance(self, IntLiteral): return f'Int({self.value})'
            elif isinstance(self, FloatLiteral): return f'Float({self.value})'
            elif isinstance(self, CharLiteral): return f'Char(\'{self.value}\')'
            elif isinstance(self, StringLiteral): return f'String("{self.value}")'
            else: return f'Literal({self.value})'

        OPERATORS = {
            PlusOperator: '+',
            MinusOperator: '-',
            MulOperator: '*',
            DivOperator: '/',
            ModOperator: '%',

            AssignmentOperator: '=',

            EqualOperator: '==',
            NeqOperator: '!=',
            LessthanOperator: '<',
            LeqOperator: '<=',
            GreaterthanOperator: '>',
            GeqOperator: '>=',
            LogicalAndOperator: '&&',
            LogicalOrOperator: '||',
            LogicalNotOperator: '!',

            AddressOperator: '&',
            DerefOperator: '*',
            UplusOperator: '+',
            UminusOperator: '-',

            StarToken: '*',
            AmpersandToken: '&',
            PlusToken: '+',
            MinusToken: '-',
        }

        if self.__class__ in OPERATORS:
            return OPERATORS[self.__class__]

        SYMBOLS = {
            Semicolon: ';',
            OpenParenthesis: '(',
            CloseParenthesis: ')',
            OpenBracket: '[',
            CloseBracket: ']',
            OpenBrace: '{',
            CloseBrace: '}',
            Comma: ',',
            Dot: '.',
            Arrow: '->',
            Colon: ':',
        }

        if self.__class__ in SYMBOLS: return SYMBOLS[self.__class__]

        if isinstance(self, Keyword):
            # Mapping enum values back to their Hebrew names for display
            KEYWORDS = {
                KeywordEnum.שלם: "int",
                KeywordEnum.ארוך: "long",
                KeywordEnum.קצר: "short",
                KeywordEnum.ריק: "void",
                KeywordEnum.תו: "char",
                KeywordEnum.מסומן: "signed",
                KeywordEnum.לאמסומן: "unsigned",
                KeywordEnum.צף: "float",
                KeywordEnum.כפול: "double",
                KeywordEnum.קבוע: "const",
                KeywordEnum.מבנה: "struct",
                KeywordEnum.איחוד: "union",
                KeywordEnum.הגדרסוג: "typedef",
                KeywordEnum.מספור: "enum",
                KeywordEnum.שבור: "break",
                KeywordEnum.החלף: "switch",
                KeywordEnum.מקרה: "case",
                KeywordEnum.המשך: "continue",
                KeywordEnum.ברירתמחדל: "default",
                KeywordEnum.עשה: "do",
                KeywordEnum.כאשר: "while",
                KeywordEnum.אם: "if",
                KeywordEnum.אחרת: "else",
                KeywordEnum.עבור: "for",
                KeywordEnum.החזר: "return",
            }
            return KEYWORDS[self.value]

        if isinstance(self, Identifier): return f"Identifier({self.name})"

        return f"<{self.__class__.__name__}>"



class Literal(Token):
    def __init__(self):
        self.value = None
        super().__init__()

class IntLiteral(Literal):
    def __init__(self, val: int):
        super().__init__()
        self.value: int = val

class CharLiteral(Literal):
    def __init__(self, val: str):
        if not len(val) == 1: raise ValueError(f"Expected char, got string {val}")
        super().__init__()
        self.value: str = val

class StringLiteral(Literal):
    def __init__(self, val: str):
        super().__init__()
        self.value = val

class FloatLiteral(Literal):
    def __init__(self, val: float):
        super().__init__()
        self.value = val



class Operator(Token, ABC):
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
    שלם = 1
    ארוך = 2
    קצר = 3
    ריק = 4
    תו = 5
    מסומן = 6
    לאמסומן = 7
    צף = 8
    כפול = 9
    קבוע = 10
    מבנה = 11
    איחוד = 12
    הגדרסוג = 13
    מספור = 14
    שבור = 15
    החלף = 16
    מקרה = 17
    המשך = 18
    ברירתמחדל = 19
    עשה = 20
    כאשר = 21
    אם = 22
    אחרת = 23
    עבור = 24
    החזר = 25

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
class StarToken(Operator):
    def __init__(self):
        super().__init__()

class AmpersandToken(Operator):
    def __init__(self):
        super().__init__()

class PlusToken(Operator):
    def __init__(self):
        super().__init__()

class MinusToken(Operator):
    def __init__(self):
        super().__init__()