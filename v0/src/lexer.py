from src.tokens import *
from .util import error

def isValidEndLine(t: Token) -> bool:
    literal_types = (IntLiteral, CharLiteral, FloatLiteral, StringLiteral, Identifier)
    closing_types = (CloseParenthesis, CloseBracket, CloseBrace)

    if isinstance(t, literal_types + closing_types):
        return True

    if isinstance(t, Keyword):
        return t.value in {KeywordEnum.BREAK, KeywordEnum.CONTINUE, KeywordEnum.RETURN}

    return False

def lexer(input_path: str) -> list[Token]:
    tokens: list[Token] = []

    open_counts = {"paren": 0, "bracket": 0, "brace": 0}

    open_string = False
    open_char = False

    PARENTHESIS = {
        '(': (OpenParenthesis, "paren", 1),
        ')': (CloseParenthesis, "paren", -1),
        '[': (OpenBracket, "bracket", 1),
        ']': (CloseBracket, "bracket", -1),
        '{': (OpenBrace, "brace", 1),
        '}': (CloseBrace, "brace", -1),
    }

    OPERATORS = {
        '+': PlusToken,
        '-': MinusToken,
        '*': StarToken,
        '/': DivOperator,
        '%': ModOperator,

        '=': AssignmentOperator,
        '==': EqualOperator,
        '!=': NeqOperator,
        '<': LessthanOperator,
        '<=': LeqOperator,
        '>': GreaterthanOperator,
        '>=': GeqOperator,

        '&&': LogicalAndOperator,
        '||': LogicalOrOperator,
        '!': LogicalNotOperator,

        '&': AmpersandToken,
        '->': Arrow,
        '.': Dot,

        ';': Semicolon,
        ':': Colon,
        ',': Comma,
    }

    buffer = ''

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            i = 0
            while i < len(line):
                char: str = line[i]

                if (open_string):
                    if char == '\n':
                        error("Unterminated string literal")

                    if char == '"':
                        tokens.append(StringLiteral(buffer))
                        buffer = ''
                        i += 1
                        open_string = False
                        continue

                    if char == '\\':
                        if i + 1 >= len(line):
                            error("Trailing backslash at the end of line")

                        next = line[i + 1]
                        if next == '\'':
                            buffer += '\''
                        elif next == '\"':
                            buffer += '\"'
                        elif next == '\\':
                            buffer += '\\'
                        elif next == 'א':
                            buffer += '\a'
                        elif next == 'ב':
                            buffer += '\b'
                        elif next == 'נ':
                            buffer += '\n'
                        elif next == 'ר':
                            buffer += '\r'
                        elif next == 'ט':
                            buffer += '\t'
                        else:
                            error(f"Invalid escape sequence: \\{next}")
                        i += 2
                        continue

                    buffer += char
                    i += 1
                    continue


                if (open_char):
                    if char == '\n':
                        error("Unterminated char literal")

                    if char == "'":
                        if len(buffer) == 0:
                            error("Empty char literal")
                        tokens.append(CharLiteral(buffer))
                        buffer = ''
                        i += 1
                        open_char = False
                        continue

                    if char == '\\':
                        if i + 1 >= len(line):
                            error("Trailing backslash at the end of line")

                        next = line[i + 1]
                        if next == '\'':
                            buffer += '\''
                        elif next == '\"':
                            buffer += '\"'
                        elif next == '\\':
                            buffer += '\\'
                        elif next == 'א':
                            buffer += '\a'
                        elif next == 'ב':
                            buffer += '\b'
                        elif next == 'נ':
                            buffer += '\n'
                        elif next == 'ר':
                            buffer += '\r'
                        elif next == 'ט':
                            buffer += '\t'
                        else:
                            error(f"Invalid escape sequence: \\{next}")
                        i += 2
                        if len(buffer) > 1:
                            error("Char literal longer than one character")
                        continue

                    buffer += char
                    i += 1

                    if len(buffer) > 1:
                        error("Char literal longer than one character")
                    continue


                if char.isspace():
                    if char == '\n':
                        is_balanced = not any(open_counts.values())
                        if is_balanced and (not tokens or isValidEndLine(tokens[-1])):
                            tokens.append(Semicolon())
                    i += 1
                    continue

                if char in PARENTHESIS:
                    cclass, key, delta = PARENTHESIS[char]
                    tokens.append(cclass())
                    open_counts[key] += delta
                    i += 1
                    continue

                if char in OPERATORS:
                    tokens.append(OPERATORS[char]())
                    i += 1
                    continue

                if char == '"':
                    open_string = True
                    i += 1
                    continue
                elif char == "'":
                    open_char = True
                    i += 1
                    continue

    if not tokens or not isinstance(tokens[-1], Semicolon): tokens.append(Semicolon())

    return tokens

