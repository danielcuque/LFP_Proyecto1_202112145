from enum import (
    Enum,
    auto,
    unique
)

from typing import NamedTuple


@unique
class TokenType(Enum):
    TAG_OPENER = auto()
    TAG_CLOSER = auto()
    CLOSING_TAG_MARKER = auto()
    EQUALS = auto()
    NAME_TAG = auto()
    VALUE_TAG = auto()
    ILLEGAL = auto()


class Token(NamedTuple):
    tokenType: TokenType
    literal: str

    def __str__(self) -> str:
        return f"Token({self.tokenType}, {self.literal})"
