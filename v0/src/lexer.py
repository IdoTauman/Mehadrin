from .tokens import *

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

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            i = 0
            while i < len(line):
                char: str = line[i]

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

    if not tokens or not isinstance(tokens[-1], Semicolon): tokens.append(Semicolon())

    return tokens

