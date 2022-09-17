from enum import (
    Enum,
    auto,
    unique
)

from typing import (
    Dict,
    NamedTuple
)


@unique
class TokenType(Enum):
    AUTO_CLOSE_TAG = auto()
    END_TAG = auto()
    ILLEGAL = auto()
    START_TAG = auto()
    TEXT = auto()
    INT_NUMBER = auto()
    FLOAT_NUMBER = auto()


class Token(NamedTuple):
    tokenType: TokenType
    literal: str
    column: int
    row: int
    is_valid = property(lambda self: self.tokenType != TokenType.ILLEGAL)

    def __str__(self) -> str:
        return f"Token Type: {self.tokenType}, Lexeme: {self.literal}, Column: {self.column}, Row: {self.row}, Is Valid: {self.is_valid}"

    # def lookup_token_type(literal: str) -> TokenType:
    #     keywords: Dict[str, TokenType] = {
    #         'tipo': TokenType.NAME_TAG,
    #         'operacion': TokenType.NAME_TAG,
    #     }

    #     return keywords.get(literal, TokenType.VALUE_TAG)
