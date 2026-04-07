from typing import Type, cast, TypeVar

from AstNodes import *
from tokens import *
from util import error

T = TypeVar("T", bound=Token)


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
        self.pos: int = 0

    # --- Navigation Helpers ---

    def current_token(self) -> Token | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def peek(self, offset: int = 1) -> Token | None:
        """Look ahead without consuming."""
        index = self.pos + offset
        return self.tokens[index] if index < len(self.tokens) else None

    def eat(self, token_type: Type[T]) -> T:
        """Consume the token if it matches the type, otherwise raise error."""
        token = self.current_token()
        if isinstance(token, token_type):
            self.pos += 1
            return token
        raise Exception(
            f"Expected {token_type.__name__}, got {type(token).__name__} at pos {self.pos}"
        )

    def match(self, token_type: Type[Token]) -> bool:
        """Check type and consume if it matches. Returns True/False."""
        if isinstance(self.current_token(), token_type):
            self.pos += 1
            return True
        return False

    # --- Main Entry Point ---

    def parse(self) -> ProgramNode:
        statements = []
        while self.pos < len(self.tokens):
            statements.append(self.parse_statement())
        return ProgramNode(statements)

    # --- Dispatcher ---

    def parse_statement(self) -> AstNode:
        token = self.current_token()

        if isinstance(token, OpenBrace):
            return self.parse_block()

        if isinstance(token, Keyword):
            # Check for types (שלם, וכו')
            TYPE_KEYWORDS = {
                KeywordEnum.שלם,
                KeywordEnum.תו,
                KeywordEnum.צף,
                KeywordEnum.כפול,
                KeywordEnum.ריק,
                KeywordEnum.ארוך,
            }
            if token.value in TYPE_KEYWORDS:
                return self.parse_variable_declaration()

            # Check for Control Flow
            if token.value == KeywordEnum.אם:
                return self.parse_if_statement()
            elif token.value == KeywordEnum.החזר:
                return self.parse_return_statement()
            elif token.value == KeywordEnum.כאשר:
                return self.parse_while_statement()
            elif token.value == KeywordEnum.החלף:
                return self.parse_switch_statement()
            elif token.value == KeywordEnum.עבור:
                return self.parse_for_statement()
            elif token.value == KeywordEnum.עשה:
                return self.parse_dowhile_statement()
            elif token.value == KeywordEnum.שבור:
                return self.parse_break_statement()
            elif token.value == KeywordEnum.המשך:
                return self.parse_continue_statement()

        return self.parse_expression_statement()

    def parse_block(self) -> BlockNode:
        statements = []

        self.eat(OpenBrace)

        while self.current_token() and not isinstance(self.current_token(), CloseBrace):
            statements.append(self.parse_statement())

        if not self.current_token():
            error("Unterminated block")

        self.eat(CloseBrace)

        return BlockNode(statements)

    def parse_variable_declaration(self) -> VarDeclNode:
        HEBREW_TO_C = {
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
            KeywordEnum.מספור: "enum",
        }

        type_parts = []

        # collect type keywords
        while isinstance(self.current_token(), Keyword):
            kw = self.eat(Keyword)
            c_name = HEBREW_TO_C.get(kw.value, kw.value.name)

            # long long special case
            if kw.value == KeywordEnum.ארוך:
                next_t = self.current_token()
                if isinstance(next_t, Keyword) and next_t.value == KeywordEnum.ארוך:
                    self.eat(Keyword)
                    c_name = "long long"

            # Special Case: 'מבנה', 'איחוד', 'מספור' (struct, union, enum)
            if kw.value in (KeywordEnum.מבנה, KeywordEnum.איחוד, KeywordEnum.מספור):
                if not isinstance(self.current_token(), Identifier):
                    error(f"Expected identifier after '{c_name}'")
                name = self.eat(Identifier).name
                c_name = f"{c_name} {name}"

            type_parts.append(c_name)

            if isinstance(self.current_token(), Identifier):
                break

        var_type = " ".join(type_parts)

        if not isinstance(self.current_token(), Identifier):
            error(f"Expected variable name after type '{var_type}'")

        name = self.eat(Identifier).name

        value_node = None
        if isinstance(self.current_token(), AssignmentOperator):
            self.eat(AssignmentOperator)
            value_node = self.parse_expression()

        if not isinstance(self.current_token(), Semicolon):
            error(f"Expected ';' after declaration of '{name}'")

        self.eat(Semicolon)
        return VarDeclNode(var_type, name, value_node)

    def parse_if_statement(self) -> IfStatementNode:
        self.eat(Keyword)  # if

        if not isinstance(self.current_token(), OpenParenthesis):
            error("Expected '(' after if token")

        self.eat(OpenParenthesis)
        cond = self.parse_expression()

        if not isinstance(self.current_token(), CloseParenthesis):
            error("Unterminated parenthesis in if statement")

        self.eat(CloseParenthesis)

        if_block = self.parse_statement()

        else_block = None
        next = self.current_token()
        if isinstance(next, Keyword) and next.value == KeywordEnum.אחרת:
            self.eat(Keyword)  # else
            else_block = self.parse_statement()

        return IfStatementNode(cond, if_block, else_block)

    def parse_while_statement(self) -> WhileNode:
        self.eat(Keyword)  # while

        if not isinstance(self.current_token(), OpenParenthesis):
            error("Expected '(' after while token")

        self.eat(OpenParenthesis)
        cond = self.parse_expression()

        if not isinstance(self.current_token(), CloseParenthesis):
            error("Unterminated parenthesis in while statement")

        self.eat(CloseParenthesis)

        body = self.parse_statement()

        return WhileNode(cond, body)

    def parse_return_statement(self) -> ReturnNode:
        self.eat(Keyword)  # return
        val = self.parse_expression()
        self.eat(Semicolon)
        return ReturnNode(val)

    def parse_break_statement(self) -> BreakNode:
        self.eat(Keyword)  # break
        self.eat(Semicolon)
        return BreakNode()

    def parse_continue_statement(self) -> ContinueNode:
        self.eat(Keyword)  # continue
        self.eat(Semicolon)
        return ContinueNode()

    def parse_switch_statement(self) -> SwitchNode:
        self.eat(Keyword)  # switch
        if not isinstance(self.current_token(), OpenParenthesis):
            error("Expected '(' after switch")
        self.eat(OpenParenthesis)
        expr = self.parse_expression()
        if not isinstance(self.current_token(), CloseParenthesis):
            error("Unterminated expression after switch statement")
        self.eat(CloseParenthesis)

        if not isinstance(self.current_token(), OpenBrace):
            error("Missing '{' after switch statement")
        self.eat(OpenBrace)

        cases = []
        default_case = None

        while self.current_token() and not isinstance(self.current_token(), CloseBrace):
            token = self.current_token()

            if isinstance(token, Keyword) and token.value == KeywordEnum.מקרה:  # case
                self.eat(Keyword)
                lit_token = self.eat(Literal)
                cond = LiteralNode(lit_token)
                self.eat(Colon)

                statements = []
                # keep parsing statements until we hit another 'case', 'default', or '}'
                while (
                    self.current_token()
                    and not (
                        isinstance(self.current_token(), Keyword)
                        and cast(Keyword, self.current_token()).value
                        in (KeywordEnum.מקרה, KeywordEnum.ברירתמחדל)
                    )
                    and not isinstance(self.current_token(), CloseBrace)
                ):
                    statements.append(self.parse_statement())

                cases.append(CaseNode(cond, statements))

            elif (
                isinstance(token, Keyword) and token.value == KeywordEnum.ברירתמחדל
            ):  # default
                self.eat(Keyword)
                self.eat(Colon)

                default_statements = []
                while self.current_token() and not isinstance(
                    self.current_token(), CloseBrace
                ):
                    if (
                        isinstance(self.current_token(), Keyword)
                        and cast(Keyword, self.current_token()).value
                        == KeywordEnum.מקרה
                    ):
                        break
                    default_statements.append(self.parse_statement())

                default_case = BlockNode(default_statements)

            else:
                error(
                    f"Statements in a switch must be inside a 'case' or 'default'. Found: {type(token).__name__}"
                )

        self.eat(CloseBrace)
        return SwitchNode(expr, cases, default_case)

    def parse_for_statement(self) -> ForNode:
        pass

    def parse_dowhile_statement(self) -> AstNode:
        pass

    # --- Expression Stubs ---

    def parse_expression_statement(self) -> AstNode:
        pass

    def parse_expression(self) -> AstNode:
        pass

    def parse_term(self) -> AstNode:
        pass

    def parse_factor(self) -> AstNode:
        pass
