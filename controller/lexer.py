from re import match

from controller.tokenType import (
    Token,
    TokenType
)


class Lexer:

    def __init__(self, source: str) -> None:
        self._source = source
        self._character: str = ""
        self._read_position: int = 0
        self._position: int = 0

        self._read_character()

    def next_token(self) -> Token:
        if match(r'^=$', self._character):
            token = Token(TokenType.EQUALS, self._character)
        elif match(r'^<$', self._character):
            token = Token(TokenType.TAG_OPENER, self._character)
        elif match(r'^>$', self._character):
            token = Token(TokenType.TAG_CLOSER, self._character)
        elif match(r'^/$', self._character):
            token = Token(TokenType.CLOSING_TAG_MARKER, self._character)
        elif match(r'^[a-zA-Z]$', self._character):
            token = Token(TokenType.NAME_TAG, self._character)
        elif match(r'^[0-9]$', self._character):
            token = Token(TokenType.VALUE_TAG, self._character)
        else:
            token = Token(TokenType.ILLEGAL, self._character)

        self._read_character()
        return token

    def _read_character(self) -> None:
        if self._read_position >= len(self._source):
            self._character = ""
        else:
            self._character = self._source[self._read_position]

        self._position = self._read_position
        self._read_position += 1
