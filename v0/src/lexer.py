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

    PARENTHESIS = {
        '(': (OpenParenthesis, "paren", 1),
        ')': (CloseParenthesis, "paren", -1),
        '[': (OpenBracket, "bracket", 1),
        ']': (CloseBracket, "bracket", -1),
        '{': (OpenBrace, "brace", 1),
        '}': (CloseBrace, "brace", -1),
    }

    OPERATORS = {
        '==': EqualOperator, '!=': NeqOperator, '<=': LeqOperator, 
        '>=': GeqOperator, '&&': LogicalAndOperator, '||': LogicalOrOperator,
        '->': Arrow, '+': PlusToken, '-': MinusToken, '*': StarToken,
        '/': DivOperator, '%': ModOperator, '=': AssignmentOperator,
        '<': LessthanOperator, '>': GreaterthanOperator, '!': LogicalNotOperator,
        '&': AmpersandToken, '.': Dot, ';': Semicolon, ':': Colon, ',': Comma,
    }

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            i = 0
            while i < len(line):
                char = line[i]

                # Skip whitespace and handle ASI
                if char.isspace():
                    if char == '\n':
                        is_balanced = not any(open_counts.values())
                        if is_balanced and tokens and isValidEndLine(tokens[-1]):
                            tokens.append(Semicolon())
                    i += 1
                    continue

                # String literals
                if char == '"':
                    i += 1
                    buffer = ""
                    while i < len(line) and line[i] != '"':
                        if line[i] == '\n': error("Unterminated string literal")
                        if line[i] == '\\':
                            # Handle escape sequences
                            if i + 1 >= len(line): error("Trailing backslash")
                            esc = line[i+1]
                            mapping = {'\'':'\'', '"':'"', '\\':'\\', 'א':'\a', 'ב':'\b', 'נ':'\n', 'ר':'\r', 'ט':'\t'}
                            if esc in mapping:
                                buffer += mapping[esc]
                                i += 2
                            else: error(f"Invalid escape: \\{esc}")
                        else:
                            buffer += line[i]
                            i += 1
                    if i >= len(line): error("Unterminated string literal")
                    tokens.append(StringLiteral(buffer))
                    i += 1
                    continue

                # Char literals
                if char == "'":
                    i += 1
                    buffer = ""
                    if i < len(line) and line[i] == '\\':
                        # Escape sequences
                        esc = line[i+1]
                        mapping = {'\'':'\'', '"':'"', '\\':'\\', 'א':'\a', 'ב':'\b', 'נ':'\n', 'ר':'\r', 'ט':'\t'}
                        if esc in mapping:
                            buffer += mapping[esc]
                            i += 2
                        else: error(f"Invalid escape: \\{esc}")
                    elif i < len(line) and line[i] != "'":
                        buffer = line[i]
                        i += 1
                    
                    if i >= len(line) or line[i] != "'": error("Unterminated or invalid char literal")
                    if len(buffer) == 0: error("Empty char literal")
                    tokens.append(CharLiteral(buffer))
                    i += 1
                    continue

                # Number literals
                if char.isdigit() or (char == '.' and i + 1 < len(line) and line[i+1].isdigit()):
                    num_buffer = ""
                    has_dot = False
                    if char == '.': # Leading dot
                        num_buffer = "0."
                        has_dot = True
                        i += 1
                    
                    while i < len(line) and (line[i].isdigit() or line[i] == '.'):
                        if line[i] == '.':
                            if has_dot: error("Multiple decimal points in number")
                            has_dot = True
                        num_buffer += line[i]
                        i += 1
                    
                    if has_dot: tokens.append(FloatLiteral(float(num_buffer)))
                    else: tokens.append(IntLiteral(int(num_buffer)))
                    continue

                # Multi character operators
                two_char = line[i:i+2]
                if two_char in OPERATORS:
                    tokens.append(OPERATORS[two_char]())
                    i += 2
                    continue

                # Single character symbols/operators
                if char in PARENTHESIS:
                    if char in '}': # Closing blocks
                        is_balanced = not any(open_counts.values())
                        if tokens and isValidEndLine(tokens[-1]):
                            tokens.append(Semicolon())
                    
                    cclass, key, delta = PARENTHESIS[char]
                    tokens.append(cclass())
                    open_counts[key] += delta
                    i += 1
                    continue

                if char in OPERATORS:
                    tokens.append(OPERATORS[char]())
                    i += 1
                    continue

                # Identifiers
                if char.isalpha() or char == '_' or ('א' <= char <= 'ת'):
                    start = i
                    while i < len(line) and (line[i].isalnum() or line[i] == '_' or ('א' <= line[i] <= 'ת')):
                        i += 1
                    word = line[start:i]

                    # Keywords
                    try:
                        kw_enum = KeywordEnum[word.upper()]
                        tokens.append(Keyword(kw_enum))
                    except KeyError:
                        tokens.append(Identifier(word))
                    continue

                error(f"Unexpected character: {char}")
                i += 1

    # End of File Semicolon
    if not tokens or not isinstance(tokens[-1], Semicolon):
        tokens.append(Semicolon())

    return tokens