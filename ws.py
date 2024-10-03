import enum
import typing


class Kind(enum.Enum):
    KIND_VALUE_EOF = enum.auto()
    KIND_VALUE_BOOL = enum.auto()
    KIND_VALUE_CHAR = enum.auto()
    KIND_VALUE_INT = enum.auto()
    KIND_VALUE_FLOAT = enum.auto()
    KIND_VALUE_STRING = enum.auto()

    KIND_OPERATOR_ADD = enum.auto()
    KIND_OPERATOR_SUB = enum.auto()
    KIND_OPERATOR_MUL = enum.auto()
    KIND_OPERATOR_DIV = enum.auto()
    KIND_OPERATOR_MOD = enum.auto()

    KIND_OPERATOR_ASN = enum.auto()

    KIND_OPERATOR_OR = enum.auto()
    KIND_OPERATOR_NOT = enum.auto()
    KIND_OPERATOR_AND = enum.auto()

    KIND_OPERATOR_LT = enum.auto()
    KIND_OPERATOR_GT = enum.auto()
    KIND_OPERATOR_EQ = enum.auto()
    KIND_OPERATOR_NEQ = enum.auto()
    KIND_OPERATOR_LTE = enum.auto()
    KIND_OPERATOR_GTE = enum.auto()

    KIND_OPERATOR_BIT_OR = enum.auto()
    KIND_OPERATOR_BIT_NOT = enum.auto()
    KIND_OPERATOR_BIT_AND = enum.auto()
    KIND_OPERATOR_BIT_XOR = enum.auto()
    KIND_OPERATOR_BIT_LST = enum.auto()
    KIND_OPERATOR_BIT_RST = enum.auto()

    KIND_DELIMITER_LPN = enum.auto()
    KIND_DELIMITER_RPN = enum.auto()
    KIND_DELIMITER_LBK = enum.auto()
    KIND_DELIMITER_RBK = enum.auto()
    KIND_DELIMITER_LBC = enum.auto()
    KIND_DELIMITER_RBC = enum.auto()

    KIND_DELIMITER_PRD = enum.auto()
    KIND_DELIMITER_CMA = enum.auto()
    KIND_DELIMITER_CLN = enum.auto()
    KIND_DELIMITER_SMI = enum.auto()

    KIND_DELIMITER_DLA = enum.auto()
    KIND_DELIMITER_HSH = enum.auto()

    KIND_KEYWORD_BOOL = enum.auto()
    KIND_KEYWORD_CHAR = enum.auto()
    KIND_KEYWORD_INT = enum.auto()
    KIND_KEYWORD_FLOAT = enum.auto()
    KIND_KEYWORD_STRING = enum.auto()
    KIND_KEYWORD_ENUM = enum.auto()
    KIND_KEYWORD_STRUCT = enum.auto()
    KIND_KEYWORD_LIST = enum.auto()
    KIND_KEYWORD_ARRAY = enum.auto()
    KIND_KEYWORD_ANY = enum.auto()
    KIND_KEYWORD_VAR = enum.auto()
    KIND_KEYWORD_CONST = enum.auto()
    KIND_KEYWORD_FUN = enum.auto()
    KIND_KEYWORD_MACRO = enum.auto()

    KIND_KEYWORD_FOR = enum.auto()
    KIND_KEYWORD_WHILE = enum.auto()
    KIND_KEYWORD_DO = enum.auto()

    KIND_KEYWORD_SWITCH = enum.auto()
    KIND_KEYWORD_CASE = enum.auto()
    KIND_KEYWORD_DEFAULT = enum.auto()
    KIND_KEYWORD_MATCH = enum.auto()
    KIND_KEYWORD_IF = enum.auto()
    KIND_KEYWORD_ELIF = enum.auto()
    KIND_KEYWORD_ESE = enum.auto()

    KIND_KEYWORD_BREAK = enum.auto()
    KIND_KEYWORD_CONTINUE = enum.auto()
    KIND_KEYWORD_RETURN = enum.auto()


class Token:
    def __init__(self, kind: Kind, value: typing.Union[bool, int, float, str], line : int) -> None:
        self.kind = kind
        self.value = value
        self.line = line

    def __str__(self) -> str:
        return f'Token {{ kind: {self.kind.name}, value: {self.value}, line: {self.line} }}'


class Lexer:
    def __init__(self, path: str, source: str) -> None:
        self.path = path
        self.source = source
        self.length: int = len(source)
        self.index: int = 0
        self.line: int = 1

    def eof(self) -> bool:
        return self.index < self.length

    def current(self) -> str:
        return self.source[self.index] if self.eof() else "\0"

    def advance(self) -> None:
        self.index += 1

    def char(self) -> str:
        self.advance()
        character = self.current()
        self.advance()
        if self.eof()