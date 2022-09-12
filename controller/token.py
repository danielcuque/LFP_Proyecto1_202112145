from enum import (
    auto,
    Enum,
    unique
)

from typing import NamedTuple


@unique
class TokenType(Enum):
    ASSIGN = auto()
    SLASH = auto()
    LBRACE = auto()
    RBRACE = auto()


class Token(NamedTuple):
    token_type: TokenType
    literal: str

    def __str__(self) -> str:
        return f'Type: {self.token_type}, Literal: {self.literal}'
