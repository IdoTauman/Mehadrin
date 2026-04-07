from abc import ABC

from tokens import Token, Literal


class AstNode(ABC):
    def __init__(self) -> None:
        super().__init__()

class ProgramNode(AstNode):
    def __init__(self, statements: list[AstNode]) -> None:
        super().__init__()
        self.statements: list[AstNode] = statements

class VarDeclNode(AstNode):
    def __init__(self, type: str, name: str, value_node: AstNode | None) -> None:
        super().__init__()
        self.type: str = type
        self.name: str = name
        self.value_node: AstNode | None = value_node

class BinOpNode(AstNode):
    def __init__(self, left: AstNode, op: Token, right: AstNode) -> None:
        super().__init__()
        self.left: AstNode = left
        self.op: Token = op
        self.right: AstNode = right

class LiteralNode(AstNode):
    def __init__(self, value: Literal) -> None:
        super().__init__()
        self.value: int | float | str | None = value.value

class IfStatementNode(AstNode):
    def __init__(self, cond: AstNode, if_block: AstNode, else_block: AstNode | None) -> None:
        super().__init__()
        self.cond: AstNode = cond
        self.if_block: AstNode = if_block
        self.else_block: AstNode | None = else_block

class IdentifierNode(AstNode):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name

class BlockNode(AstNode):
    """Represents code inside { braces }"""
    def __init__(self, statements: list[AstNode]) -> None:
        super().__init__()
        self.statements: list[AstNode] = statements

class UnaryOpNode(AstNode):
    def __init__(self, op: Token, operand: AstNode) -> None:
        super().__init__()
        self.op: Token = op
        self.operand: AstNode = operand

class AssignmentNode(AstNode):
    def __init__(self, target: str, value: AstNode) -> None:
        super().__init__()
        self.target: str = target
        self.value: AstNode = value

class WhileNode(AstNode):
    def __init__(self, cond: AstNode, body: AstNode) -> None:
        super().__init__()
        self.cond: AstNode = cond
        self.body: AstNode = body

class ForNode(AstNode):
    def __init__(self, init: AstNode | None, cond: AstNode | None, step: AstNode | None, body: AstNode) -> None:
        super().__init__()
        self.init: AstNode | None = init
        self.cond: AstNode | None = cond
        self.step: AstNode | None = step
        self.body: AstNode = body

class CaseNode(AstNode):
    def __init__(self, condition: LiteralNode, body: list[AstNode]) -> None:
        super().__init__()
        self.condition: LiteralNode = condition
        self.body: list[AstNode] = body

class SwitchNode(AstNode):
    def __init__(self, expression: AstNode, cases: list[CaseNode], default_case: AstNode | None) -> None:
        super().__init__()
        self.expression: AstNode = expression
        self.cases: list[CaseNode] = cases
        self.default_case: AstNode | None = default_case

class ReturnNode(AstNode):
    def __init__(self, value: AstNode | None) -> None:
        super().__init__()
        self.value: AstNode | None = value

class BreakNode(AstNode):
    def __init__(self) -> None:
        super().__init__()

class ContinueNode(AstNode):
    def __init__(self) -> None:
        super().__init__()

class FunctionCallNode(AstNode):
    def __init__(self, func_name: str, arguments: list[AstNode]) -> None:
        super().__init__()
        self.func_name: str = func_name
        self.arguments: list[AstNode] = arguments